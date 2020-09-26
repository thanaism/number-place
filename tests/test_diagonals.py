import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def grid_creation():
    from src.grid import Grid

    grid = Grid(np_type=1)
    return grid


def test_show_index(grid_creation):
    grid = grid_creation
    print('\n')
    grid.create
    for i, v in enumerate(grid.peers):
        print(i, len(v), v)
        if any([i % 10 == 0, i % 8 == 0]):
            if i == 40:
                assert len(v) == 9 + 6 * 4
            else:
                assert len(v) == 9 + 6 * 3
        else:
            assert len(v) == 9 + 6 * 2
    for i, v in enumerate(grid.houses):
        print(i, v)
    grid.create()
    for diagonal in grid.diagonals:
        assert [*range(1, 10)] == sorted([grid.cells[i].digit for i in diagonal])
        print(sorted([grid.cells[i].digit for i in diagonal]))
    grid.show_grid()


if __name__ == '__main__':
    parameter = '-sv'  # 's' to print to console.
    pytest.main([parameter, __file__])
