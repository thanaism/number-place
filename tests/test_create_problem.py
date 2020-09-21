import os
import sys
import pytest
import time
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def grid_creation():
    from src.grid import Grid
    grid = Grid()
    return grid


# @pytest.mark.parametrize('sequence', [
    # (),
    # ('000000000'
    #  + '000000000'
    #  + '000000000'
    #  + '000000000'
    #  + '000000000'
    #  + '000000000'
    #  + '000000000'
    #  + '000000000'
    #  + '000000000')
    # ('000380094'
    #  + '804270000'
    #  + '935640872'
    #  + '169000380'
    #  + '000813000'
    #  + '048000721'
    #  + '280037569'
    #  + '000068207'
    #  + '690052008'),
    # (''
    #  + '013'+'000'+'000'
    #  + '000'+'008'+'006'
    #  + '070'+'000'+'001'
    #  + '060'+'000'+'490'
    #  + '000'+'070'+'800'
    #  + '007'+'060'+'200'
    #  + '200'+'096'+'308'
    #  + '040'+'020'+'600'
    #  + '700'+'400'+'000'),
    # (''
    #  + '490'+'083'+'700'
    #  + '100'+'000'+'000'
    #  + '002'+'400'+'600'
    #  + '030'+'500'+'900'
    #  + '000'+'100'+'000'
    #  + '920'+'060'+'001'
    #  + '800'+'000'+'000'
    #  + '000'+'000'+'080'
    #  + '045'+'000'+'023')
# ])
def test_create(grid_creation):  # sequence, grid_creation):
    print('\n')
    grid = grid_creation
    # print(grid.can_solve)
    # grid.show_grid()
    start = time.time()
    count = 0
    while grid.techniques['X-Wing'] is False:
        grid.set_sequence('0'*81)
        # grid.show_grid()
        # print(grid.create())
        grid.create()
        # assert grid.sum_check() is True
        count += 1
        grid.create_problem(0)
    print(grid.answer)
    print(count)
    elapsed_time = time.time() - start
    print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
    grid.show_grid()
    print(grid.count_digits())
    print(grid.techniques)


if __name__ == '__main__':
    parameter = '-sv'  # 's' to print to console.
    pytest.main([parameter, __file__])
