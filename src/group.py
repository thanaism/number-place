import itertools
import random
from collections import deque


class Group:
    def __init__(self):
        """
        Attributes
        ----------
        group : list of int
            各マスのインデックス
        """
        self.group = [i // 27 * 3 + i % 9 // 3 for i in range(81)]
        # グループ個数レンジの設定
        self.MIN_SIZE = 9
        self.MAX_SIZE = 9

    @property
    def members(self):
        return [
            [i for i in range(81) if self.group[i] == j]
            for j in range(max(self.group) + 1)
        ]

    def shuffle(self):
        # サムの場合にGr数が不定なのでカウント処理
        group_count = max(self.group) + 1
        # 順序をシャッフルする
        rand_order = random.sample([*range(group_count)], group_count)
        # nC2で条件合致するまでサーチする
        # owns,opposites: 自軍Grインデックス,敵軍Grインデックス
        for owns, opposites in itertools.combinations(rand_order, 2):
            # 自軍の周囲に敵軍がいたら格納
            """
            print(f'own,opp: {owns,opposites}')
            print(f'membres[owns]: {self.members[owns]}')
            print(f'membres[opps]: {self.members[opposites]}')
            """
            index_pairs = set()
            for i in self.members[owns]:
                for j in self.around4[i]:
                    if j is not None:
                        if self.group[j] == opposites:
                            index_pairs.update({(i, j)})
                            # 同じ数字を2回使用しないためのbreak
                            break
            # print(f'index_pairs: {index_pairs}')
            # 自軍と敵軍のペアが2つ以上なら、それぞれ切り取り可能かを確認してスワップする
            if len(index_pairs) >= 2:
                # print(f'index_pairs: {index_pairs}')
                """
                先に判定すると1回目のswapで入れ替えたときにバグる

                def f(x):
                    return self.can_replace(x)

                for i, j in index_pairs:
                    print(f(i), f(j))
                pairs_ok = [f(i) and f(j) for i, j in index_pairs]
                print(f'pairs_ok: {pairs_ok}')
                if sum(pairs_ok) >= 2:
                """
                swap_count = 0
                for i, v in enumerate(index_pairs):
                    if swap_count == 0:
                        if self.can_replace(v[0]):
                            # print(f'idx {v[0]}: group {own} -> {opp}')
                            buf = v[0]  # 復元用
                            self.group[v[0]] = self.group[v[1]]
                            swap_count += 1
                    elif swap_count == 1:
                        if self.can_replace(v[1]):
                            # print(f'idx {v[1]}: group {opp} -> {own}')
                            self.group[v[1]] = self.group[v[0]]
                            swap_count += 1
                    else:
                        break
                if swap_count == 1:
                    # print(f'reverse: {buf}')
                    self.group[buf] = owns
                break

    @property
    def around8(self):
        """
        自身をXとして、周囲8マスのインデックスを以下の順序のリストで返す
        7 0 1
        6 X 2
        5 4 3
        """
        res = []
        for i in range(81):
            row = i // 9
            col = i % 9
            top = i - 9 if row != 0 else None
            rig = i + 1 if col != 8 else None
            bot = i + 9 if row != 8 else None
            lef = i - 1 if col != 0 else None
            tor = i - 8 if row != 0 and col != 8 else None
            tol = i - 10 if row != 0 and col != 0 else None
            bor = i + 10 if row != 8 and col != 8 else None
            bol = i + 8 if row != 8 and col != 0 else None
            res += ([top, tor, rig, bor, bot, bol, lef, tol],)

        return res

    @property
    def around4(self):
        """
        自身をXとして、周囲4マスのインデックスを以下の順序のリストで返す
        - 0 -
        3 X 1
        - 2 -
        """
        res = []
        for ls in self.around8:
            res += ([ls[i] for i in [0, 2, 4, 6]],)
        return res

    def can_replace(self, index):
        """
        指定したインデックスのマスが切り取り可能かを返す

        Examples
        --------
        自身を中心として、
        x x o
        x o o
        x x x -> OK

        o x o
        o o o
        x o x -> NG
        """
        flg8 = [False] * 8
        for i, v in enumerate(self.around8[index]):
            if v is not None and self.group[v] == self.group[index]:
                flg8[i] = True
        count = sum(
            [
                1
                for i in self.around4[index]
                if i is not None and self.group[i] == self.group[index]
            ]
        )
        if count == 1:
            return True
        elif count == 2:
            # if all([flg8[0], flg8[4]]) or all([flg8[2], flg8[6]]):
            #     return False
            # elif (
            if (
                all([flg8[0], flg8[1], flg8[2]])
                or all([flg8[2], flg8[3], flg8[4]])
                or all([flg8[4], flg8[5], flg8[6]])
                or all([flg8[6], flg8[7], flg8[0]])
            ):
                return True
            else:
                return False
        elif count == 3:
            if (
                all([not flg8[0], flg8[3], flg8[5]])
                or all([not flg8[2], flg8[5], flg8[7]])
                or all([not flg8[4], flg8[7], flg8[1]])
                or all([not flg8[6], flg8[1], flg8[3]])
            ):
                return True
            else:
                return False
        elif count == 4:
            return False
        # else:
        #     print(f'count(err): {count}')

    def show_group(self, grid=None):
        """現在のGr配置を整形してコンソールに表示"""
        print('+-------+-------+-------+')
        for i in range(81):
            if grid is None:
                d = self.group[i]
            else:
                d = grid[i]
            d = str(d)  # if d > 0 else '*'
            if i % 9 == 8:
                print(f'{d} |')
                if all([i // 9 % 3 == 2, i // 9 != 8]):
                    print('+-------+-------+-------+')
            elif i % 9 % 3 == 0:
                print(f'| {d} ', end='')
            else:
                print(f'{d} ', end='')
        print('+-------+-------+-------+')

    def show_lines(self):
        """
        罫線情報の表示
        """
        res = ''
        self.lines = [0] * 81
        for i in range(81):
            for j, v in enumerate(self.around4[i]):
                # print(j, v)
                if v is None:
                    self.lines[i] |= 1 << j
                elif self.group[v] != self.group[i]:
                    self.lines[i] |= 1 << j
            bit = self.lines[i]
            res += f'{bit:1x}'
            # print(f'{bit:04b}, {bit:1x}')
        return res

    def get_new_random_group(self, min_size, max_size):
        """
        最外殻の各ループで、新しいGrの生成が開始する
        さらに各ループ内でGr内の次マス再帰探索をコールする
        Parameters
        ----------
        min_size : int
            目標値の最低値
            （速度のため、拡張できなくなった場合にこの値を無視して最低2要素までは許容）
        max_size : int
            目標値の最大値
            （9個以上は問題が不成立となるためこちらは厳守される）
        """
        self.MIN_SIZE = min_size
        self.MAX_SIZE = max_size

        def grouping():
            # 便利のため-1で初期化
            self.group = [-1 for _ in range(81)]
            # 点対称なのでループ区間はインデックス40番まで
            for index in range(41):
                # 設定済みのグループはスキップ
                if self.group[index] > -1:
                    continue
                # 当該グループの個数
                group_size = random.randint(self.MIN_SIZE, self.MAX_SIZE)
                # 初期値-1のため0から開始される
                group_no = max(self.group) + 1
                empty_stack = deque()
                if self.group_dfs(index, group_size, group_no, empty_stack) is False:
                    return False
            # 成功した場合、点対称を転写
            for i in range(80, 40, -1):
                if self.group[i] < 0:
                    self.group[i] = self.group[80 - i]
            # インデックスを振り直す
            self.set_group_by_lines(self.show_lines())
            # ループを繰り返した場合などに個数チェックをすり抜けるケースがあるため最終チェック
            for i in self.members:
                if len(i) > self.MAX_SIZE:
                    return False
            return True

        while grouping() is False:
            pass

    def set_group_by_lines(self, lines):
        """
        罫線情報からGrインデックスを振り直す
        """

        def dfs(index, group_no, checked):
            self.group[index] = group_no
            checked[index] = True
            bit = eval('0x' + lines[index])
            for shift in range(4):
                if bit & 1 << shift:
                    continue
                next_cell = self.around4[index][shift]
                if next_cell is not None and checked[next_cell] is False:
                    self.group[next_cell] = group_no
                    dfs(next_cell, group_no, checked)

        checked = [False] * 81
        group_no = -1
        for i in range(81):
            if checked[i] is False:
                group_no += 1
                dfs(i, group_no, checked)

    def group_dfs(self, index, group_size, group_no, _stack):
        """
        各グループの次マス再帰探索
        """
        # 呼び出されたら自身をグループに追加する
        self.group[index] = group_no
        # この時点で規定数に満ちていたら再帰終了
        if len(self.members[group_no]) == group_size:
            return True
        # スタックの複製
        stack = _stack.copy()
        # グラフに見立てたときに周囲4マスに辺があるか（進むことが可能か）
        has_edges = set()
        # 点対称境界をループさせたaround4
        looped_around4 = set()
        for i in self.around4[index]:
            if i is None:
                continue
            if i in range(41, 50):
                # 境界オーバーした部分を展開したindexに置き換える
                looped_around4 |= {80 - i}
            else:
                # それ以外は普通に加える
                looped_around4 |= {i}

        for i in looped_around4:
            if self.group[i] < 0:
                # まだグループ未確定のマスならedgeに追加
                has_edges |= {i}

        if has_edges:
            # edgeからランダムに1つを次のマスに指定し、残りをスタックに積む
            next_node = random.choice([*has_edges])
            for i in has_edges - {next_node}:
                stack.append(i)
            # 再帰コールする（呼び出し先でグループに追加される）
            return self.group_dfs(next_node, group_size, group_no, stack)

        else:
            # 行き先となるマスがない場合
            while True:
                if stack:
                    # スタックに要素があればpopして未確定マスかチェック
                    next_node = stack.pop()
                    if self.group[next_node] < 0:
                        return self.group_dfs(next_node, group_size, group_no, stack)
                        break
                    else:
                        # ダメなら次のスタック要素へ
                        continue
                else:
                    # スタック内に候補となる要素がない
                    break
            """
            # スタックが尽きた場合にここに到達
            Notes
            -----
            いきなりreturn Falseすると終わらなくなる。
            jigと共通化するには、点対称条件の入切も同時に必要。
            そのままだと成立ケース少なすぎて無限にバックトラッキングされる。
            return False
            """
            # スタックが尽きた場合は、現状の自軍メンバー数を数える
            count = len(self.members[group_no])
            if count > 1:
                # 2マス以上ならそのまま打ち切り
                return True
            else:
                # 要素数1のグループの場合は、周囲とマージ出来るかを検討
                for i in looped_around4:
                    opp_group = self.group[i]  # 相手グループ
                    if len(self.members[opp_group]) < self.MAX_SIZE:
                        # 相手が最大未満（count==1なので自動的に自軍以外は満たす）ならマージ
                        self.group[index] = opp_group
                        return True
                if self.group[index] == group_no:
                    # マージ先がなかった場合、すべてをリセットする
                    return False
