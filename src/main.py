import PySimpleGUI as sg
import edit_csv
import grid
import pyperclip


class GraphGUI:
    def __init__(self, cell_size=50, margin=4, thick_line_widh=4):
        self.CS = cell_size
        self.MA = margin
        self.THICK = thick_line_widh

    def get_graph_area(self):
        graph = sg.Graph(
            (self.CS * 9 + self.MA, self.CS * 9 + self.MA),
            (0, self.CS * 9 + self.MA),
            (self.CS * 9 + self.MA, 0),
            key="_GRAPH_",
            change_submits=True,
        )

        return graph

    def line_draw(self, graph, index, hex):
        row, col = index // 9, index % 9
        line_width = self.THICK
        # half_width = line_width / 2
        for shift in range(4):
            if hex & 1 << shift:
                if shift == 0:
                    bgn = (
                        self.CS * (col + 0),
                        self.CS * (row + 0),
                    )
                    end = (
                        self.CS * (col + 1),
                        self.CS * (row + 0),
                    )
                if shift == 1:
                    bgn = (
                        self.CS * (col + 1),
                        self.CS * (row + 0),
                    )
                    end = (
                        self.CS * (col + 1),
                        self.CS * (row + 1),
                    )
                if shift == 2:
                    bgn = (
                        self.CS * (col + 0),
                        self.CS * (row + 1),
                    )
                    end = (
                        self.CS * (col + 1),
                        self.CS * (row + 1),
                    )
                if shift == 3:
                    bgn = (
                        self.CS * (col + 0),
                        self.CS * (row + 0),
                    )
                    end = (
                        self.CS * (col + 0),
                        self.CS * (row + 1),
                    )
                graph.draw_line(
                    (
                        bgn[0] + self.MA / 2,
                        bgn[1] + self.MA / 2,
                    ),
                    (
                        end[0] + self.MA / 2,
                        end[1] + self.MA / 2,
                    ),
                    width=line_width,
                )

    def update_graph(self, window, graph, digits, lines, labels, is_dia=False):
        graph.Erase()
        label = [None] * 81
        digit = [None] * 81
        cell = [None] * 81
        for row in range(9):
            for col in range(9):
                index = row * 9 + col
                self.line_draw(graph, index, eval('0x' + lines[index]))
                if is_dia and (row == col or row == 8 - col):
                    fill_color = '#bbbbbb'
                else:
                    fill_color = '#dddddd'
                cell[index] = graph.draw_rectangle(
                    (col * self.CS + self.MA / 2, row * self.CS + self.MA / 2),
                    (
                        col * self.CS + self.CS + self.MA / 2,
                        row * self.CS + self.CS + self.MA / 2,
                    ),
                    line_width=0.25,
                    fill_color=fill_color,
                )
                label[index] = graph.DrawText(
                    text=labels[index],
                    location=(
                        col * self.CS + 10 + self.MA / 2,
                        row * self.CS + 7 + self.MA / 2,
                    ),
                    font=('Courier', 9),
                )
                digit[index] = graph.DrawText(
                    text=digits[index],
                    location=(
                        col * self.CS + 25 + self.MA / 2,
                        row * self.CS + 30 + self.MA / 2,
                    ),
                    font=('Courier', 35),
                )
        # for i in range(81):
        #     graph.bring_figure_to_front(cell[i])
        # 外枠の描画
        graph.draw_rectangle(
            (self.MA / 2, self.MA / 2),
            (self.CS * 9 + self.MA / 2, self.CS * 9 + self.MA / 2),
            line_width=self.MA,
        )
        return True


gui = GraphGUI()
graph = gui.get_graph_area()
frame = [
    [sg.Text('somehting', font=('', 50))],
]
# fmt: off
diff = sg.Frame('難易度（表示）', [[
    sg.Radio('入門', 1),
    sg.Radio('初級', 1),
    sg.Radio('中級', 1),
    sg.Radio('上級', 1),
    sg.Radio('難問', 1, default=True),
]])
types = sg.Frame('種類（表示・作成）', [[
    sg.Radio('通常', 2, default=True),
    sg.Radio('対角線', 2),
    sg.Radio('サム', 2),
    sg.Radio('ジグソー', 2),
]])
num_gen = sg.Frame('生成数（作成）', [[
    sg.Radio('10', 3, default=True),
    sg.Radio('100', 3),
    sg.Radio('1000', 3),
    sg.Radio('5000', 3),
    sg.Radio('10000', 3),
]])
hint_limit = sg.Frame('ヒント数下限（作成）', [[
    sg.Radio('MIN', 4, default=True),
    sg.Radio('25', 4),
    sg.Radio('30', 4),
    sg.Radio('40', 4),
    sg.Radio('50', 4),
]])
prev_next_btns = [[
    sg.Button('前へ', size=(15, 2), key='_PREV_'),
    sg.Button('次へ', size=(15, 2), key='_NEXT_'),
]]
read_make_btns = [[
    sg.Button('読込', size=(10, 2), key='_READ_'),
    sg.Button('作成', size=(10, 2), key='_MAKE_'),
]]


def raised_txt(strings):
    return sg.Text(strings, size=(15, 1), background_color='#dddddd', relief='raised')


techs = [None] * 11
techs[0] = raised_txt('CRBE')
techs[1] = raised_txt('Last Digit')
techs[2] = raised_txt('Naked Single')
techs[3] = raised_txt('Hid Single')
techs[4] = raised_txt('Naked Pair')
techs[5] = raised_txt('Hid Pair')
techs[6] = raised_txt('Naked Triple')
techs[7] = raised_txt('Hid Triple')
techs[8] = raised_txt('LC Pointing')
techs[9] = raised_txt('LC Claiming')
techs[10] = raised_txt('X-Wing')

tech = [
    [sg.Column([[
        techs[0],
    ]])],
    [sg.Column([[
        techs[1],
        techs[2],
        techs[3],
    ]])],
    [sg.Column([[
        techs[4],
        techs[5],
    ]])],
    [sg.Column([[
        techs[6],
        techs[7],
    ]])],
    [sg.Column([[
        techs[8],
        techs[9],
        techs[10],
    ]])],
]

func_btns = [
    [sg.Button('問題のコピー', size=(12, 2), key='_PRB_')],
    [sg.Button('解答のコピー', size=(12, 2), key='_ANS_')],
    [sg.Button('サムのコピー', size=(12, 2), key='_SUM_')],
]

layout = [
    [sg.Column([[
        sg.Column([[diff], [types], [num_gen], [hint_limit]]),
        sg.Frame('テクニック', tech)
    ], ])],
    [sg.Column([[
        graph,
        sg.Column([
            [sg.Frame('閲覧', [[sg.Text('----- / -----', font=('', 20), key='_NOW_')]])],
            [sg.Frame('便利ボタン', func_btns)],
            [sg.Button('解答表示', size=(12, 2), key='_SHOW_')],
            [sg.Button('問題表示', size=(12, 2), key='_BACK_')],
        ]),
    ]])],
    [sg.Column([[
        sg.Column(prev_next_btns),
        sg.Column(read_make_btns),
        sg.Button('終了', size=(8, 2), key='_END_')
    ], ])],
]
# fmt: on


window = sg.Window('', layout, finalize=True)  # no_titlebar=True,
gui.update_graph(
    window,
    graph,
    [''] * 81,
    '913913913802802802c46c46c46913913913802802802c46c46c46913913913802802802c46c46c46',
    [*map(str, range(81))],
)
read_flg = False
data_length = 0


def update(graph, gui, df, current_idx, tp_lock, is_prob=True):
    ans_set = df.loc[current_idx, 'answer']
    lines_set = df.loc[current_idx, 'lines']
    print(lines_set)
    prob_set = df.loc[current_idx, 'problem']
    techniques = df.loc[current_idx, 'technique_used']
    for i in range(len(techs)):
        techs[i].update(background_color='#dddddd', text_color='white')
        if techniques & 1 << i:
            techs[i].update(background_color='yellow', text_color='black')
    graph.Erase()
    gr = grid.Grid(np_type=tp_lock)
    gr.set_sequence(prob_set)
    gr.set_lines(lines_set)
    gr.answer = ans_set
    sums_set = (
        [''] * 81 if tp_lock != 2 else ['' if i == 0 else i for i in gr.sum_symbol]
    )
    if is_prob:
        gui.update_graph(
            window,
            graph,
            [str(i) if i != '0' else '' for i in prob_set],
            lines_set,
            sums_set,
            True if tp_lock == 1 else False,
        )
    else:
        gui.update_graph(
            window,
            graph,
            [str(i) for i in ans_set],
            lines_set,
            sums_set,
            True if tp_lock == 1 else False,
        )
    return gr


def copy_seq_to_clipboard(sequence):
    ls = []
    for i, v in enumerate(sequence):
        if i == 80:
            ls.append(str(v))
        elif i % 9 == 8:
            ls.append(str(v) + '\r\n')
        else:
            ls.append(str(v) + '\t')
    pyperclip.copy(''.join(ls))


while 1:
    event, value = window.read()
    print(event, value)
    if event == '_MAKE_':
        for i in range(5, 9):
            if value[i]:
                tp = i - 5
        for i in range(9, 14):
            if value[i]:
                sz = (10, 100, 1000, 5000, 10000)[i - 9]
        for i in range(14, 19):
            if value[i]:
                ht = (0, 25, 30, 40, 50)[i - 14]
        msg, tmp_path = edit_csv.add_to_csv(tp, sz, ht)
        sg.popup('重複確認', msg)

    if event == '_READ_':
        for i in range(5, 9):
            if value[i]:
                tp = i - 5
                tp_name = ('NOR', 'DIA', 'SUM', 'JIG')[tp]
        for i in range(5):
            if value[i]:
                diff = ('NOV', 'REG', 'EXP', 'PRO', 'MAS')[i]
        df = edit_csv.read_csv(tp_name, diff)
        if df is not False:
            tp_lock = tp
            read_flg = True
            data_length = len(df)
            print('data is found.')
            df = df.reset_index(drop=True)
            current_idx = 0
            window['_NOW_'].update(f'{current_idx+1} / {len(df)}')
            gr = update(graph, gui, df, current_idx, tp_lock)
    if event == '_SHOW_' and read_flg:
        gr = update(graph, gui, df, current_idx, tp_lock, False)
    if event == '_BACK_' and read_flg:
        gr = update(graph, gui, df, current_idx, tp_lock, True)
    if event == '_PREV_' and read_flg:
        if current_idx > 0:
            current_idx -= 1
            window['_NOW_'].update(f'{current_idx+1} / {len(df)}')
            gr = update(graph, gui, df, current_idx, tp_lock)
    if event == '_NEXT_' and read_flg:
        if current_idx < len(df) - 1:
            current_idx += 1
            window['_NOW_'].update(f'{current_idx+1} / {len(df)}')
            gr = update(graph, gui, df, current_idx, tp_lock)
    if event == '_ANS_' and read_flg:
        copy_seq_to_clipboard(df.loc[current_idx, 'answer'])
    if event == '_PRB_' and read_flg:
        copy_seq_to_clipboard(df.loc[current_idx, 'problem'])
    if event == '_SUM_' and read_flg:
        sums = (
            [''] * 81 if tp_lock != 2 else ['' if i == 0 else i for i in gr.sum_symbol]
        )
        copy_seq_to_clipboard(sums)
    if event in [None, '_END_']:
        break
window.close()
