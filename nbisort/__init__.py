import re
from copy import deepcopy
from pathlib import Path

import more_itertools
import nbformat

IMPORT_RGX: re.Pattern = re.compile(
    r"^(from\s+\w+\s+import\s+(?:\w+|\((?:[^\)]|\n)*\)).*|import\s+.*)", flags=re.M
)


def try_run_isort(code: str) -> str:
    try:
        # pylint:disable-next = import-outside-toplevel
        from isort import Config

        # pylint:disable-next = import-outside-toplevel
        from isort.api import sort_code_string
    except ImportError:
        return code
    return sort_code_string(
        code, config=Config(settings_path=str(Path.cwd().resolve()))
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
        0, nbformat.v4.new_code_cell(try_run_isort("\n".join(sorted(all_imports))))
    )

    return nb_copy
