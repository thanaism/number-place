import pytest
from cell import Cell


@pytest.fixture
def cell_creation():
    cell = Cell(0, 0)
    cell.remove(6, 7, 8)
    return cell


@pytest.mark.parametrize('digits,AND,expected', [
    ((1, 2, 3, 4, 5, 6, 7, 8, 9), {}, False),
    ((1, 2, 3, 4, 5, 6, 7, 8, 9), {'AND': False}, True),
    ((1, 2, 3, 4, 5, 9), {}, True),
    ((1,), {}, True),
    ((8,), {}, False)
])
def test_has(digits, AND, expected, cell_creation):
    """"Cellクラスのhas関数のテスト"""
    assert cell_creation.has(*digits, **AND) == expected


if __name__ == '__main__':
    pytest.main(['-v', __file__])
