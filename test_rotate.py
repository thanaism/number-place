import pytest
from grid import Grid


@pytest.fixture
def grid_creation():
    grid = Grid()
    grid.create()
    yield grid
    print('--yield behavior test')


def test_rotate(grid_creation):
    """"Test for rotate function in class Grid"""
    grid = grid_creation
    grids = grid.rotate(grid.grid)
    for i, j in enumerate(grids):
        print(i)
        grid.show_grid(j)


if __name__ == '__main__':
    parameter = '-v'  # 's' to print to console.
    pytest.main([parameter, __file__])
