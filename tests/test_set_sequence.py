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
    grid.show_grid()


@pytest.mark.parametrize('sequence', [
    # (),
    # (),
    ('000380094'
     + '804270000'
     + '935640872'
     + '169000380'
     + '000803000'
     + '048000721'
     + '280037569'
     + '000068207'
     + '690052008')
])
def test_set_sequence(sequence, grid_creation):
    grid = grid_creation
    print('\n<---SET SEQUENCE FUNCTION--->')
    grid.set_sequence(sequence)


if __name__ == '__main__':
    parameter = '-sv'  # 's' to print to console.
    pytest.main([parameter, __file__])
