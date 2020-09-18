import os
import sys
import pytest
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def grid_creation():
    from src.grid import Grid
    grid = Grid()
    for i in range(9, 18):
        grid.cells[i].remove(9)
    grid.cells[12].add(9)
    for i in range(9, 18):
        if i != 12:
            assert grid.cells[i].candidates == 0b011111111
        else:
            assert grid.cells[i].candidates == 0b111111111
    yield grid
    print()
    grid.show_grid()


def test_hidden_single(grid_creation):
    grid = grid_creation
    grid.hidden_single()
    assert grid.cells[12].digit == 9


if __name__ == '__main__':
    parameter = '-sv'  # 's' to print to console.
    pytest.main([parameter, __file__])
