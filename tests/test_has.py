import os
import sys
import pytest
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def cell_creation():
    from src.cell import Cell
    cell = Cell(0, 0)
    cell.remove(6, 7, 8)
    return cell


params = {
    'digits mixed;AND': ((1, 2, 3, 4, 5, 6, 7, 8, 9), {}, False),
    'digits mixed;OR': ((1, 2, 3, 4, 5, 6, 7, 8, 9), {'AND': False}, True),
    'all digits included;AND': ((1, 2, 3, 4, 5, 9), {}, True),
    'single digit included': ((1,), {}, True),
    'single digit not included': ((8,), {}, False)
}


@pytest.mark.parametrize('digits,AND,expected',
                         [*params.values()], ids=[*params.keys()])
def test_has(digits, AND, expected, cell_creation):
    """"Cellクラスのhas関数のテスト"""
    assert cell_creation.has(*digits, **AND) == expected


if __name__ == '__main__':
    pytest.main(['-v', __file__])
