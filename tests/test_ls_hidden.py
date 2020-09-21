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


@pytest.mark.parametrize('house, rm, ls', [
    (10, [5, 7, 8], [1, 28, 73]),
    (19, [5, 8], [3, 22]),
    (0, [1, 2], [2, 7])
])
def test_ls_hidden(house, rm, ls, grid_creation):
    print('\n')
    grid = grid_creation
    # 対象数字をハウス内候補から削除
    for i in grid.houses[house]:
        grid.cells[i].remove(*rm)
    # LockedSetとなるセルにだけ対象数字を付与
    for i in ls:
        grid.cells[i].add(*rm)
    # 実行
    grid.show_only_input_index(*ls)
    while grid.ls_hidden(len(rm)):
        pass
    # 判定用ビット作成
    bit = 0x0
    for i in rm:
        bit |= 1 << (i-1)
    # 削除確認
    for i in ls:
        print(f'index: {i}, candidates: {grid.cells[i].candidates:09b}')
        assert grid.cells[i].candidates == bit


if __name__ == '__main__':
    parameter = '-sv'  # 's' to print to console.
    pytest.main([parameter, __file__])
