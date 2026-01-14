import datetime
import filecmp
import inspect
import shutil
from pathlib import Path
from unittest import TestCase

from bx_py_utils.test_utils.datetime import parse_dt
from bx_py_utils.test_utils.redirect import RedirectOut
from bx_py_utils.test_utils.snapshot import assert_text_snapshot
from manageprojects.test_utils.subprocess import (
    SimpleRunReturnCallback,
    SubprocessCallMock,
)
from manageprojects.utilities.temp_path import TemporaryDirectory
from packaging.version import Version

from cli_base.cli_dev import PACKAGE_ROOT
from cli_base.cli_tools.git import (
    Git,
    GitCommitMessage,
    GitHistoryEntry,
    GithubInfo,
    GitlabInfo,
    GitLogLine,
    GitTagInfo,
    GitTagInfos,
    NoGitRepoError,
)
from cli_base.cli_tools.test_utils.environment_fixtures import MockCurrentWorkDir
from cli_base.cli_tools.test_utils.git_utils import init_git
from cli_base.cli_tools.test_utils.logs import AssertLogs


class MockedGit(Git):
    def __init__(self, *, mocked_output):
        self.mocked_output = mocked_output
        super().__init__(cwd=Path('/mocked/'), detect_root=False)

    def git_verbose_check_output(self, *args, **kwargs):
        return self.mocked_output


class GitTestCase(TestCase):  # TODO: Use BaseTestCase
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        with RedirectOut() as out_buffer:
            cls.own_git = Git(cwd=PACKAGE_ROOT, detect_root=True)
            git_root_path = cls.own_git.cwd
        assert git_root_path == PACKAGE_ROOT, f'{git_root_path=} is not {PACKAGE_ROOT=}'
        assert out_buffer.stderr == '', f'{out_buffer.stderr=}'

    def test_detect_cwd(self):
        with MockCurrentWorkDir(prefix='test_detect_cwd') as mocked_cwd:
            temp_path = mocked_cwd.temp_path
            with self.assertRaises(NoGitRepoError) as cm:
                Git()
            self.assertEqual(str(cm.exception), f'"{temp_path}" is not a git repository')

            with self.assertRaises(NoGitRepoError) as cm:
                Git(cwd=temp_path)
            self.assertEqual(str(cm.exception), f'"{temp_path}" is not a git repository')

            # e.g.: "git.init()" should be used:
            git = Git(cwd=temp_path, detect_root=False)
            self.assertEqual(git.cwd, temp_path)

    def test_config(self):
        with TemporaryDirectory(prefix='test_init_git_') as temp_path:
            git = Git(cwd=temp_path, detect_root=False)
            git.init()

            self.assertEqual(git.get_config(key='user.name'), 'Foo Bar')
            self.assertEqual(git.get_config(key='user.email'), 'foo-bar@test.tld')

            keys = git.list_config_keys()
            self.assertIsInstance(keys, set)
            self.assertGreaterEqual(len(keys), 1)

            section = 'cli-base'
            test_key = f'{section}.test-config-entry'

            value = git.get_config(key=test_key)
            self.assertIsNone(value)

            output = git.config(key=test_key, value='test', scope='local')
            self.assertEqual(output, '')

            value = git.get_config(key=test_key)
            self.assertEqual(value, 'test')

            git.git_verbose_check_output('config', '--local', '--remove-section', section)

            value = git.get_config(key=test_key)
            self.assertIsNone(value)

    def test_own_git_repo(self):
        git_hash = self.own_git.get_current_hash(verbose=False)
        self.assertEqual(len(git_hash), 7, f'Wrong: {git_hash!r}')

        now = datetime.datetime.now(datetime.UTC)

        commit_date = self.own_git.get_commit_date(verbose=False)
        self.assertIsInstance(commit_date, datetime.datetime)
        self.assertGreater(commit_date, parse_dt('2025-01-01T00:00:00+0000'))
        self.assertLess(commit_date, now)  # We are not in the future ;)

        with self.assertLogs('cli_base'):
            file_dt1 = self.own_git.get_file_dt('cli.py', with_tz=True)
            self.assertIsInstance(file_dt1, datetime.datetime)
            self.assertGreater(file_dt1, parse_dt('2023-01-01T00:00:00+0000'))
            self.assertLess(file_dt1, now)  # We are not in the future ;)

            file_dt2 = self.own_git.get_file_dt('cli.py', with_tz=False)
            self.assertIsInstance(file_dt2, datetime.datetime)
            self.assertGreater(file_dt2, datetime.datetime(2023, 1, 1))
            self.assertLess(file_dt2, datetime.datetime(2026, 1, 1))

        git_bin = shutil.which('git')
        with SubprocessCallMock() as call_mock:
            self.own_git.push(name='origin', branch_name='my_branch')
        self.assertEqual(call_mock.get_popenargs(), [[git_bin, 'push', 'origin', 'my_branch']])

        with SubprocessCallMock(return_callback=SimpleRunReturnCallback(stdout='mocked output')) as call_mock:
            output = self.own_git.push(name='origin', branch_name='my_branch', get_output=True)
        self.assertEqual(call_mock.get_popenargs(), [[git_bin, 'push', 'origin', 'my_branch']])
        self.assertEqual(output, 'mocked output')

        with SubprocessCallMock() as call_mock:
            self.own_git.checkout_branch('foo-bar')
        self.assertEqual(call_mock.get_popenargs(), [[git_bin, 'checkout', 'foo-bar']])

        with SubprocessCallMock() as call_mock:
            self.own_git.checkout_new_branch('foo-bar')
        self.assertEqual(call_mock.get_popenargs(), [[git_bin, 'checkout', '-b', 'foo-bar']])

        with SubprocessCallMock(return_callback=SimpleRunReturnCallback(stdout='mocked output')) as call_mock:
            output = self.own_git.pull(name='origin', branch_name='my_branch')
        self.assertEqual(call_mock.get_popenargs(), [[git_bin, 'pull', 'origin', 'my_branch']])
        self.assertEqual(output, 'mocked output')

    def test_init_git(self):
        with TemporaryDirectory(prefix='test_init_git_') as temp_path:
            Path(temp_path, 'foo.txt').touch()
            Path(temp_path, 'bar.txt').touch()

            git, git_hash = init_git(temp_path)
            self.assertEqual(len(git_hash), 7)
            self.assertEqual(
                git.ls_files(verbose=False),
                [Path(temp_path, 'bar.txt'), Path(temp_path, 'foo.txt')],
            )

    def test_git_diff(self):
        with TemporaryDirectory(prefix='test_git_diff_') as temp_path:
            change_txt_path = Path(temp_path, 'change.txt')
            change_txt_path.write_text('This is the first revision!')
            Path(temp_path, 'unchange.txt').write_text('This file will be not changed')

            git, first_hash = init_git(temp_path)
            self.assertEqual(len(first_hash), 7)
            self.assertEqual(
                git.ls_files(verbose=False),
                [Path(temp_path, 'change.txt'), Path(temp_path, 'unchange.txt')],
            )

            change_txt_path.write_text('This is the second revision!')

            git.add('.', verbose=False)
            git.commit('The second commit', verbose=False)

            second_hash = git.get_current_hash(verbose=False)
            reflog = git.reflog(verbose=False)
            self.assertIn('The second commit', reflog)
            self.assertIn(first_hash, reflog)
            self.assertIn(second_hash, reflog)

            diff_txt = git.diff(first_hash, second_hash)
            self.assertIn('--- a/change.txt', diff_txt)
            self.assertIn('+++ b/change.txt', diff_txt)
            self.assertIn('@@ -1 +1 @@', diff_txt)
            assert_text_snapshot(got=diff_txt, extension='.patch')

    def test_git_apply_patch(self):
        with TemporaryDirectory(prefix='test_git_apply_patch_') as temp_path:
            repo_path = temp_path / 'git-repo'
            project_path = temp_path / 'project'

            repo_change_path = repo_path / 'directory1' / 'pyproject.toml'
            repo_change_path.parent.mkdir(parents=True)
            repo_change_path.write_text(
                inspect.cleandoc(
                    '''
                    [tool.darker]
                    src = ['.']
                    revision = "origin/main..."
                    line_length = 79  # 79 is initial, change to 100 later
                    verbose = true
                    diff = false
                    '''
                )
            )
            Path(repo_path, 'directory1', 'unchanged.txt').write_text('Will be not changed file')

            shutil.copytree(repo_path, project_path)  # "fake" cookiecutter output
            project_git, project_first_hash = init_git(project_path)  # init project

            # 1:1 copy?
            project_change_path = project_path / 'directory1' / 'pyproject.toml'
            self.assertTrue(filecmp.cmp(project_change_path, repo_change_path))

            # init "cookiecutter" source project:
            repo_git, repo_first_hash = init_git(repo_path)

            # Add a change to "fake" source:
            repo_change_path.write_text(
                inspect.cleandoc(
                    '''
                    [tool.darker]
                    src = ['.']
                    revision = "origin/main..."
                    line_length = 100  # 79 is initial, change to 100 later
                    verbose = true
                    diff = false
                    '''
                )
            )
            repo_git.add('.', verbose=False)
            repo_git.commit('The second commit', verbose=False)
            second_hash = repo_git.get_current_hash(verbose=False)

            # Generate a patch via git diff:
            diff_txt = repo_git.diff(repo_first_hash, second_hash)
            self.assertIn('directory1/pyproject.toml', diff_txt)
            patch_file_path = temp_path / 'git-diff-1.patch'
            patch_file_path.write_text(diff_txt)
            assert_text_snapshot(got=diff_txt, extension='.patch')

            # Change the project a little bit, before apply the git diff patch:

            # Just add a new file, unrelated to the diff patch:
            Path(project_path, 'directory1', 'new.txt').write_text('A new project file')

            # Commit the new file:
            project_git.add('.', verbose=False)
            project_git.commit('Add a new project file', verbose=False)

            # Change a diff related file:
            project_change_path.write_text(
                inspect.cleandoc(
                    '''
                    [tool.darker]
                    src = ['.']
                    revision = "origin/main..."
                    line_length = 79  # 79 is initial, change to 100 later
                    verbose = true
                    skip_string_normalization = true  # Added from project
                    diff = false
                    '''
                )
            )

            # Commit the changes, too:
            project_git.add('.', verbose=False)
            project_git.commit('Existing project file changed', verbose=False)

            # Now: Merge the project changes with the "fake" cookiecutter changes:
            project_git.apply(patch_file_path)

            # Merge successful?
            #  * line_length <<< change from "fake" cookiecutter changed
            #  * skip_string_normalization <<< added by project
            # The Rest is unchanged
            self.assertEqual(
                project_change_path.read_text(),
                inspect.cleandoc(
                    '''
                    [tool.darker]
                    src = ['.']
                    revision = "origin/main..."
                    line_length = 100  # 79 is initial, change to 100 later
                    verbose = true
                    skip_string_normalization = true  # Added from project
                    diff = false
                    '''
                ),
            )

    def test_status(self):
        with TemporaryDirectory(prefix='test_status_') as temp_path:
            change_txt_path = Path(temp_path, 'change.txt')
            change_txt_path.write_text('This is the first revision!')

            git, first_hash = init_git(temp_path)

            change_txt_path.write_text('Changed content')
            Path(temp_path, 'added.txt').write_text('Added file')

            status = git.status(verbose=False)
            self.assertEqual(status, [('M', 'change.txt'), ('??', 'added.txt')])

            git.add('.', verbose=False)
            git.commit('The second commit', verbose=False)

            status = git.status(verbose=False)
            self.assertEqual(status, [])

    def test_branch_names(self):
        with TemporaryDirectory(prefix='test_branch_names_') as temp_path, RedirectOut() as out_buffer:
            Path(temp_path, 'foo.txt').touch()
            git, first_hash = init_git(temp_path)

            with AssertLogs(self, loggers=('cli_base',)) as logs:
                branch_names = git.get_branch_names()
                self.assertEqual(branch_names, ['main'])
            logs.assert_in("Git raw branches: ['* main']")

            git.git_verbose_check_call('checkout', '-b', 'foobar')

            with AssertLogs(self, loggers=('cli_base',)) as logs:
                branch_names = git.get_branch_names()
                self.assertEqual(branch_names, ['foobar', 'main'])
            logs.assert_in("Git raw branches: ['* foobar', '  main']")

            with AssertLogs(self, loggers=('cli_base',)):
                main_branch_name = git.get_main_branch_name()
                self.assertEqual(main_branch_name, 'main')
        self.assertEqual(out_buffer.stderr, '')

        # Test with local "cli_base" git clone:
        with AssertLogs(self, loggers=('cli_base',)), RedirectOut() as out_buffer:
            git = Git(cwd=PACKAGE_ROOT, detect_root=True)
            main_branch_name = git.get_main_branch_name()
            self.assertEqual(main_branch_name, 'main')
        self.assertEqual(out_buffer.stderr, '')

    def test_log(self):
        with TemporaryDirectory(prefix='test_get_version_from_tags') as temp_path:
            Path(temp_path, '1.txt').touch()
            git, first_hash = init_git(temp_path, comment='The initial commit ;)')

            git.tag('v0.0.1', message='one', verbose=False)

            Path(temp_path, '2.txt').touch()
            git.add(spec='.')
            git.commit(comment='Useless 1')

            Path(temp_path, '3.txt').touch()
            git.add(spec='.')
            git.commit(comment='Useless 2')

            git.tag('v0.2.0', message='two', verbose=False)
            Path(temp_path, '4.txt').touch()
            git.add(spec='.')
            git.commit(comment='Useless 3')

            output = git.log(format='%s')
            self.assertEqual(output, ['Useless 3', 'Useless 2', 'Useless 1', 'The initial commit ;)'])

            output = git.log(format='%s', no_merges=True, commit1='HEAD', commit2='v0.0.1')
            self.assertEqual(output, ['Useless 3', 'Useless 2', 'Useless 1'])

    def test_get_version_from_tags(self):
        with TemporaryDirectory(prefix='test_get_version_from_tags') as temp_path:
            Path(temp_path, 'foo.txt').touch()
            git, first_hash = init_git(temp_path)

            empty_tags = git.get_tag_infos()
            self.assertEqual(empty_tags, GitTagInfos(tags=[]))
            self.assertEqual(empty_tags.get_releases(), [])
            self.assertIs(empty_tags.get_last_release(), None)

            git.tag('v0.0.1', message='one', verbose=False)
            git.tag('v0.2.dev1', message='dev release', verbose=False)
            git.tag('v0.2.0a1', message='pre release', verbose=False)
            git.tag('v0.2.0rc2', message='release candidate', verbose=False)
            git.tag('v0.2.0', message='two', verbose=False)
            git.tag('foo', message='foo', verbose=False)
            git.tag('bar', message='bar', verbose=False)

            self.assertEqual(git.tag_list(), ['bar', 'foo', 'v0.0.1', 'v0.2.0', 'v0.2.0a1', 'v0.2.0rc2', 'v0.2.dev1'])

            with AssertLogs(self, loggers=('cli_base',)) as logs:
                git_tag_infos = git.get_tag_infos()
                self.assertEqual(
                    git_tag_infos,
                    GitTagInfos(
                        tags=[
                            GitTagInfo(raw_tag='bar', version=None),
                            GitTagInfo(raw_tag='foo', version=None),
                            GitTagInfo(raw_tag='v0.0.1', version=Version('0.0.1')),
                            GitTagInfo(raw_tag='v0.2.dev1', version=Version('0.2.dev1')),
                            GitTagInfo(raw_tag='v0.2.0a1', version=Version('0.2.0a1')),
                            GitTagInfo(raw_tag='v0.2.0rc2', version=Version('0.2.0rc2')),
                            GitTagInfo(raw_tag='v0.2.0', version=Version('0.2.0')),
                        ]
                    ),
                )
            logs.assert_in('Ignore: Invalid version')

            self.assertTrue(git_tag_infos.exists(Version('0.0.1')))
            self.assertTrue(git_tag_infos.exists(Version('0.2.0rc2')))
            self.assertFalse(git_tag_infos.exists(Version('1.0')))

            self.assertEqual(
                git_tag_infos.get_releases(),
                [
                    GitTagInfo(raw_tag='v0.0.1', version=Version('0.0.1')),
                    GitTagInfo(raw_tag='v0.2.0', version=Version('0.2.0')),
                ],
            )
            self.assertEqual(
                git_tag_infos.get_last_release(),
                GitTagInfo(raw_tag='v0.2.0', version=Version('0.2.0')),
            )

    def test_get_remote_url_and_github_username(self):
        with self.assertLogs('cli_base'), TemporaryDirectory(
            prefix='test_get_remote_url_and_github_username'
        ) as temp_path:
            Path(temp_path, 'foo.txt').touch()
            git, first_hash = init_git(temp_path)

            self.assertEqual(git.get_remote_url(), '.')
            self.assertIs(git.get_github_username(), None)

            git.git_verbose_check_call('remote', 'set-url', 'origin', 'git@github.com:user-name/project-name.git')

            self.assertEqual(git.get_remote_url(), 'git@github.com:user-name/project-name.git')
            self.assertEqual(git.get_github_username(), 'user-name')

    def test_get_project_info(self):
        with self.assertLogs('cli_base'), TemporaryDirectory(prefix='github') as temp_path:
            Path(temp_path, 'foo.txt').touch()
            git, first_hash = init_git(temp_path)

            self.assertEqual(git.get_remote_url(), '.')
            self.assertIs(git.get_project_info(), None)

            git.git_verbose_check_call('remote', 'set-url', 'origin', 'git@github.com:user-name/project-name.git')
            project_info = git.get_project_info()
            self.assertEqual(
                project_info,
                GithubInfo(
                    remote_url='git@github.com:user-name/project-name.git',
                    user_name='user-name',
                    project_name='project-name',
                ),
            )
            self.assertEqual(
                project_info.commit_url(hash='<hash>'),
                'https://github.com/user-name/project-name/commit/<hash>',
            )
            self.assertEqual(
                project_info.compare_url(old='v1', new='v2'),
                'https://github.com/user-name/project-name/compare/v1...v2',
            )

        ##############################################################
        # https GitHub

        with self.assertLogs('cli_base'), TemporaryDirectory(prefix='github') as temp_path:
            Path(temp_path, 'foo.txt').touch()
            git, first_hash = init_git(temp_path)
            git.git_verbose_check_call(
                'remote', 'set-url', 'origin', 'https://github.com/user-name/project-name.git'
            )
            project_info = git.get_project_info()
            self.assertEqual(
                project_info,
                GithubInfo(
                    remote_url='https://github.com/user-name/project-name.git',
                    user_name='user-name',
                    project_name='project-name',
                ),
            )
            self.assertEqual(
                project_info.commit_url(hash='<hash>'),
                'https://github.com/user-name/project-name/commit/<hash>',
            )
            self.assertEqual(
                project_info.compare_url(old='v1', new='v2'),
                'https://github.com/user-name/project-name/compare/v1...v2',
            )

        ##############################################################
        # GitLab

        with self.assertLogs('cli_base'), TemporaryDirectory(prefix='gitlab') as temp_path:
            Path(temp_path, 'foo.txt').touch()
            git, first_hash = init_git(temp_path)

            self.assertEqual(git.get_remote_url(), '.')
            self.assertIs(git.get_project_info(), None)

            git.git_verbose_check_call('remote', 'set-url', 'origin', 'git@gitlab.com:user-name/project-name.git')
            project_info = git.get_project_info()
            self.assertEqual(
                project_info,
                GitlabInfo(
                    remote_url='git@gitlab.com:user-name/project-name.git',
                    user_name='user-name',
                    project_name='project-name',
                ),
            )
            self.assertEqual(
                project_info.commit_url(hash='<hash>'),
                'https://gitlab.com/user-name/project-name/-/commit/<hash>',
            )
            self.assertEqual(
                project_info.compare_url(old='v1', new='v2'),
                'https://gitlab.com/user-name/project-name/-/compare/v1...v2',
            )

    def test_first_commit_info(self):
        # The first commit of this project will never be changed, isn't it? So use it for testing ;)
        self.assertEqual(
            self.own_git.first_commit_info(),
            GitLogLine(
                hash='d89f23b',
                date=datetime.date(2023, 5, 21),
                author='JensDiemer',
                comment='init',
            ),
        )

    def test_get_tag_history(self):
        with TemporaryDirectory(prefix='test_get_tag_history') as temp_path:
            test_file_path = Path(temp_path, 'foo.txt')
            test_file_path.touch()
            git, first_hash = init_git(temp_path, comment='The initial commit ;)')
            tag_history = git.get_tag_history()
            self.assertEqual(
                tag_history,
                [
                    GitHistoryEntry(
                        tag=GitTagInfo(raw_tag='1f8bbf9', version=None),
                        last='HEAD',
                        next='1f8bbf9',
                        log_lines=[
                            GitLogLine(
                                hash='1f8bbf9',
                                date=datetime.date(2023, 11, 1),
                                author='Mr. Test',
                                comment='The initial commit ;)',
                            )
                        ],
                    )
                ],
            )

    def test_get_commit_date(self):
        self.assertEqual(
            MockedGit(mocked_output='2022-10-25 20:43:10 +0200\n').get_commit_date(),
            parse_dt('2022-10-25T20:43:10+0200'),
        )
        self.assertEqual(
            MockedGit(mocked_output='2022-10-25T20:43:10+0200\n').get_commit_date(),
            parse_dt('2022-10-25T20:43:10+0200'),
        )
        self.assertEqual(
            MockedGit(mocked_output='2024-08-02T11:14:55Z\n').get_commit_date(),
            parse_dt('2024-08-02T11:14:55+0000'),
        )

    def test_commit_message(self):
        with TemporaryDirectory(prefix='test_commit_message_') as temp_path:
            git = Git(cwd=temp_path, detect_root=False)
            git.init()
            Path(temp_path, 'foobar.txt').touch()
            git.add('.', verbose=False)
            git.commit(
                comment=GitCommitMessage(
                    summary='A Commit Message',
                    description='With some text...',
                ),
                verbose=False,
            )

            self.assertEqual(
                git.get_commit_message(),
                GitCommitMessage(
                    summary='A Commit Message',
                    description='With some text...',
                ),
            )

    def test_changed_files(self):
        with TemporaryDirectory(prefix='test_changed_files_') as temp_path:
            git = Git(cwd=temp_path, detect_root=False)
            git.init()
            Path(temp_path, 'foo.txt').touch()
            Path(temp_path, 'bar.txt').touch()
            self.assertEqual(
                git.changed_files(),
                [
                    temp_path / 'bar.txt',
                    temp_path / 'foo.txt',
                ],
            )
