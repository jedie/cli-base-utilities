# cli-base-utilities

[![tests](https://github.com/jedie/cli-base-utilities/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/jedie/cli-base-utilities/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/cli-base-utilities/branch/main/graph/badge.svg)](https://app.codecov.io/github/jedie/cli-base-utilities)
[![cli-base-utilities @ PyPi](https://img.shields.io/pypi/v/cli-base-utilities?label=cli-base-utilities%20%40%20PyPi)](https://pypi.org/project/cli-base-utilities/)
[![Python Versions](https://img.shields.io/pypi/pyversions/cli-base-utilities)](https://github.com/jedie/cli-base-utilities/blob/main/pyproject.toml)
[![License GPL-3.0-or-later](https://img.shields.io/pypi/l/cli-base-utilities)](https://github.com/jedie/cli-base-utilities/blob/main/LICENSE)

Helpers to bild a CLI program

* https://pypi.org/project/cli-base-utilities/


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
│ coverage                    Run and show coverage.                                               │
│ fix-code-style              Fix code style of all cli_base source code files via darker          │
│ install                     Run pip-sync and install 'cli_base' via pip as editable.             │
│ mypy                        Run Mypy (configured in pyproject.toml)                              │
│ publish                     Build and upload this project to PyPi                                │
│ safety                      Run safety check against current requirements files                  │
│ test                        Run unittests                                                        │
│ tox                         Run tox                                                              │
│ update                      Update "requirements*.txt" dependencies files                        │
│ update-test-snapshot-files  Update all test snapshot files (by remove and recreate all snapshot  │
│                             files)                                                               │
│ version                     Print version and exit                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated dev help end ✂✂✂)


# DEMO app CLI

[comment]: <> (✂✂✂ auto generated app help start ✂✂✂)
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
[comment]: <> (✂✂✂ auto generated app help end ✂✂✂)
