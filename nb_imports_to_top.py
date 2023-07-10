#!/usr/bin/env python

import argparse
import re
from copy import deepcopy
from pathlib import Path
from shutil import copyfile

import more_itertools
import nbformat

IMPORT_RGX: re.Pattern = re.compile(
    r"^(from\s+\w+\s+import\s+(?:\w+|\((?:[^\)]|\n)*\)).*|import\s+.*)", flags=re.M
)


def move_imports_to_top(nb: nbformat.NotebookNode) -> nbformat.NotebookNode:
    nb_copy = deepcopy(nb)

    all_imports = set()
    for i, cell in enumerate(nb["cells"]):
        if cell["cell_type"] != "code":
            continue
        source = cell["source"]
        code, imports = more_itertools.partition(
            IMPORT_RGX.match, IMPORT_RGX.split(source)
        )
        all_imports |= set(imports)
        new_source = "".join(code)

        # Set source to None if it was emptied by moving the imports so that it can be
        # removed later.
        nb_copy["cells"][i]["source"] = (
            new_source if new_source.strip() or not source else None
        )

    nb_copy["cells"] = [cell for cell in nb_copy["cells"] if cell.source is not None]

    nb_copy["cells"].insert(
        0,
        nbformat.v4.new_code_cell(
            "\n".join(sorted(all_imports)),  # TODO: apply isort if available
        ),
    )

    return nb_copy


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
