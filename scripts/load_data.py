import sqlite3
import os
from contextlib import closing
import sys
import pandas as pd

SOURCE = os.path.abspath(__file__)
PARENT = os.path.abspath(os.path.join(SOURCE, '..', '..'))
DB = 'starry.db'


def check_directory():  # eventually add logic to allow user to input path if directory changed
    try:
        assert os.path.basename(PARENT) == 'take-home-assignment'
    except AssertionError:
        print('It looks like the directory structure has changed. Please see the README and make sure your structure '
              'matches the directory shown.')
        sys.exit()


def compile_csvs():
    _csvs = []
    _data = os.path.join(PARENT, 'data')
    for _root, _dir, _files in os.walk(_data):
        print(f'--{len(_files)} CSVs found in \'data\' directory.')
        for _f in _files:
            _csvs.append(os.path.join(_root, _f))
    return _csvs


def create_table():
    with closing(sqlite3.connect(DB)) as _connection:
        with closing(_connection.cursor()) as _cursor:
            _cursor.execute('''
            CREATE TABLE IF NOT EXISTS starry
            ([id] INTEGER PRIMARY KEY, [dt] INTEGER, [val] FLOAT, [category_1] TEXT, [category_2] TEXT);
            ''')
    print('--\'starry\' table created.')


def csv_vals():
    _vals = []
    for _csv in compile_csvs():  # eventually add check for null data, invalid types, etc.
        _df = pd.read_csv(_csv, dtype={'id': int, 'dt': float, 'val': float, 'category_1': str, 'category_2': str})
        for _ix, _row in _df.iterrows():
            _vals.append(_row.to_list())  # store values in a list
    return _vals


if __name__ == '__main__':
    check_directory()  # check file structure
    create_table()  # create table

    with closing(sqlite3.connect(DB)) as connection:  # upsert values from csv
        with closing(connection.cursor()) as cursor:
            for _id, _dt, _val, _cat_1, _cat_2 in csv_vals():
                cursor.execute('''INSERT INTO starry VALUES (?, ?, ?, ?, ?) 
                                ON CONFLICT (id) DO UPDATE SET dt = ?, val = ?, category_1 = ?, category_2 = ? WHERE dt < ?;''',
                               (_id, _dt, _val, _cat_1, _cat_2, _dt, _val, _cat_1, _cat_2, _dt)
                               )
            rows = cursor.execute('SELECT * FROM starry')

            print('Row count: ', len([r for r in rows]))

        connection.commit()

    print('Done.')






