def assert_in(content: str, parts: tuple[str, ...], strip_ansi=True) -> None:
    """
    Check if all parts exist in content
    """
    if strip_ansi:
        from cli_base.cli_tools.test_utils.rich_test_utils import strip_ansi_codes  # import loop

        content = strip_ansi_codes(content)

    missing = [part for part in parts if part not in content]
    if missing:
        missing = '\n\n'.join(missing)
        error_message = (
            f'\nassert_in(): {len(missing)} parts not found in content:\n'
            '∨∨∨∨∨∨∨∨∨∨∨∨ [Content start] ∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨\n'
            f'{content}\n'
            '∧∧∧∧∧∧∧∧∧∧∧∧ [Content end] ∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧\n'
            f'Missing parts are:\n'
            f'{missing}\n'
            '======================================================================================================\n\n'
        )
        raise AssertionError(error_message)


def assert_startswith(text, prefix):
    if not text.startswith(prefix):
        raise AssertionError(f'{prefix=!r} is not at the beginning of: {text!r}')
