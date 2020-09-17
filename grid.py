from cell import Cell
from datetime import datetime
import random
import itertools


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
      指定インデックスに対して同一ブロックに含まれるインデックスの配列
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
        # self.__unfilled=[1]*81

    def unfilled_in_house(self, house_index, candidates=0x1FF):
        """指定したハウス内の指定した候補を持つマスのインデックス配列を返す"""
        return [i for i in self.houses[house_index]
                if self.cells[i].candidates & candidates]

    # def low_hanging_fruit(self):
    #   for c in self.cells:
    #     self.rows[c.row]
    #     if c.digit!=0:
    #       pass
    #   return 1

    def single_candidate(self, index, digit):
        """対象セルが対象数字を唯一の候補として持つかを真偽値でリターン"""
        return self.cells[index].candidates | 1 << digit - 1 == 1 << digit - 1
    # def create_diagonal(self):

    def create(self):
        """問題を生成する"""
        self.__givens = 20
        r81 = Grid.rand81()

        def create_ans(index):
            """解答の盤面を生成する再帰関数"""
            for i in range(index, 81):
                if self.cells[i].digit == 0:
                    index = i
                    break
            for j in Grid.rand9():
                if self.can_place(index, j):
                    self.cells[index].digit = j
                    if index + 1 == 81:
                        return True
                    else:
                        if create_ans(index + 1):
                            return True
                        self.cells[index].digit = 0
            return False

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
        create_ans(0)
        # erase_digit(0)

    def last_digit(self):
        """
        Last digit法
        未確定のセルが1つのハウスを確定
        """
        count = 0
        for house in Grid.houses:
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
                self.cells[idx].digit = remain.pop()
                count += 1
        print(f'Last digit -> filled {count} cells.')
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
                # Naked Single
                if c.count == 1:
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
        # while True:
        # blank_before=self.count_blank

        for digit in range(1):  # ,10):
            for house in self.houses:
                # res=[]
                for i in house:
                    # res+=i,
                    if self.cells[i].candidates:
                        pass
                # print(','.join(map(str,res)))
            #   c=self.cells[i]
            #   if c.digit==0:
            #     # Hidden Single
            #     self.erase_peers_candidates(i,c.digit)
            # if self.count_blank==blank_before:break

    @property
    def can_solve(self):
        """盤面が仮定法なしで解けるかを返す"""
        # CRBE法
        # 後述の下位互換のため一旦パス

    def erase_peers_candidates(self, cell_index, digit):
        """指定マスと同一ハウスにあるマスから指定の候補数字を消去する"""
        for i in Grid.peers[cell_index]:
            if (c := self.cells[i]).candidates != 0 and i != cell_index:
                c.remove(digit)

    @property
    def sequence(self):
        """全マスの数字を連結した文字列でリターン"""
        return ''.join([str(self.cells[i].digit) for i in range(81)])

    @property
    def grid(self):
        """盤面をlist[int]で返す"""
        return [self.cells[i].digit for i in range(81)]

    def sum_check(self):
        """すべてのハウスにおいて9マスの合計値が正しいかをリターン"""
        def check_sum_of_house(house):
            return 45 == sum([self.cells[i].digit for i in house])
        return all([check_sum_of_house(Grid.houses[j]) for j in range(27)])

    def count_blank(self):
        """盤面に含まれるすべての空白マスの個数をリターン"""
        return self.sequence.count('0')

    def can_place(self, index, digit):
        """指定したマスに指定した数字を配置可能か（ハウス内に重複数字がないか）をリターン"""
        for i in Grid.peers[index]:
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