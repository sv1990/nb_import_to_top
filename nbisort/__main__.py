#!/usr/bin/env python

import argparse
from pathlib import Path

import nbformat

from nbisort import nbisort


def format_notebook(notebook: Path, verbose: bool = False) -> None:
    if notebook.suffix != ".ipynb":
        return

    with open(notebook) as f:
        nb = nbformat.read(f, as_version=4)

    if verbose:
        print(f"Formatting {notebook}...")

    nb = nbisort(nb)

    with open(notebook, "w") as f:
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
