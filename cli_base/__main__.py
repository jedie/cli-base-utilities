"""
    Allow cli_base to be executable
    through `python -m cli_base`.
"""


from cli_base.cli import cli_app


def main():
    cli_app.main()


if __name__ == '__main__':
    main()
