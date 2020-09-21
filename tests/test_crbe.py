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
    print('\n')
    print(f'sum check: {grid.sum_check()}')
    grid.show_grid()


@pytest.mark.parametrize('sequence, digit, targets', [
    ('000380094'
     + '804270000'
     + '935640872'
     + '169020380'
     + '000803000'
     + '048000721'
     + '280037569'
     + '000068207'
     + '690052008', 3, [45]),
    ('000380094'
     + '804270000'
     + '935640872'
     + '169000380'
     + '000813000'
     + '048000721'
     + '280037569'
     + '000068207'
     + '690052008', 2, [31]),
    ('000380094'
     + '804270000'
     + '935640072'
     + '169000380'
     + '000803000'
     + '048000721'
     + '280037569'
     + '000068207'
     + '690052008', 8, [24])
])
def test_crbe(sequence, digit, targets, grid_creation):
    grid = grid_creation
    grid.set_sequence(sequence)
    print('\n<---CRBE--->')
    grid.crbe()
    for i in targets:
        assert grid.cells[i].digit == digit


if __name__ == '__main__':
    parameter = '-sv'  # 's' to print to console.
    pytest.main([parameter, __file__])
