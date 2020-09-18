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


@pytest.mark.parametrize('box, target, i1, i2, peer', [
    (3, 7, 37, 38, 4),
    (1, 4, 3, 12, 12),
    (8, 2, 78, 80, 8)
])
def test_lc_pointing(box, target, i1, i2, peer, grid_creation):
    grid = grid_creation
    for i in grid.boxes[box]:
        grid.cells[i].remove(target)
    grid.cells[i1].add(target)
    grid.cells[i2].add(target)
    count = 0
    for i in grid.boxes[box]:
        if grid.cells[i].has(target):
            count += 1
    assert count == 2
    grid.lc_pointing()
    for i in grid.boxes[box]:
        if i != i1 and i != i2:
            assert grid.cells[i].has(target) is False
    for i in grid.houses[peer]:
        if i != i1 and i != i2:
            assert grid.cells[i].has(target) is False
    for i in range(81):
        if i in grid.boxes[box] \
                and i in grid.houses[peer] \
                and i in [i1, i2]:
            candidates = grid.cells[i].candidates
            assert grid.cells[i].has(target) is True
            assert candidates == 511
    print()
    grid.show_index()


if __name__ == '__main__':
    parameter = '-sv'  # 's' to print to console.
    pytest.main([parameter, __file__])
