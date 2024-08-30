import inspect
from unittest import TestCase

from cli_base.cli_tools.rich_utils import EncloseRuleContext
from cli_base.cli_tools.test_utils.rich_test_utils import get_fixed_console


class RichUtilsTestCase(TestCase):
    maxDiff = None

    def test_enclose_rule_context_as_context_manager(self):
        console = get_fixed_console(width=50)

        with EncloseRuleContext('Usage as context manager', console=console):
            console.print('Hello, World inside context manager!')
        self.assertEqual(
            console.file.getvalue().strip(),
            inspect.cleandoc(
                '''
                ──────────── Usage as context manager ────────────
                Hello, World inside context manager!
                ──────────────────────────────────────────────────
                '''
            ),
        )

    def test_enclose_context_as_decorator(self):
        console = get_fixed_console(width=50)

        @EncloseRuleContext('Usage as decorator', console=console)
        def use_as_decorator():
            console.print('Hello, World inside decorator!')

        use_as_decorator()

        self.assertEqual(
            console.file.getvalue().strip(),
            inspect.cleandoc(
                '''
                ─────────────── Usage as decorator ───────────────
                Hello, World inside decorator!
                ──────────────────────────────────────────────────
                '''
            ),
        )
