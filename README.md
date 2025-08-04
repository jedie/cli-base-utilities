# cli-base-utilities

[![tests](https://github.com/jedie/cli-base-utilities/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/jedie/cli-base-utilities/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/cli-base-utilities/branch/main/graph/badge.svg)](https://app.codecov.io/github/jedie/cli-base-utilities)
[![cli-base-utilities @ PyPi](https://img.shields.io/pypi/v/cli-base-utilities?label=cli-base-utilities%20%40%20PyPi)](https://pypi.org/project/cli-base-utilities/)
[![Python Versions](https://img.shields.io/pypi/pyversions/cli-base-utilities)](https://github.com/jedie/cli-base-utilities/blob/main/pyproject.toml)
[![License GPL-3.0-or-later](https://img.shields.io/pypi/l/cli-base-utilities)](https://github.com/jedie/cli-base-utilities/blob/main/LICENSE)

Helpers to build a CLI program and some useful tools for CLI programs.

```
pip install cli-base-utilities
```


## Features

Some of the features are:

* [`run_pip_audit()` to run `pip-audit` with configuration from `pyproject.toml`](https://github.com/jedie/cli-base-utilities/blob/main/docs/pip_audit.md)

TODO: Document all features here ;)


# start development

```bash
~$ git clone https://github.com/jedie/cli-base-utilities.git
~$ cd cli-base-utilities
~/cli-base-utilities$ ./dev-cli.py --help
```


# dev CLI

[comment]: <> (✂✂✂ auto generated dev help start ✂✂✂)
```
usage: ./dev-cli.py [-h]
                    {check-code-style,coverage,fix-code-style,install,mypy,nox,pip-audit,publish,t
est,update,update-test-snapshot-files,version}



╭─ options ──────────────────────────────────────────────────────────────────────────────────────╮
│ -h, --help        show this help message and exit                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ subcommands ──────────────────────────────────────────────────────────────────────────────────╮
│ {check-code-style,coverage,fix-code-style,install,mypy,nox,pip-audit,publish,test,update,updat │
│ e-test-snapshot-files,version}                                                                 │
│     check-code-style                                                                           │
│                   Check code style by calling darker + flake8                                  │
│     coverage      Run tests and show coverage report.                                          │
│     fix-code-style                                                                             │
│                   Fix code style of all cli_base source code files via darker                  │
│     install       Run pip-sync and install 'cli_base' via pip as editable.                     │
│     mypy          Run Mypy (configured in pyproject.toml)                                      │
│     nox           Run nox                                                                      │
│     pip-audit     Run pip-audit check against current requirements files                       │
│     publish       Build and upload this project to PyPi                                        │
│     test          Run unittests                                                                │
│     update        Update "requirements*.txt" dependencies files                                │
│     update-test-snapshot-files                                                                 │
│                   Update all test snapshot files (by remove and recreate all snapshot files)   │
│     version       Print version and exit                                                       │
╰────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated dev help end ✂✂✂)


# app CLI

[comment]: <> (✂✂✂ auto generated app help start ✂✂✂)
```
usage: ./cli.py [-h] {update-readme-history,version}



╭─ options ──────────────────────────────────────────────────────────────────────────────────────╮
│ -h, --help        show this help message and exit                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ subcommands ──────────────────────────────────────────────────────────────────────────────────╮
│ {update-readme-history,version}                                                                │
│     update-readme-history                                                                      │
│                   Update project history base on git commits/tags in README.md Will be exited  │
│                   with 1 if the README.md was updated otherwise with 0.                        │
│                                                                                                │
│                   Also, callable via e.g.:                                                     │
│                       python -m cli_base update-readme-history -v                              │
│     version       Print version and exit                                                       │
╰────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated app help end ✂✂✂)


# DEMO app CLI

[comment]: <> (✂✂✂ auto generated demo help start ✂✂✂)
```
usage: ./demo-cli.py [-h]
                     {demo-endless-loop,demo-verbose-check-output-error,edit-settings,print-settin
gs,systemd-debug,systemd-logs,systemd-remove,systemd-setup,systemd-status,systemd-stop,version}



╭─ options ──────────────────────────────────────────────────────────────────────────────────────╮
│ -h, --help        show this help message and exit                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ subcommands ──────────────────────────────────────────────────────────────────────────────────╮
│ {demo-endless-loop,demo-verbose-check-output-error,edit-settings,print-settings,systemd-debug, │
│ systemd-logs,systemd-remove,systemd-setup,systemd-status,systemd-stop,version}                 │
│     demo-endless-loop                                                                          │
│                   Just a useless example command, used in systemd DEMO: It just print some     │
│                   information in a endless loop.                                               │
│     demo-verbose-check-output-error                                                            │
│                   DEMO for a error calling                                                     │
│                   cli_base.cli_tools.subprocess_utils.verbose_check_output()                   │
│     edit-settings                                                                              │
│                   Edit the settings file. On first call: Create the default one.               │
│     print-settings                                                                             │
│                   Display (anonymized) MQTT server username and password                       │
│     systemd-debug                                                                              │
│                   Print Systemd service template + context + rendered file content.            │
│     systemd-logs  List and follow logs of systemd service. (May need sudo)                     │
│     systemd-remove                                                                             │
│                   Write Systemd service file, enable it and (re-)start the service. (May need  │
│                   sudo)                                                                        │
│     systemd-setup                                                                              │
│                   Write Systemd service file, enable it and (re-)start the service. (May need  │
│                   sudo)                                                                        │
│     systemd-status                                                                             │
│                   Display status of systemd service. (May need sudo)                           │
│     systemd-stop  Stops the systemd service. (May need sudo)                                   │
│     version       Print version and exit                                                       │
╰────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated demo help end ✂✂✂)


# Generate project history base on git commits/tags

Add a test case similar to [cli_base/tests/test_readme_history.py](https://github.com/jedie/cli-base-utilities/blob/main/cli_base/tests/test_readme_history.py) into your project.
Add the needed `start`/`end` comments into your README.

To make a new release, do this:

* Increase your project version number
* Run tests to update the README
* commit the changes
* Create release

It's recommended to use git hookd (via [pre-commit](https://pre-commit.com/)) to update the README.
For this, add in your `pyproject.toml`:

```toml
[tool.cli_base]
version_module_name = "<your_package>" # Must provide the `__version__` attribute
```

Copy&paste [.pre-commit-config.yaml](https://github.com/jedie/cli-base-utilities/blob/main/.pre-commit-config.yaml) into your project.

Add `pre-commit` to your requirements and install the git hooks by:

```bash
.venv/bin/pre-commit install
.venv/bin/pre-commit autoupdate
```

# Update pre-commit hooks

Update version in `.pre-commit-config.yaml` and make a release.

The Problem: The hooks are broken, if the "new" version is not tagged yet.
To create a release, it's possible to use all git commands (commit, push, etc) with `--no-verify` to skip the hooks.

It's easier to temporarily uninstall the hooks, create the release and install the hooks again, e.g.:

```bash
.../cli-base-utilities$ .venv/bin/pre-commit uninstall
# ...bump version, commit, push, merge... create release...
.../cli-base-utilities$ .venv/bin/pre-commit install
```

# Backwards-incompatible changes

## v0.14 - Switch from pip-tools to uv

`cli_base.run_pip_audit.run_pip_audit()` works now with `uv` base projects instead of `pip-tools`.


# history

[comment]: <> (✂✂✂ auto generated history start ✂✂✂)

* [v0.20.0](https://github.com/jedie/cli-base-utilities/compare/v0.19.0...v0.20.0)
  * 2025-08-04 - Release v0.20.0
  * 2025-08-04 - Fix git history caused by github
* [v0.19.0](https://github.com/jedie/cli-base-utilities/compare/v0.18.0...v0.19.0)
  * 2025-07-29 - Expand Git() around commit message
  * 2025-07-29 - Update requirements
* [v0.18.0](https://github.com/jedie/cli-base-utilities/compare/v0.17.1...v0.18.0)
  * 2025-06-16 - Add helper to display logs from systemd service
  * 2025-06-16 - Update requirements
* [v0.17.1](https://github.com/jedie/cli-base-utilities/compare/v0.17.0...v0.17.1)
  * 2025-06-02 - Update requirements
  * 2025-06-02 - Execute "pre-commit autoupdate" only if "pre-commit" is installed

<details><summary>Expand older history entries ...</summary>

* [v0.17.0](https://github.com/jedie/cli-base-utilities/compare/v0.16.0...v0.17.0)
  * 2025-02-12 - migrate from tox to nox
* [v0.16.0](https://github.com/jedie/cli-base-utilities/compare/v0.15.1...v0.16.0)
  * 2025-01-17 - +lookup_python_tool()
* [v0.15.1](https://github.com/jedie/cli-base-utilities/compare/v0.15.0...v0.15.1)
  * 2025-01-17 - Remove pip-tools work-a-round and update requirements
* [v0.15.0](https://github.com/jedie/cli-base-utilities/compare/v0.14.0...v0.15.0)
  * 2024-12-03 - Restructure cli test utils
  * 2024-12-03 - Remove tyro work-a-round
* [v0.14.0](https://github.com/jedie/cli-base-utilities/compare/v0.13.1...v0.14.0)
  * 2024-11-21 - Use tyro.extras.SubcommandApp()
  * 2024-11-21 - Update "install" command and use uv
  * 2024-11-21 - Switch from pip-tools to uv
* [v0.13.1](https://github.com/jedie/cli-base-utilities/compare/v0.13.0...v0.13.1)
  * 2024-09-26 - Bugfix missing click. Add it for Backward compatibility
* [v0.13.0](https://github.com/jedie/cli-base-utilities/compare/v0.12.0...v0.13.0)
  * 2024-09-26 - Add Helper for tyro and replace click with tyro in own CLIs
* [v0.12.0](https://github.com/jedie/cli-base-utilities/compare/v0.11.0...v0.12.0)
  * 2024-09-25 - Add debug log to update_readme_history call
  * 2024-09-25 - Simplify AssertCliHelpInReadme to a flat function
  * 2024-09-25 - Apply manage projects updates
  * 2024-09-25 - Update requirements
* [v0.11.0](https://github.com/jedie/cli-base-utilities/compare/v0.10.3...v0.11.0)
  * 2024-08-30 - Apply manageprojects updates, e.g.: Set min. Python to 3.11+
  * 2024-08-30 - NEW: EncloseRuleContext
* [v0.10.3](https://github.com/jedie/cli-base-utilities/compare/v0.10.2...v0.10.3)
  * 2024-08-05 - Bugfix unchanable boolean flags in toml settings
* [v0.10.2](https://github.com/jedie/cli-base-utilities/compare/v0.10.1...v0.10.2)
  * 2024-08-04 - Auto activate pre commit hooks
  * 2024-08-04 - Update demo CLI: Always update pip and pip-tools
  * 2024-08-04 - Handle KeyboardInterrupt in cli scripts.
  * 2024-08-04 - Bugfix #50 toml2dataclass(): AttributeError: 'bool' object has no attribute 'unwrap'.
  * 2024-08-02 - Fix doc link in README.md
* [v0.10.1](https://github.com/jedie/cli-base-utilities/compare/v0.10.0...v0.10.1)
  * 2024-08-02 - Increase default timout from 5 to 15 minutes
  * 2024-08-02 - Update pre-commit hook version to cli-base-utilities v0.10.0
* [v0.10.0](https://github.com/jedie/cli-base-utilities/compare/v0.9.0...v0.10.0)
  * 2024-08-02 - Use dateutil in get_commit_date()
  * 2024-08-02 - Replace "safety" by "pip-audit" and add tooling for it.
  * 2024-08-01 - Update manageprojects updates
* [v0.9.0](https://github.com/jedie/cli-base-utilities/compare/v0.8.0...v0.9.0)
  * 2024-07-16 - Update project
* [v0.8.0](https://github.com/jedie/cli-base-utilities/compare/v0.7.0...v0.8.0)
  * 2024-03-12 - Bugfix publish
  * 2024-03-12 - fix tests
  * 2024-03-12 - Split app/dev CLI into a package with autodiscovery
  * 2024-03-12 - Move click defaults
  * 2024-03-12 - Apply cookiecutter template updates
  * 2024-03-12 - Update requirements
  * 2024-01-16 - Use typeguard in tests
  * 2024-01-16 - manageprojects updates
  * 2024-01-16 - Update requirements + datetimes ;)
  * 2023-12-17 - Bugfix .pre-commit-config.yaml
* [v0.7.0](https://github.com/jedie/cli-base-utilities/compare/v0.6.0...v0.7.0)
  * 2023-12-16 - Add "Update pre-commit hooks" to README
  * 2023-12-16 - Bugfix update_readme_history(): Use `__version__` from module
  * 2023-12-16 - NEW: "update-readme-history" git hook using "pre-commit"
  * 2023-12-16 - fix tests
  * 2023-12-16 - Bugfix type hints
  * 2023-12-16 - Add update-readme-history to app CLI
  * 2023-12-16 - Move DEMO into `./cli_base/demo/`
  * 2023-12-16 - Simplify App CLI
  * 2023-12-16 - Remove PACKAGE_ROOT from app CLI
  * 2023-12-16 - Update requirements
  * 2023-12-16 - Skip test_readme_history() on CI
* [v0.6.0](https://github.com/jedie/cli-base-utilities/compare/v0.5.0...v0.6.0)
  * 2023-12-02 - NEW: Code style tools
* [v0.5.0](https://github.com/jedie/cli-base-utilities/compare/v0.4.5...v0.5.0)
  * 2023-12-01 - fix flake8
  * 2023-12-01 - NEW: test utils: AssertLogs() context manager
  * 2023-12-01 - Bugfix expand_user() if SUDO_USER is the same as current user
  * 2023-12-01 - Add "run_coverage()" to "dev_tools" and polish tox, unittest, too.
  * 2023-12-01 - add tests for EraseCoverageData()
  * 2023-12-01 - Apply manageprojects updates
* [v0.4.5](https://github.com/jedie/cli-base-utilities/compare/v0.4.4...v0.4.5)
  * 2023-11-30 - Configure unittests via "load_tests Protocol" hook
  * 2023-11-30 - Update requirements and add "flake8-bugbear"
  * 2023-11-30 - Remove function calls in function agruments
* [v0.4.4](https://github.com/jedie/cli-base-utilities/compare/v0.4.3...v0.4.4)
  * 2023-11-01 - Bugfix "AssertionError: Expected only one line" in Git.first_commit_info()
* [v0.4.3](https://github.com/jedie/cli-base-utilities/compare/v0.4.2...v0.4.3)
  * 2023-11-01 - Git history renderer: Collapse older entries
* [v0.4.2](https://github.com/jedie/cli-base-utilities/compare/v0.4.1...v0.4.2)
  * 2023-11-01 - Remove duplicate git commits and keep only test last one, e.g.: "update requirements"
  * 2023-11-01 - Bugfix git history: Add commits before the first tag
* [v0.4.1](https://github.com/jedie/cli-base-utilities/compare/v0.4.0...v0.4.1)
  * 2023-10-08 - Remove commit URLs from history and handle release a new version
  * 2023-10-08 - NEW: Generate a project history base on git commits/tags.
  * 2023-10-08 - Update requirements
  * 2023-09-26 - Update README.md
* [v0.4.0](https://github.com/jedie/cli-base-utilities/compare/v0.3.0...v0.4.0)
  * 2023-09-24 - fix tests
  * 2023-09-24 - Add UpdateTestSnapshotFiles() Context Manager
  * 2023-09-24 - coverage: Refactor setup and add helpers
  * 2023-09-24 - Update requirements
* [v0.3.0](https://github.com/jedie/cli-base-utilities/compare/v0.2.0...v0.3.0)
  * 2023-08-17 - Bugfix tests run in terminal
  * 2023-08-17 - update requirements
  * 2023-08-17 - NEW: cli_base.cli_tools.git and cli_base.cli_tools.version_info
* [v0.2.0](https://github.com/jedie/cli-base-utilities/compare/d89f23b...v0.2.0)
  * 2023-08-09 - Project setup updates
  * 2023-05-22 - Update README.md
  * 2023-05-22 - Rename project "cli-base" to "cli-base-utilities"
  * 2023-05-22 - Add github CI config
  * 2023-05-22 - Add subprocess_utils from manageprojects
  * 2023-05-21 - init

</details>


[comment]: <> (✂✂✂ auto generated history end ✂✂✂)
