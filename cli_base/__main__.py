"""
    Allow cli_base to be executable
    through `python -m cli_base`.
"""


from cli_base.cli_app import main


if __name__ == '__main__':
    main()
