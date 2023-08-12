#!/usr/bin/env python

import argparse
from pathlib import Path

import nbformat

from nbisort import nbisort


def format_notebook(notebook: Path) -> None:
    if notebook.suffix != ".ipynb":
        return

    with open(notebook) as f:
        nb = nbformat.read(f, as_version=4)

    nb = nbisort(nb)

    with open(notebook, "w") as f:
        nbformat.write(nb, f)


def format_path(path: Path) -> None:
    if path.is_file():
        format_notebook(path)
    else:
        for subpath in path.iterdir():
            format_path(subpath)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("notebook", type=Path, nargs="?")

    args = parser.parse_args()

    path: Path = args.notebook or Path.cwd()
    format_path(path)


if __name__ == "__main__":
    main()
