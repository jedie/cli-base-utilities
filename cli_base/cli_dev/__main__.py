"""
    Allow cli_base to be executable
    through `python -m cli_base.cli_dev`.
"""

from cli_base.cli_dev import main


if __name__ == '__main__':
    main()
