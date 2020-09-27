import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def grid_creation():
    from src.grid import Grid

    # grid = Grid(np_type=3)
    grid = Grid(np_type=2)
    # grid = Grid(np_type=1)
    # grid = Grid(np_type=0)
    return grid


# @pytest.mark.parametrize([])
def test_create(grid_creation):
    from src.pysimplegui import show_on_gui

    print('\n')
    grid = grid_creation
    count = 0
    # while grid.techniques['Hidden Pair'] is False:
    # while grid.count_digits() > 25:
    while count < 1:
        grid.set_sequence('0' * 81)
        assert grid.create() is True
        # show_on_gui([*map(str, grid.group)], grid.lines, False)
        assert grid.sum_check() is True
        count += 1
        grid.create_problem(0)
    # show_on_gui([' ' if s == '0' else s for s in grid.answer], grid.lines, False)
    show_on_gui([' ' if s == '0' else s for s in grid.sequence], grid.lines, False)
    print(f'Hints: {grid.count_digits()}')
    for key, value in grid.techniques.items():
        print(f'{value*1}: {key}')


if __name__ == '__main__':
    parameter = '-sv'  # 's' to print to console.
    pytest.main([parameter, __file__])
