#!/usr/bin/env python

import argparse
from pathlib import Path
from shutil import copyfile

import nbformat

from nbisort import move_imports_to_top


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("notebook", type=Path)

    args = parser.parse_args()

    with open(args.notebook) as f:
        nb = nbformat.read(f, as_version=4)

    copyfile(args.notebook, args.notebook.with_suffix(f"{args.notebook.suffix}.bak"))

    nb = move_imports_to_top(nb)

    with open(args.notebook, "w") as f:
        nbformat.write(nb, f)


if __name__ == "__main__":
    main()
