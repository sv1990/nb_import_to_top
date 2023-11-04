from __future__ import annotations

import re
from copy import deepcopy
from pathlib import Path

import isort
import more_itertools
import nbformat

IMPORT_RGX = re.compile(
    r"^(from\s+\w+(?:\.\w+)*\s+import\s+(?:\w+|\((?:[^\)]|\n)*\)).*|import\s+.*)",
    flags=re.MULTILINE,
)


def run_isort(code: str) -> str:
    return isort.code(
        code, config=isort.Config(settings_path=str(Path.cwd().resolve()))
    )


def is_import(s: str | None) -> bool:
    return bool(IMPORT_RGX.match(s)) if s else False


def nbisort(nb: nbformat.NotebookNode) -> nbformat.NotebookNode:
    nb_copy = deepcopy(nb)

    all_imports = set()
    for i, cell in enumerate(nb["cells"]):
        if cell["cell_type"] != "code":
            continue
        source = cell["source"]
        code, imports = more_itertools.partition(is_import, IMPORT_RGX.split(source))
        all_imports |= set(imports)
        new_source = "".join(filter(bool, code))

        # Set source to None if it was emptied by moving the imports so that it can be
        # removed later.
        nb_copy["cells"][i]["source"] = (
            new_source if new_source.strip() or not source.strip() else None
        )

    nb_copy["cells"] = [
        cell for cell in nb_copy["cells"] if getattr(cell, "source", None) is not None
    ]

    nb_copy["cells"].insert(
        0, nbformat.v4.new_code_cell(run_isort("\n".join(sorted(all_imports))))
    )

    return nb_copy
