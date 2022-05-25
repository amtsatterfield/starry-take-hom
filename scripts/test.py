import unittest
import load_data
import os
from contextlib import closing
import sqlite3


class MyTestCase(unittest.TestCase):
    def test_path(self):
        assert os.path.exists(load_data.SOURCE)
        print(f'script path: {load_data.SOURCE}')

        parent_dir = os.path.abspath(os.path.join(load_data.SOURCE, '..', '..'))
        assert os.path.basename(parent_dir) == 'take-home-assignment'
        print(f'parent path: {parent_dir}')

    def test_db(self):
        with closing(sqlite3.connect(load_data.DB)) as connection:
            assert os.path.isfile(load_data.DB)
            print('DB connection has been created.')

    def test_table(self):
        with closing(sqlite3.connect(load_data.DB)) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute('''CREATE TABLE IF NOT EXISTS starry 
                                ([id] INTEGER PRIMARY KEY, [dt] INTEGER, [val] FLOAT, [category_1] TEXT, [category2] TEXT)''')
                tables = cursor.execute('SELECT name FROM sqlite_master WHERE type = "table"')
                print([t for t in tables])
                print('starry table present.')

    def test_vals(self):
        with closing(sqlite3.connect(load_data.DB)) as connection:
            with closing(connection.cursor()) as cursor:
                for _id, _dt, _val, _cat_1, _cat_2 in load_data.csv_vals():
                    cursor.execute(
                        '''INSERT INTO starry VALUES (?, ?, ?, ?, ?) 
                           ON CONFLICT (id) DO UPDATE SET dt = ?, val = ?, category_1 = ?, category2 = ? WHERE dt < ?;''',
                        (_id, _dt, _val, _cat_1, _cat_2, _dt, _val, _cat_1, _cat_2, _dt)
                    )

                rows = cursor.execute("SELECT * FROM starry")
                vals = [r for r in rows]
        assert len(vals) > 0
        print('values updated.')


if __name__ == '__main__':
    unittest.main()
