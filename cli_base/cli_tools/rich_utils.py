from __future__ import annotations

import sys

from bx_py_utils.test_utils.assertion import text_unified_diff
from pygments.lexer import Lexer
from rich.console import Console
from rich.highlighter import ReprHighlighter
from rich.panel import Panel
from rich.pretty import Pretty
from rich.syntax import Syntax
from rich.text import Text


def print_code(
    code: str,
    *,
    title: str | None = None,
    lexer: Lexer | str,
    theme: str = 'ansi_dark',
    background_color: str = '#090909',
    line_numbers: bool = True,
    console: Console | None = None,
) -> None:
    """
    Print source code via Pygments
    """
    console = console or Console()

    console.print()
    console.rule(title)
    console.print(
        Syntax(
            code,
            lexer,
            theme=theme,
            background_color=background_color,
            line_numbers=line_numbers,
        )
    )
    console.rule()
    console.print()


def print_unified_diff(
    txt1: str,
    txt2: str,
    *,
    fromfile: str = 'got',
    tofile: str = 'expected',
    title: str = '[bright][green]unified diff[/green]:',
    console: Console | None = None,
) -> None:
    """
    Print a diff highlight with Pygments
    """
    diff = text_unified_diff(
        txt1=txt1,
        txt2=txt2,
        fromfile=fromfile,
        tofile=tofile,
    )
    print_code(code=diff, lexer='diff', title=title, console=console)


class PanelPrinter:
    def __init__(
        self,
        *,
        HighlighterClass=ReprHighlighter,
        border_style='bright_yellow',
        padding=(2, 5),
        console=None,
    ):
        if HighlighterClass is not None:
            self.highlighter = HighlighterClass()
        else:
            self.highlighter = None

        self.HighlighterClass = HighlighterClass
        self.border_style = border_style
        self.padding = padding
        self.console = console or Console()
        self.console.print()

    def print_panel(self, *, content, title, border_style=None):
        self.console.print(
            Panel(
                self.highlight(content),
                title=title,
                border_style=border_style or self.border_style,
                expand=False,
                padding=self.padding,
            )
        )
        self.console.print()

    def highlight(self, content):
        if not isinstance(content, (str, Text)):
            content = Pretty(content)
        elif self.highlighter:
            content = self.highlighter(content)
        return content


def human_error(
    message: str,
    *,
    title='[red]Error',
    exit_code=None,
    exception: BaseException | None = None,
    exception_extra_lines: int = 2,
    exception_max_frames: int = 20,
    HighlighterClass=ReprHighlighter,
    border_style='bright_red',
    padding=(2, 5),
    console=None,
):
    """
    Print a message in a Panel.
    Optional:
        - print traceback first
        - Exit with: sys.exit(exit_code)
    """
    if console is None:
        use_stderr = exception is not None
        console = Console(stderr=use_stderr)

    console.print('\n')

    if exception is not None:
        assert isinstance(exception, BaseException), f'Not a exception: {exception!r}'
        console.print_exception(
            width=console.size.width,  # full terminal width
            extra_lines=exception_extra_lines,
            show_locals=True,
            max_frames=exception_max_frames,
        )

    console.print()

    pp = PanelPrinter(HighlighterClass=HighlighterClass, border_style=border_style, padding=padding, console=console)
    pp.print_panel(content=message, title=title)

    if exit_code is not None:
        sys.exit(exit_code)
