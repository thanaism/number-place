import csv
import pandas as pd
import sys
from pathlib import Path
import os


def mypath():
    return Path(sys.argv[0]).parent if hasattr(sys, "frozen") else Path(__file__).parent


def add_reindex_csv(filename='test.csv'):
    dict_list = []
    for _ in range(3):
        dic_to_write = {
            'l1': 'a',
            'l2': 'j',
        }
        dict_list.append(dic_to_write)
    add_df = pd.DataFrame.from_dict(dict_list)
    add_df.info()
    if os.path.isfile(mypath() / filename):
        old_df = pd.read_csv(
            mypath() / filename,
            header=0,
            encoding='utf-8',
            index_col=0,
        )
        new_df = pd.concat([old_df, add_df])
        new_df = new_df.reset_index(drop=True)
    else:
        new_df = add_df

    new_df.to_csv(
        mypath() / filename,
        mode='w',
        quoting=csv.QUOTE_ALL,
    )


add_reindex_csv()