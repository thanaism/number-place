from cell_grid import *

cell=Cell(0,0)
cell.remove(6,7,8)
assert cell.has(1,2,3,4,5,6,7,8,9)==False
assert cell.has(1,2,3,4,5,6,7,8,9,AND=False)==True
assert cell.has(1,2,3,4,5,9)==True
assert cell.has(1)==True
assert cell.has(8)==False
exit()

# インスタンス生成・解答盤面生成
grid=Grid()
grid.create()

grid.hidden_single()
exit()

# 適当に数字を消す
for i in grid.rand81()[:40]:
  grid.cells[i].digit=0

# 復元前の盤面表示
grid.show_grid()

# Last digitの実行
  # naked-singleの下位互換になっている？
grid.last_digit()

# Naked singleの実行
grid.naked_single()

# 復元盤面の表示
grid.show_grid()

# 回転・反転した同形8パターンの表示
test_seq='473826519591473286826159734352748691618295473749631852964387125285914367137562948'
for s in Grid.rotate(test_seq): 
  print(''.join(map(str,s)))

# クラス化していない関数の呼び出し可否確認
show_index()