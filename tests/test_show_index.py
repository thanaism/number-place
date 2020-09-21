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


def test_show_index(grid_creation):
    grid = grid_creation
    print('\n')
    grid.show_index()


if __name__ == '__main__':
    parameter = '-sv'  # 's' to print to console.
    pytest.main([parameter, __file__])
