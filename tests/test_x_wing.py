import os
import sys
import pytest
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def grid_creation():
    from src.grid import Grid
    grid = Grid()
    yield grid


@pytest.mark.parametrize('rm, targets, eliminated', [
    # (5, 0, [9, 10, 11, 19], [1, 2, 9, 10, 11, 19, 12, 13, 21, 15, 17, 25]),
    # (5, 4, [3, 5, 21], [3, 21, 13, 22, 5, 30, 32, 57, 59]),
    (1, [9, 13, 36, 40, 12, 15, 16, 17, 38, 39, 42, 43, 44]\
        + [2, 3, 21, 24, 25, 29, 30, 34, 35, 48, 52, 51, 69, 70],
     [12, 15, 16, 17, 38, 39, 42, 43, 44]),
    (5, [13, 16, 40, 43, 31], [31])
])
def test_x_wing(rm, targets, eliminated, grid_creation):
    grid = grid_creation
    for i in range(81):
        grid.cells[i].remove(rm)
        # print(f'{grid.cells[i].candidates:09b}')
    for i in targets:
        grid.cells[i].add(rm)
    print('\n')
    grid.x_wing()
    grid.show_only_input_index(*targets)
    for i in eliminated:
        # print(i, f'{grid.cells[i].candidates:09b}')
        assert grid.cells[i].has(rm) is False
    # for i in targets:
    #     if grid.cells[i].has(rm):
    #         print(f'{i} has {rm}')


if __name__ == '__main__':
    parameter = '-sv'  # 's' to print to console.
    pytest.main([parameter, __file__])
