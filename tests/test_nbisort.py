from typing import Iterable

import nbformat
import pytest

from nbisort import is_import, move_imports_to_top


@pytest.mark.parametrize(
    "code, expected",
    [
        ("import foo", True),
        ("    import foo", False),
        ("import foo as f", True),
        ("", False),
        ("[x for x in xs]", False),
        ("from os.path import abspath", True),
    ],
)
def test_is_import(code, expected):
    assert is_import(code) == expected


def cell(text: str) -> nbformat.NotebookNode:
    return nbformat.v4.new_code_cell(text)


def markdown(text: str) -> nbformat.NotebookNode:
    return nbformat.v4.new_markdown_cell(text)


def to_notebook(cells: Iterable[nbformat.NotebookNode]):
    nb = nbformat.v4.new_notebook()
    nb["cells"] = list(cells)
    return nb


@pytest.mark.parametrize(
    "nb, expected_nb",
    [
        (
            to_notebook(
                [
                    cell("import os\nimport sys\nprint('Hello, world!')"),
                    cell("# Some code here"),
                    cell("from math import sqrt\nimport numpy as np"),
                ]
            ),
            to_notebook(
                [
                    cell(
                        "import os\nimport sys\nfrom math import sqrt\n\nimport numpy as np\n"
                    ),
                    cell("\n\nprint('Hello, world!')"),
                    cell("# Some code here"),
                ]
            ),
        )
    ],
)
def test_move_imports(nb, expected_nb):
    result_nb = move_imports_to_top(nb)

    for cell1, cell2 in zip(result_nb["cells"], expected_nb["cells"]):
        cell1.pop("id")
        cell2.pop("id")
        assert cell1 == cell2
