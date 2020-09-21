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


@pytest.mark.parametrize('sequence', [
    # (),
    ('000000000'
     + '000000000'
     + '000000000'
     + '000000000'
     + '000000000'
     + '000000000'
     + '000000000'
     + '000000000'
     + '000000000'),
    ('000380094'
     + '804270000'
     + '935640872'
     + '169000380'
     + '000813000'
     + '048000721'
     + '280037569'
     + '000068207'
     + '690052008')
])
def test_create(sequence, grid_creation):
    print('\n')
    grid = grid_creation
    grid.set_sequence(sequence)
    # grid.show_grid()
    print(grid.create())
    grid.show_grid()
    print(grid.answer)
    assert grid.sum_check() is True


if __name__ == '__main__':
    parameter = '-sv'  # 's' to print to console.
    pytest.main([parameter, __file__])
