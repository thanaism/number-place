import os
import sys
import pytest
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def grid_creation():
    from src.grid import Grid
    grid = Grid()
    for i in grid.boxes[3]:
        grid.cells[i].remove(7)
    grid.cells[37].add(7)
    grid.cells[38].add(7)
    yield grid


def test_lc_pointing(grid_creation):
    grid = grid_creation
    count = 0
    for i in grid.boxes[3]:
        if grid.cells[i].has(7):
            count += 1
    assert count == 2
    grid.lc_pointing()
    for i in range(39, 44):
        assert grid.cells[i].has(7) is False
    l = []
    for b in range(9):
        for i in grid.boxes[b]:
            if b != 3 and grid.cells[i].row != 4:
                candidates = grid.cells[i].candidates
                assert grid.cells[i].has(7) is True
                if candidates != 511:
                    l.append((i, candidates))
    print(l)
    grid.show_index()


if __name__ == '__main__':
    parameter = '-sv'  # 's' to print to console.
    pytest.main([parameter, __file__])
