class LogicError(Exception):
    pass


class Cell:
    """
    セルの情報を保持する。

    Attributes
    ----------
    index : int
      セルのインデックス番号、左上から右方向へ0-80
    row : int
      行番号、上から下に0-8
    column : int
      列番号、左から右に0-8
    box : int
      ボックスの番号、左上から右に0-8
    _digit : int
      確定数字、未確定時は0
    candidates : int
      候補数字を9ビットで表現、確定数字は0で候補なし
    """

    def __init__(self, index, digit):
        """
        Parameters
        ----------
        index : int
          0-80のインデックス番号
        digit : int
          セルの数字、未確定は0

        Notes
        -----
        入力値のバリデーションは未実装
        """
        self.index = index
        self.row = index // 9
        self.column = index % 9
        self.box = index // 27 * 3 + index % 9 // 3
        self._digit = digit
        if digit == 0:
            self.candidates = 0x1FF
        else:
            self.candidates = 0

    @property
    def count(self):
        """
        候補数字の個数を返す。
        """
        return bin(self.candidates).count('1')

    @property
    def digit(self):
        """
        セルの確定数字を返す、未確定は0
        """
        return self._digit

    @property
    def naked_single(self):
        """
        Naked Singleの場合に、その数字を返す
        """
        ret_digit = len(bin(self.candidates & -self.candidates)) - 2
        return ret_digit if self.candidates != 0 else 0

    @digit.setter
    def digit(self, digit):
        """
        セルに数字をセットする。未確定時は候補数字を0x1FFで初期化。

        Parameters
        ----------
        digit : int
          格納する数字、1-9または未確定の0

        Notes
        -----
        入力値のバリデーションは未実装
        """
        if digit != 0:
            self.candidates = 0
            self._digit = digit
        else:
            self.candidates = 0x1FF
            self._digit = digit

    def add(self, *digits):
        """
        候補数字を加える。複数指定可能。

        Parameters
        ----------
        *digits : int
          カンマ区切りで加える数字1-9を列挙

        Notes
        -----
        入力値のバリデーションは未実装
        """
        for digit in digits:
            self.candidates |= 1 << digit - 1

    def has(self, *digits, AND=True):
        """
        指定した数字を候補に持つかを真偽値で返す。

        Parameters
        ----------
        *digits : *int
        AND : bool
          Falseを指定するとOR判定になる
        """
        if digits[0] == 0:
            return False
        if AND:
            flg = []
            candidates = self.candidates
            for digit in (i - 1 for i in digits):
                if candidates >> digit & 1:
                    flg += True,
                else:
                    flg += False,
            return all(flg)
        else:
            flg = False
            candidates = self.candidates
            for digit in (i - 1 for i in digits):
                if candidates >> digit & 1:
                    flg = True
            return flg

    def remove(self, *digits):
        """
        指定の候補数字を削除する。複数指定可能。

        Parameters
        ----------
        *digits : int
          カンマ区切りで削除する数字1-9を列挙

        Notes
        -----
        入力値のバリデーションは未実装。

        Raises
        ------
        LogicError
          候補数字が枯渇した場合。
          候補数字をにするにはdigit.setterで確定数字を指定する。
        """
        for digit in digits:
            self.candidates &= ~(1 << digit - 1)
        if self.candidates == 0:
            raise LogicError('romoveメソッドにより候補数字が空になりました。')

    def show(self):
        """
        どの候補数字を持つかをビット表現でコンソールに出力する。
        """
        print(f'{self.candidates:b}')
