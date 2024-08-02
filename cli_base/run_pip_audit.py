"""
    DocWrite: pip_audit.md # Helper to run pip-audit
    https://github.com/pypa/pip-audit
"""

from __future__ import annotations

import logging
from pathlib import Path

from bx_py_utils.pyproject_toml import get_pyproject_config

from cli_base.cli_tools.subprocess_utils import verbose_check_call
from cli_base.cli_tools.verbosity import setup_logging


logger = logging.getLogger(__name__)


def run_pip_audit(base_path: Path | None = None, verbosity: int = 1):
    """DocWrite: pip_audit.md ## cli_base.run_pip_audit.run_pip_audit()
    Call `run_pip_audit()` to run `pip-audit` with configuration from `pyproject.toml`.

    pyproject.toml example:

        [tool.cli_base.pip_audit]
        requirements=["requirements.dev.txt"]
        strict=true
        require_hashes=true
        ignore-vuln=[
            "CVE-2019-8341", # Jinja2: Side Template Injection (SSTI)
        ]
    """
    setup_logging(verbosity=verbosity)

    config: dict = get_pyproject_config(
        section=('tool', 'cli_base', 'pip_audit'),
        base_path=base_path,
    )
    logger.debug('pip_audit config: %r', config)
    assert isinstance(config, dict), f'Expected a dict: {config=}'

    popenargs = ['pip-audit']

    if verbosity:
        popenargs.append(f'-{"v" * verbosity}')

    if config.get('strict'):
        popenargs.append('--strict')

    if config.get('require_hashes'):
        popenargs.append('--require-hashes')

    for requirement in config.get('requirements', []):
        popenargs.extend(['-r', requirement])

    for vulnerability_id in config.get('ignore-vuln', []):
        popenargs.extend(['--ignore-vuln', vulnerability_id])

    logger.debug('pip_audit args: %s', popenargs)
    verbose_check_call(*popenargs)
