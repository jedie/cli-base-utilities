# Helper to run pip-audit

https://github.com/pypa/pip-audit

## cli_base.run_pip_audit.run_pip_audit()

Call `run_pip_audit()` to run `pip-audit` with configuration from `pyproject.toml`.

It used `uv export` to generate a temporary `requirements.txt` file
and pass it to `pip-audit` for checking vulnerabilities.

pyproject.toml example:

    [tool.cli_base.pip_audit]
    requirements=["requirements.dev.txt"]
    options=["--strict", "--require-hashes", "--disable-pip"]
    ignore-vuln=[
        "CVE-2019-8341", # Jinja2: Side Template Injection (SSTI)
    ]