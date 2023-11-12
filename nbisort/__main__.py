import argparse
from functools import wraps
from pathlib import Path

import nbformat

from nbisort import nbisort


@wraps(print)
def _print_if_verbose(*args, verbose: bool = False, **kwargs):
    if verbose:
        print(*args, **kwargs)


def format_notebook(notebook: Path, verbose: bool = False) -> None:
    if notebook.suffix != ".ipynb":
        _print_if_verbose(f"Skipping {notebook}", verbose=verbose)
        return

    with open(notebook, encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    _print_if_verbose(f"Formatting {notebook}...", verbose=verbose)

    nb = nbisort(nb)

    with open(notebook, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)


def format_path(path: Path, verbose: bool = False) -> None:
    if path.is_file():
        format_notebook(path, verbose=verbose)
    else:
        for subpath in path.iterdir():
            format_path(subpath, verbose=verbose)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("notebook", type=Path, nargs="?")
    parser.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args()

    path: Path = args.notebook or Path.cwd()
    format_path(path, verbose=args.verbose)


if __name__ == "__main__":
    main()
