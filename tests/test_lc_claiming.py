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


@pytest.mark.parametrize('rm, chute, targets, digits', [
    (5, 0, [9, 10, 11, 19], [1, 2, 9, 10, 11, 19, 12, 13, 21, 15, 17, 25]),
    (5, 4, [3, 5, 21], [3, 21, 13, 22, 5, 30, 32, 57, 59]),
    (5, 2, [60], [60, 78, 54, 55, 66, 68]),
    (5, 1, [30, 32, 49], [30, 32, 40, 49, 33, 34, 45, 47])
])
def test_lc_claiming(rm, chute, targets, digits, grid_creation):
    grid = grid_creation
    for i in grid.chutes[chute]:
        grid.cells[i].remove(rm)
    for i in digits:
        grid.cells[i].add(rm)
    print('\n')
    grid.lc_claiming()
    grid.show_only_input_index(*digits)
    for i in targets:
        assert grid.cells[i].has(rm) is False


if __name__ == '__main__':
    parameter = '-sv'  # 's' to print to console.
    pytest.main([parameter, __file__])
