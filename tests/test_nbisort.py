import pytest

from nbisort import IMPORT_RGX


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
    assert bool(IMPORT_RGX.match(code)) == expected
