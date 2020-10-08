import csv
import pandas as pd
import itertools
import PySimpleGUI as sg
import sys
from pathlib import Path
from grid import Grid
from datetime import datetime
import os


def mypath():
    return Path(sys.argv[0]).parent if hasattr(sys, "frozen") else Path(__file__).parent


def get_add_df(problem_type, num_to_make, hints_limit, window):

    dict_list = []
    for i in range(num_to_make):
        grid = Grid(np_type=problem_type)
        grid.create()
        grid.create_problem(hints_limit)
        dic_to_write = {
            'created_on': str(grid.creation_datetime),
            'difficulty': str(grid.difficulty),
            'type': str(grid.type_str),
            'hints': f'{grid.count_digits():02d}',
            'answer': str(grid.answer),
            'problem': str(grid.problem),
            'lines': str(grid.lines),
            'technique_used': str(grid.used_techniques),
            'uploaded': '0',
        }
        dict_list.append(dic_to_write)
        del grid
        window["progbar"].update_bar(i + 1)

    return pd.DataFrame.from_dict(dict_list)


def rotate(grid):
    if type(grid) is str:
        grid = [int(i) for i in grid]

    def get_other_pattern_index():
        pattern = [(i // 9, i % 9, 8 - i // 9, 8 - i % 9) for i in range(81)]
        indexes = []
        pairs = [(i, j) for i, j in itertools.permutations(range(4), 2) if (i ^ j) & 1]
        for row, column in pairs:
            indexes += ([grid[i[row] * 9 + i[column]] for i in pattern],)
        return indexes

    grids = []
    for i in get_other_pattern_index():
        grids += (''.join(map(str, i)),)

    return grids


def get_progress_window(num):
    layout = [
        [sg.Text("生成中…", font=('Courier', 20))],
        [sg.ProgressBar(num, orientation="h", size=(40, 40), key="progbar")],
    ]
    return sg.Window("ナンプレメーカー", layout)


def add_to_csv(problem_type=0, num_to_make=10, hints_limit=0, filename='np_data.csv'):

    window = get_progress_window(num_to_make)
    window.read(timeout=0)

    add_df = get_add_df(problem_type, num_to_make, hints_limit, window)
    count = 0
    if os.path.isfile(mypath() / filename):
        old_df = pd.read_csv(
            mypath() / filename,
            header=0,
            encoding='utf-8',
            index_col=0,
            dtype={'technique_used': str},
        )
        for i, answer in enumerate(add_df['answer']):
            rotates = rotate(answer)
            for old_answer in old_df['answer']:
                if old_answer in rotates:
                    count += 1
                    add_df = add_df.drop(index=i)

        if 1:
            add_df.to_csv(
                mypath() / f'np_{datetime.now():%y%m%d_%H%M%S}.csv',
                mode='w',
                quoting=csv.QUOTE_ALL,
            )
        new_df = pd.concat([old_df, add_df])
        new_df = new_df.reset_index(drop=True)
    else:
        new_df = add_df
    msg = f'{count}個の問題が重複しました'

    new_df.to_csv(
        mypath() / filename,
        mode='w',
        quoting=csv.QUOTE_ALL,
    )
    window.close()
    return msg


def read_csv(tp, diff, filename='np_data.csv'):
    if os.path.isfile(mypath() / filename):
        df_read = pd.read_csv(
            mypath() / filename,
            header=0,
            encoding='utf-8',
        )
        df_type_groupby = df_read.groupby('type')
        for key, _ in df_type_groupby:
            if key == tp:
                df_type_filtered = df_type_groupby.get_group(tp)
                df_diff_groupby = df_type_filtered.groupby('difficulty')
                for key_, _ in df_diff_groupby:
                    if key_ == diff:
                        df_diff_filtered = df_diff_groupby.get_group(diff)
                        sg.popup(f'{len(df_diff_filtered)}件見つかりました')
                        return df_diff_filtered
                sg.popup_error('指定した難易度の問題はデータにありません')
                return False
        sg.popup_error('指定した種類の問題はデータにありません')
        return False
    else:
        return False
