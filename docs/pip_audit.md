# Helper to run pip-audit

https://github.com/pypa/pip-audit

## cli_base.run_pip_audit.run_pip_audit()

Call `run_pip_audit()` to run `pip-audit` with configuration from `pyproject.toml`.

pyproject.toml example:

    [tool.cli_base.pip_audit]
    requirements=["requirements.dev.txt"]
    strict=true
    require_hashes=true
    ignore-vuln=[
        "CVE-2019-8341", # Jinja2: Side Template Injection (SSTI)
    ]