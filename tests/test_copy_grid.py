import os
import sys
import pytest
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def grid_creation():
    from src.grid import Grid
    grid = Grid()
    return grid


def test_copy_grid(grid_creation):
    grid = grid_creation
    copied_grid = grid.copy_grid()
    for i in range(9, 18):
        grid.cells[i].remove(9)
        copied_grid.cells[i].remove(3)
    grid.cells[12].add(9)
    copied_grid.cells[16].add(3)
    for i in range(9, 18):
        if i != 12:
            assert grid.cells[i].candidates == 0b011111111
        else:
            assert grid.cells[i].candidates == 0b111111111
    grid.hidden_single()
    copied_grid.hidden_single()
    assert grid.cells[12].digit == 9
    assert copied_grid.cells[16].digit == 3
    print()
    grid.show_grid()
    copied_grid.show_grid()


if __name__ == '__main__':
    parameter = '-sv'  # 's' to print to console.
    pytest.main([parameter, __file__])
