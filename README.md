# Number Place Generator & Solver

## 概要

Python によるナンプレ問題生成＆解答作成の試作中

- 2020/09/16: Grid クラス内で cells を 1 種類しか持っていないので、穴あけ前後をどう管理するか、どう解答を保持するか要検討

## TODO

- ~~各解法を ON/OFF 出来るようにする~~
- GUI を実装する
- 問題のビューワを実装する（または Excel に出力する）
- 問題を csv に出力する
- ジグソー生成と house 追加
- サム生成と house 追加
- 罫線情報からグループ情報
- グループ情報から罫線情報
- グループは dfs で取得
- グループが交換可能か
  - 周囲に存在する同一 Gr の個数で場合分けが可能
  - 1 つなら無条件 OK
  - 2 つなら、
    - 対向 2 辺は NG
    - 以下は OK
    - ↑↗ ＋ →
    - →↘ ＋ ↓
    - ↓↙ ＋ ←
    - ←↖ ＋ ↑

元のコード（VBA で作ってた頃のやつ）

```vb
Rem 対象要素を切り取り後にグループが分断しないかを真偽値で返す
Private Function canReplace(ByVal idx, ByRef group) As Boolean
    Dim digitNeighbors: digitNeighbors = getDigitNeighbors(idx)
    Dim digitCorners: digitCorners = getDigitCorners(idx)
    Dim akinExists: Set akinExists = getAkinExistsColl(idx, group, digitNeighbors, digitCorners)

    Select Case getAkinNeighborsCount(idx, group, digitNeighbors)
        Case 1
            canReplace = True: Exit Function
        Case 2
            With akinExists
                If (.Item("TOP") And .Item("BOT")) Or _
                   (.Item("LEF") And .Item("RIG")) Then _
                   canReplace = False: Exit Function
                If (.Item("TOP") And .Item("TOR") And .Item("RIG")) Or _
                   (.Item("RIG") And .Item("BOR") And .Item("BOT")) Or _
                   (.Item("BOT") And .Item("BOL") And .Item("LEF")) Or _
                   (.Item("LEF") And .Item("TOL") And .Item("TOP")) Then _
                   canReplace = True: Exit Function
            End With
        Case 3
            With akinExists
                If ((Not .Item("TOP")) And .Item("BOR") And .Item("BOL")) Or _
                   ((Not .Item("RIG")) And .Item("TOL") And .Item("BOL")) Or _
                   ((Not .Item("BOT")) And .Item("TOR") And .Item("TOL")) Or _
                   ((Not .Item("LEF")) And .Item("TOR") And .Item("BOR")) Then _
                   canReplace = True: Exit Function
            End With
        Case 4
            canReplace = False: Exit Function
    End Select
End Function
```

### more

- beautiful soup ないし requests で問題をサーバーに submit する
