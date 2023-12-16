"""
    Allow cli_base to be executable
    through `python -m cli_base.demo`.
"""

from cli_base.demo.cli import main


if __name__ == '__main__':
    main()
