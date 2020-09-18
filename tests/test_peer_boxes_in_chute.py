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


@pytest.mark.parametrize('digit,expected', [
    (0, (1, 2, 3, 6)),
    (5, (3, 4, 8, 2)),
    (7, (8, 6, 1, 4))
])
def test_peer_boxes_in_chute(digit, expected, grid_creation):
    grid = grid_creation
    assert grid.peer_boxes_in_chute(digit) == expected


if __name__ == '__main__':
    parameter = '-sv'  # 's' to print to console.
    pytest.main([parameter, __file__])
