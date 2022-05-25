import argparse
import csv
import sys
from pathlib import Path
import random
import time
import typing as t
import os


def cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Use this module to generate random-ish data')
    parser.add_argument('--fp', '--out-file', dest="dest", type=Path, help="Name of the file to create")
    parser.add_argument('-n', '--rows', dest="rows", type=int, default=1000, help="Number of rows to write")
    parser.add_argument('--seed', dest="seed", help="Control randomness by specifying a static value")
    args = parser.parse_args()
    return args


def generate_data(
    *,
    dest: t.Optional[Path] = None,
    rows: int = 1000,
    seed: t.Optional[t.Union[int, float, str, bytes, bytearray]] = None
) -> None:
    if seed:
        random.seed(seed)

    if dest:
        try:
            assert os.path.isfile(dest)
        except AssertionError:
            print("Please include the filename of a csv in your path.")
        sys.exit()

    with open(dest or Path(f"data_{int(time.time())}.csv"), "w", newline='') as fout:  # windows default text mode writes /r/r/n
        writer = csv.writer(fout, delimiter=",")
        writer.writerow(["id", "dt", "val", "category_1", "category_2"])
        for _ in range(rows):
            writer.writerow([random.randint(1, 10000), time.time(), random.random(), random.choice("abcde"), random.choice("abcde")])


if __name__ == '__main__':
    params = cli()
    generate_data(dest=params.dest, rows=params.rows, seed=params.seed)
