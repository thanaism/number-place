import pytest


def test_create(tp=2):  # grid_creation):
    from src.pysimplegui import show_on_gui
    from src.grid import Grid

    print('\n')
    grid = Grid(np_type=tp, min_gr_size=2, max_gr_size=5)
    assert grid.create() is True
    # show_on_gui([*map(str, grid.group)], grid.lines, False)
    assert grid.sum_check() is True
    grid.create_problem(0)
    sums = grid.sum_symbol if tp == 2 else [0] * 81
    # show_on_gui(
    #     [' ' if s == '0' else s for s in grid.answer],
    #     grid.lines,
    #     False,
    #     sums,
    # )
    show_on_gui(
        [' ' if s == '0' else s for s in grid.sequence],
        grid.lines,
        False,
        sums,
    )
    print(f'Answer:  {grid.answer}')
    print(f'Problem: {grid.problem}')
    print(f'Lines:   {grid.lines}')
    print(f'Hints:   {grid.count_digits()}')
    for key, value in grid.techniques.items():
        print(f'{value*1}: {key}')


if __name__ == '__main__':
    parameter = '-sv'
    pytest.main([parameter, __file__])
