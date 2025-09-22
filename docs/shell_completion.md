# Tyro CLI Shell Completion

Helper to setup shell completion for a Tyro based CLI program.

Currently only bash shell is supported.
Usage: Expand you Tyro CLI and call `setup_tyro_shell_completion()` from your program ;)

## fix_completion_prog()

When Tyro writes completion file, use the full path to the CLI program.
So that the completion match only for this program.
e.g.: Usage of more than one "./cli.py" in different folders ;)

So build your app like this:
```python
app.cli(
    prog=fix_completion_prog('./cli.py'),
    ...
)
```