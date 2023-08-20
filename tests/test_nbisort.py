from typing import Iterable

import nbformat
import pytest
from more_itertools import zip_equal

from nbisort import is_import, nbisort


@pytest.mark.parametrize(
    "code, expected",
    [
        ("import foo", True),
        ("    import foo", False),
        ("import foo as f", True),
        ("", False),
        ("[x for x in xs]", False),
        ("from os.path import abspath", True),
        ("from itertools import permutations, combinations", True),
        ("from module import func, (ClassA, ClassB)", True),
        ("import my_package.my_module", True),
        ("import my_package.my_module.my_submodule", True),
        ("from module import (\n    func1,\n    func2,\n    func3,\n)", True),
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
        ),
        (
            to_notebook(
                [
                    cell("import a\n"),
                    cell("import b\n"),
                ]
            ),
            to_notebook(
                [
                    cell("import a\nimport b\n"),
                ]
            ),
        ),
        (
            to_notebook(
                [
                    cell("import a\n"),
                    cell("\n\n"),
                    cell("import b\n"),
                ]
            ),
            to_notebook(
                [
                    cell("import a\nimport b\n"),
                    cell("\n\n"),
                ]
            ),
        ),
        (
            to_notebook(
                [
                    cell("from mod1 import f1"),
                    cell("from mod2.submod1 import f2, f3"),
                ]
            ),
            to_notebook(
                [
                    cell("from mod1 import f1\nfrom mod2.submod1 import f2, f3\n"),
                ]
            ),
        ),
        (
            to_notebook(
                [
                    cell("import a\n"),
                    markdown("import a"),
                    cell("import b\n"),
                ]
            ),
            to_notebook(
                [
                    cell("import a\nimport b\n"),
                    markdown("import a"),
                ]
            ),
        ),
    ],
)
def test_move_imports(nb, expected_nb):
    result_nb = nbisort(nb)

    for cell1, cell2 in zip_equal(result_nb["cells"], expected_nb["cells"]):
        cell1.pop("id")
        cell2.pop("id")
        assert cell1 == cell2
