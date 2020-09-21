from .cell import Cell
from datetime import datetime
import random
import itertools
import copy
# import sys


class LogicError(Exception):
    pass


class Grid:
    """
    ナンプレ盤面への操作と状態保持を行う。Cellクラス81マスはここで保持。

    Attributes
    ----------
    rows : list(int)
      上から順に各行のインデックスを保持
    columuns : list(int)
      左から順に各列のインデックスを保持
    boxes : list(int)
      左上から右下の順に各ボックスのインデックスを保持
    houses : list(int)
      各行・列・ボックスのインデックスを保持
    peers_row : list(int)
      指定インデックスに対して同一行に含まれるインデックスの配列
    peers_column : list(int)
      指定インデックスに対して同一列に含まれるインデックスの配列
    peers_box : list(int)
      指定インデックスに対して同一ボックスに含まれるインデックスの配列
    peers : list(int)
      指定インデックスに対して同一行・列・ボックスに含まれるインデックスの配列
    """
    rows = tuple(tuple(i for i in range(81) if i // 9 == j) for j in range(9))
    columns = tuple(tuple(i for i in range(81) if i % 9 == j)
                    for j in range(9))
    boxes = tuple(tuple(i for i in range(81) if i // 27 * 3 + i %
                        9 // 3 == j) for j in range(9))
    houses = rows + columns + boxes
    peers_row = tuple(tuple(i + j // 9 * 9 for i in range(9))
                      for j in range(81))
    peers_column = tuple(tuple(9 * i + j % 9 for i in range(9))
                         for j in range(81))
    peers_box = tuple(tuple(i // 3 * 6 + i + j // 27 * 27 + j %
                            9 // 3 * 3 for i in range(9)) for j in range(81))
    peers = tuple({*i, *j, *k}
                  for (i, j, k) in zip(peers_box, peers_column, peers_row))
    floors = tuple(tuple(i for i in range(81) if i // 9 // 3 == j)
                   for j in range(3))
    towers = tuple(tuple(i for i in range(81) if i % 9 // 3 == j)
                   for j in range(3))
    chutes = floors + towers
    peers_floor = tuple(tuple(i + j // 27 * 27 for i in range(27))
                        for j in range(81))
    peers_tower = tuple(tuple(i // 3 * 9 + j % 9 // 3 * 3 + i %
                              3 for i in range(27)) for j in range(81))

    def __init__(self, difficulty=0, np_type=0):
        """
        Attributes
        ----------
        creation_datetime : str
        difficulty : int
        type : int
        cells : list(Cell)
        """
        self.creation_datetime = f'{datetime.now():%m%d%H%M%S%f}'
        self.difficulty = difficulty
        self.type = np_type  # 0:normal,1:diagonal,2:sum
        self.cells = [Cell(i, 0) for i in range(81)]
        self.answer = None

    def unfilled_in_house(self, house_index, candidates=0x1FF):
        """指定したハウス内の指定した候補を持つマスのインデックス配列を返す"""
        return [i for i in self.houses[house_index]
                if self.cells[i].candidates & candidates]

    def single_candidate(self, index, digit):
        """対象セルが対象数字を唯一の候補として持つかを真偽値でリターン"""
        return self.cells[index].candidates | 1 << digit - 1 == 1 << digit - 1

    def create(self):
        # sys.setrecursionlimit(2000)
        # print(f'recursion limit: {sys.getrecursionlimit()}')
        """解答を生成する"""
        def create_ans(index):
            """解答の盤面を生成する再帰関数"""
            for i in range(index, 81):
                if self.cells[i].digit == 0:
                    index = i
                    break
            # print(f'index: {index}')
            if self.cells[index].digit > 0 and index == 80:
                return True
            for j in self.rand9():
                if self.can_place(index, j):
                    self.cells[index].digit = j
                    # self.show_grid()
                    if index + 1 == 81:
                        return True
                    else:
                        if create_ans(index + 1):
                            return True
                        self.cells[index].digit = 0
            return False
        return create_ans(0)

    def create_problem(self):
        """問題を作成する"""
        r81 = self.rand81()

        def erase_digit(index):
            """完成盤面にランダムに穴あけしていく再帰関数"""
            if self.count_blank() >= 81 - self.__givens or index == 81:
                return
            i = r81[index]
            if self.cells[i] != 0:
                buf, self.cells[i].digit = self.cells[i].digit, 0
                if not self.can_solve:
                    self.cells[i].digit = buf
            erase_digit(index + 1)

    def last_digit(self):
        """
        Last digit法
        未確定のセルが1つのハウスを確定
        """
        count = 0
        for house in self.houses:
            unfilled = 0
            idx = None
            remain = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            for i in house:
                d = self.cells[i].digit
                if d == 0:
                    unfilled += 1
                    idx = i
                else:
                    remain -= {d}
            if unfilled == 1:
                target = remain.pop()
                print(f'Last digit -> {target} to {idx}')
                self.cells[idx].digit = target
                count += 1
        return count

    def naked_single(self):
        """
        Naked Single法
        候補数字が1つのセルを確定
        """
        count = 0
        # 空白セルが減らなくなるまで繰り返す
        while True:
            blank_before = self.count_blank
            for i in range(81):
                c = self.cells[i]
                if c.digit > 0:
                    self.erase_peers_candidates(i, c.digit)
            for i in range(81):
                c = self.cells[i]
                if c.count == 1:  # Naked Single
                    c.digit = bin(c.candidates)[::-1].find('1') + 1
                    count += 1
                    self.erase_peers_candidates(i, c.digit)
            if self.count_blank == blank_before:
                break
        print(f'Naked single -> filled {count} cells.')
        return count

    def hidden_single(self):
        """
        Hidden Single法
        同一ハウス内で当該の候補数字を持つセルが1つのみであれば確定
        """
        # 空白セルが減らなくなるまで繰り返す
        while True:
            blank_before = self.count_blank
            for digit in range(1, 10):
                for i, house in enumerate(self.houses):
                    cells_unfilled = self.unfilled_in_house(i, 1 << (digit-1))
                    if len(cells_unfilled) == 1:
                        hidden_single = cells_unfilled[0]
                        self.cells[hidden_single].digit = digit
                        self.erase_peers_candidates(hidden_single, digit)
            if self.count_blank == blank_before:
                break

    def lc_pointing(self):
        """
        Locked candidates(Pointing)法
        同一ボックス内で単一の行（列）のみに候補数字が存在する場合に、
        同一行（列）でボックス外にある候補を削除可能
        """
        for digit in range(1, 10):
            row_occupied = [0]*9
            col_occupied = [0]*9
            for i in range(81):
                if self.cells[i].has(digit):
                    row = self.cells[i].row
                    column = self.cells[i].column
                    box = self.cells[i].box
                    row_occupied[box] |= (1 << row)
                    col_occupied[box] |= (1 << (column+9))
            for b in range(9):
                for rc in (row_occupied[b], col_occupied[b]):
                    if bin(rc).count('1') == 1:
                        house = bin(rc)[::-1].find('1')
                        for i in self.unfilled_in_house(house, 1 << (digit-1)):
                            if self.cells[i].box != b:
                                self.cells[i].remove(digit)

    def lc_claiming(self):
        """
        Locked candidates(Claiming)法
        同一行（列）内で単一のボックスのみに候補数字が存在する場合に、
        同一ボックスで行（列）外にある候補を削除可能
        """
        for digit in range(1, 10):
            row_occupied = [0]*9
            col_occupied = [0]*9
            for cell in self.cells:
                if cell.has(digit):
                    row_occupied[cell.box] |= (1 << cell.row)
                    col_occupied[cell.box] |= (1 << cell.column)
            for b in range(9):
                peer_boxes = self.peer_boxes_in_chute(b)
                for i, v in enumerate([row_occupied, col_occupied]):
                    b1, b2 = peer_boxes[0+i*2], peer_boxes[1+i*2]
                    if bin(v[b]).count('1') <= 1:
                        continue
                    if (bit_b1 := v[b1] & 0x1FF) <= 0:
                        continue
                    if (bit_b2 := v[b2] & 0x1FF) <= 0:
                        continue
                    b12 = bit_b1 | bit_b2
                    non_common = bin(v[b] & (b12 ^ 0x1FF))[::-1].find('1')
                    if bin(b12).count('1') == 2 and non_common >= 0:
                        for j in self.unfilled_in_house(18+b, 1 << (digit-1)):
                            found_cell = self.cells[j]
                            if found_cell.row != non_common and i == 0:
                                self.cells[j].remove(digit)
                                print(f'remove {digit} in house {j}')
                            if found_cell.column != non_common and i == 1:
                                self.cells[j].remove(digit)
                                print(f'remove {digit} in house {j}')

    def ls_hidden(self, dim):
        """
        Locked set (hidden)法

        Patameters
        ----------
        dim : int
            次数(Pair, triple, quadruple ...)

        Notes
        -----
        # サムナンプレでは、サムをハウスに含めるとハウス個数が不定のためおそらくバグとなる。

        # 高速化するならhideenとnakedを1つの探索にする
        ハウス内の空白マス数：ucell_count
        includes：選択セル
        excludes：非選択セル
        選択セルの個数＝次数
        選択セルの候補数字数＝不定
        一方で、
        非選択セルの候補数字数＝空白数-次数
        非選択セルの個数＝ハウス内の候補数字数-次数
        よって、len(ex_candidates)==len(excludes)が条件
        """
        for i_house, v_house in enumerate(self.houses):
            cells_unfilled = self.unfilled_in_house(i_house)
            ucell_count = len(cells_unfilled)
            if ucell_count <= dim:
                continue
            for cmb in itertools.combinations(cells_unfilled, dim):
                includes = set(cmb)
                excludes = set(v_house)-includes
                in_candidates = ex_candidates = 0
                for i in includes:
                    in_candidates |= self.cells[i].candidates
                for i in excludes:
                    ex_candidates |= self.cells[i].candidates
                # in_bitcount = bin(in_candidates).count('1')
                ex_bitcount = bin(ex_candidates).count('1')
                if ex_bitcount == len(excludes) == ucell_count-dim:
                    for i in includes:
                        bit = self.cells[i].candidates & ex_candidates
                        rm = []
                        for j in range(9):
                            if f'{bit:09b}'[::-1][j] == '1':
                                rm += j+1,
                        # print(f'includes: {includes}, excludes: {excludes}')
                        print(f'house: {i_house}, index: {i}, remove: {rm}')
                        self.cells[i].remove(*rm)

    def ls_naked(self, dim):
        """
        Locked set (naked)法

        Patameters
        ----------
        dim : int
            次数(Pair, triple, quadruple ...)

        Notes
        -----
        次数＝選択セルの候補数字数＝不定
        """
        for i_house, v_house in enumerate(self.houses):
            cells_unfilled = self.unfilled_in_house(i_house)
            ucell_count = len(cells_unfilled)
            if ucell_count <= dim:
                continue
            for cmb in itertools.combinations(cells_unfilled, dim):
                includes = set(cmb)
                excludes = set(v_house)-includes
                in_candidates = ex_candidates = 0
                for i in includes:
                    in_candidates |= self.cells[i].candidates
                for i in excludes:
                    ex_candidates |= self.cells[i].candidates
                in_bitcount = bin(in_candidates).count('1')
                # ex_bitcount = bin(ex_candidates).count('1')
                if in_bitcount == dim:
                    for i in excludes:
                        bit = in_candidates
                        rm = []
                        for j in range(9):
                            if f'{bit:09b}'[::-1][j] == '1':
                                rm += j+1,
                        # print(f'includes: {includes}, excludes: {excludes}')
                        print(f'house: {i_house}, index: {i}, remove: {rm}')
                        self.cells[i].remove(*rm)

    def x_wing(self):
        """
        X-Wingメソッド
        Fishで一般化可能；
        N個以下の対象数字を含むBase set
        それをカバーするCover setの概念を使用する
        今回はX-Wingケースのみに絞ってビットを使用せず書く
        すべてのナンプレで使用可能なはず。
        """
        cmb = itertools.combinations
        fish_size = 2
        for digit in range(1, 10):
            bit = 1 << (digit-1)
            # print(f'digit: {digit} starts...')
            # Row -> Col, Col -> Row
            for rowcol in [(0, 9), (9, 0)]:
                base_sets = []
                for rc in range(9):
                    unfilleds = self.unfilled_in_house(rc+rowcol[0], bit)
                    if len(unfilleds) == fish_size:
                        # print(
                        #     f'base house: {rc+rowcol[0]}')
                        base_sets += unfilleds,
                        # print(f'base sets: {base_sets}')
                for base_set in cmb(base_sets, fish_size):
                    # print(f'base set found: {base_set[0],base_set[1]}')
                    bs_indexes = set()
                    for i in base_set:
                        bs_indexes.update({*i})
                    # bs_indexesにbase_setのindexが含まれている状態
                    cover_sets = []
                    for rc in range(9):
                        unfilleds = self.unfilled_in_house(rc+rowcol[1], bit)
                        if len(unfilleds) >= 2:
                            # print(
                            #     f'cover house: {rc+rowcol[1]}')
                            cover_sets += unfilleds,
                            # print(f'cover sets: {cover_sets}')
                    for cover_set in cmb(cover_sets, fish_size):
                        # print(
                        #     f'cover set found: {cover_set[0],cover_set[1]}')
                        cs_indexes = set()
                        for i in cover_set:
                            cs_indexes.update({*i})
                        # cs_indexesにcover_setのindexが含まれている状態
                        if bs_indexes.issubset(cs_indexes):
                            removables = cs_indexes-bs_indexes
                            if len(removables) > 0:
                                print(
                                    f'X-Wing: {bs_indexes}, {cs_indexes}')
                                print(f'remove: {removables}')
                                for i in removables:
                                    self.cells[i].remove(digit)
                                # remain = [i for i in range(
                                #     81) if self.cells[i].has(digit)]
                                # self.show_only_input_index(*remain)
                                return True
        return False

    @ staticmethod
    def peer_boxes_in_chute(box_index):
        """
        Returns
        -------
        (br1, br2, bc1, bc2) : tuple(int)
        同一floorのboxインデックス、同一towerのboxインデックス
        """
        b = box_index
        br1 = b//3*3+(b+1) % 3
        br2 = b//3*3+(b+2) % 3
        bc1 = (b+3) % 9
        bc2 = (b+6) % 9
        return (br1, br2, bc1, bc2)

    def copy_grid(self):
        copied_grid = copy.deepcopy(self)
        return copied_grid

    @ property
    def can_solve(self):
        """盤面が仮定法なしで解けるかを返す"""
        # CRBE法：後述の下位互換のため一旦パス

    def erase_peers_candidates(self, cell_index, digit):
        """指定マスと同一ハウスにあるマスから指定の候補数字を消去する"""
        for i in self.peers[cell_index]:
            if (c := self.cells[i]).candidates != 0 and i != cell_index:
                c.remove(digit)

    @ property
    def sequence(self):
        """全マスの数字を連結した文字列でリターン"""
        return ''.join([str(self.cells[i].digit) for i in range(81)])

    @ property
    def grid(self):
        """盤面をlist[int]で返す"""
        return [self.cells[i].digit for i in range(81)]

    def sum_check(self):
        """すべてのハウスにおいて9マスの合計値が正しいかをリターン"""
        def check_sum_of_house(house):
            return 45 == sum([self.cells[i].digit for i in house])
        return all([check_sum_of_house(self.houses[j]) for j in range(27)])

    def count_blank(self):
        """盤面に含まれるすべての空白マスの個数をリターン"""
        return self.sequence.count('0')

    def can_place(self, index, digit):
        """指定したマスに指定した数字を配置可能か（ハウス内に重複数字がないか）をリターン"""
        for i in self.peers[index]:
            if self.cells[i].digit == digit:
                return False  # 1つでも該当ケースがあればNG
        return True

    def show_grid(self, grid=None):
        """現在の盤面を整形してコンソールに表示"""
        print('+-------+-------+-------+')
        for i in range(81):
            if grid is None:
                d = self.cells[i].digit
            else:
                d = grid[i]
            d = str(d) if d > 0 else '*'
            if i % 9 == 8:
                print(f'{d} |')
                if all([i // 9 % 3 == 2, i // 9 != 8]):
                    print('+-------+-------+-------+')
            elif i % 9 % 3 == 0:
                print(f'| {d} ', end='')
            else:
                print(f'{d} ', end='')
        print('+-------+-------+-------+')

    @ staticmethod
    def rand9():
        """1-9のランダム順列をリターン"""
        return random.sample([*range(1, 10)], 9)

    @ staticmethod
    def rand81():
        """1-81のランダム順列をリターン"""
        return random.sample([*range(81)], 81)

    @ staticmethod
    def rotate(grid):
        """
        gridを入力すると回転・反転の全8パターンをリストにしてリターン

        parameters
        ----------
        grid : list(int) or str
          整数配列、シーケンス文字列どちらでも可。

        Returns
        -------
        grids : list(list(int))

        Notes
        -----
        90度ごとの回転のため、{Row, Column ,8-Row, 8-Column}の組み合わせで得られる8パターンとなる。

        """
        if type(grid) is str:
            grid = [int(i) for i in grid]

        def get_other_pattern_index():
            pattern = [(i//9, i % 9, 8 - i//9, 8-i % 9) for i in range(81)]
            indexes = []
            pairs = [(i, j) for i, j in itertools.permutations(
                range(4), 2) if (i ^ j) & 1]
            for row, column in pairs:  # itertools.combinations(range(4), 2):
                indexes += [grid[i[row]*9+i[column]] for i in pattern],
            return indexes

        grids = []
        for i in get_other_pattern_index():
            grids += i,

        return grids

    @ staticmethod
    def show(*digits):
        """1-9の入力整数タプルに対して、立っているビット位置をコンソールに表示（候補数字フラグ確認用）"""
        print(f'{0x1FF&sum([1<<(i-1) for i in digits]):b}')

    @ staticmethod
    def show_index():
        """インデックスの位置関係をコンソールに表示"""
        print('+----------+----------+----------+')
        for i in range(81):
            if i % 9 == 8:
                print(f'{i:>2d} |')
                if all([i // 9 % 3 == 2, i // 9 != 8]):
                    print('|----------+----------+----------|')
            elif i % 9 % 3 == 0:
                print(f'| {i:>2d} ', end='')
            else:
                print(f'{i:>2d} ', end='')
        print('+----------+----------+----------+')

    @ staticmethod
    def show_only_input_index(*indexes):
        """インデックスの位置関係をコンソールに表示"""
        print('+----------+----------+----------+')
        for i in range(81):
            if i not in indexes:
                if i % 9 == 8:
                    print('** |')
                    if all([i // 9 % 3 == 2, i // 9 != 8]):
                        print('|----------+----------+----------|')
                elif i % 9 % 3 == 0:
                    print('| ** ', end='')
                else:
                    print('** ', end='')
            else:
                if i % 9 == 8:
                    print(f'{i:>2d} |')
                    if all([i // 9 % 3 == 2, i // 9 != 8]):
                        print('|----------+----------+----------|')
                elif i % 9 % 3 == 0:
                    print(f'| {i:>2d} ', end='')
                else:
                    print(f'{i:>2d} ', end='')
        print('+----------+----------+----------+')

    def crbe(self):
        self.last_digit()
        # skipフラグ
        skip = [False]*10
        # 個数カウント初期化
        digit_count = {}
        while True:  # sum(skip) < 9:
            for i in range(1, 10):
                digit_count[i] = 0
            # 個数カウント
            for i in range(81):
                d = self.cells[i].digit
                if d != 0:
                    digit_count[d] += 1
            # 降順ソート
            target = 0
            for i, v in sorted(digit_count.items(), key=lambda x: -x[1]):
                if v == 9:
                    skip[i] = True
                if not skip[i]:
                    target = i
                    print(f'target: {target}')
                    break
            if target == 0:
                break
            # 見つかった数字について各boxをサーチ
            for i_box, v_box in enumerate(self.boxes):
                # print(f'target: {target}, box: {i_box}')
                # 当該boxに対応する行列のHouseインデックス
                rows = [i_box // 3 * 3 + j for j in range(3)]
                columns = [i_box % 3 * 3 + j + 9 for j in range(3)]
                house_indexes = rows+columns
                # print(f'houses: {house_indexes}')
                # Box内の9マスにtargetが配置可能かのフラグ
                can_exist = {}
                for i in v_box:
                    can_exist[i] = 1
                # 対象行列6つのループ
                for i_house, v_house in enumerate(house_indexes):
                    if self.digit_exists_in_house(target, v_house):
                        # if i_house < 3:  # Row
                        for j in set(v_box) & set(self.houses[v_house]):
                            # print(f'house {v_house}, remove: {j}')
                            can_exist[j] = 0
                        # else:  # Column
                        # for j in set(v_box)&set(v_house):
                            # print(f'Col {i_house}, Remove: {j}')
                            # can_exist[j] = False
                # すでに数字のあるセルもFalseにする
                # targetがbox内にある場合もFalse
                for i, v in enumerate(v_box):
                    digit = self.cells[v].digit
                    if digit == target:
                        for k in v_box:
                            can_exist[k] = 0
                        break
                    if digit > 0:
                        can_exist[v] = 0
                # print(f'can_exist: {can_exist.values()}')
                # 配置可能マスが1つなら確定
                if sum(can_exist.values()) == 1:
                    for k, v in can_exist.items():
                        if v:
                            self.cells[k].digit = target
                            # digit_count[target] += 1
                            print(f'CRBE -> {target} to {k}')
                            # 本来はCRBEがすべて終了するまでを1つのメソッドにしたい
                            # 単なるreturnだとskipフラグの管理が無意味
                            # return
                    self.last_digit()
                    for i in range(10):
                        skip[i] = False
            skip[target] = True

    def digit_exists_in_house(self, digit, house_index):
        for i in self.houses[house_index]:
            if self.cells[i].digit == digit:
                return True
        return False

    def set_sequence(self, digits):
        if len(digits) != 81:
            raise LogicError('入力には長さ81の配列または文字列が必要です')
        for i, v in enumerate(digits):
            if type(v) == str:
                self.cells[i].digit = int(v)
            else:
                self.cells[i].digit = v
