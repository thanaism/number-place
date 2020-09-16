from cell_grid import *

g=Grid()
g.create()
for i in Grid.rand81()[:20]:
  g.cells[i].digit=0
g.show_grid()
# g.last_digit()
g.naked_single()
g.show_grid()
# print(Grid.rotate('473826519591473286826159734352748691618295473749631852964387125285914367137562948'))