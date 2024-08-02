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

* [`run_pip_audit()` to run `pip-audit` with configuration from `pyproject.toml`](https://github.com/boxine/bx_py_utils/blob/master/docs/pip_audit.md)

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
Usage: ./dev-cli.py [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ check-code-style            Check code style by calling darker + flake8                          │
│ coverage                    Run tests and show coverage report.                                  │
│ fix-code-style              Fix code style of all cli_base source code files via darker          │
│ install                     Run pip-sync and install 'cli_base' via pip as editable.             │
│ mypy                        Run Mypy (configured in pyproject.toml)                              │
│ pip-audit                   Run pip-audit check against current requirements files               │
│ publish                     Build and upload this project to PyPi                                │
│ test                        Run unittests                                                        │
│ tox                         Run tox                                                              │
│ update                      Update "requirements*.txt" dependencies files                        │
│ update-test-snapshot-files  Update all test snapshot files (by remove and recreate all snapshot  │
│                             files)                                                               │
│ version                     Print version and exit                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated dev help end ✂✂✂)


# app CLI

[comment]: <> (✂✂✂ auto generated app help start ✂✂✂)
```
Usage: ./cli.py [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ update-readme-history      Update project history base on git commits/tags in README.md          │
│ version                    Print version and exit                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated app help end ✂✂✂)


# DEMO app CLI

[comment]: <> (✂✂✂ auto generated demo help start ✂✂✂)
```
Usage: ./cli.py [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ demo-endless-loop                Just a useless example command, used in systemd DEMO: It just   │
│                                  print some information in a endless loop.                       │
│ demo-verbose-check-output-error  DEMO for a error calling                                        │
│                                  cli_base.cli_tools.subprocess_utils.verbose_check_output()      │
│ edit-settings                    Edit the settings file. On first call: Create the default one.  │
│ print-settings                   Display (anonymized) MQTT server username and password          │
│ systemd-debug                    Print Systemd service template + context + rendered file        │
│                                  content.                                                        │
│ systemd-remove                   Write Systemd service file, enable it and (re-)start the        │
│                                  service. (May need sudo)                                        │
│ systemd-setup                    Write Systemd service file, enable it and (re-)start the        │
│                                  service. (May need sudo)                                        │
│ systemd-status                   Display status of systemd service. (May need sudo)              │
│ systemd-stop                     Stops the systemd service. (May need sudo)                      │
│ version                          Print version and exit                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
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


# history

[comment]: <> (✂✂✂ auto generated history start ✂✂✂)

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

<details><summary>Expand older history entries ...</summary>

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
