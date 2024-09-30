import json
import subprocess
from contextlib import closing
from pathlib import Path
from typing import Iterable

import dataset

from uksi.utils import batched, log, open_db


def get_tables(db_file: Path) -> list[str]:
    """
    Returns the list of table names available in the database.

    :param db_file: the Path to the access database
    :return: a list of table names
    """
    result = subprocess.run(
        ["mdb-tables", db_file.resolve()], capture_output=True, text=True
    )
    return [table.strip() for table in result.stdout.split()]


def read_rows(db_file: Path, table_name: str) -> Iterable[dict]:
    """
    Given a database and a table name, yields the rows in the database one by one as
    dicts.

    :param db_file: the Path to the access database
    :param table_name: the table name
    :return: yields row dicts
    """
    proc = subprocess.Popen(
        [
            "mdb-json",
            db_file.resolve(),
            table_name,
            "--date-format=%Y-%m-%d",
            "--datetime-format=%Y-%m-%dT%H:%M:%S",
        ],
        stdout=subprocess.PIPE,
    )
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        yield json.loads(line)


def make_db(source: Path, target: Path):
    """
    Reads all data from the access database at the source Path and writes it into a new
    SQLite database at the target Path.
    """
    target.unlink(missing_ok=True)
    for extra in ["shm", "wal"]:
        target.with_name(f"{target.name}-{extra}").unlink(missing_ok=True)

    with open_db(target) as db:
        for table_name in get_tables(source):
            table = db.create_table(table_name, primary_id="_id")
            count = 0
            log(f"Loading {table_name}...", fg="blue")
            for chunk in batched(read_rows(source, table_name), 10_000):
                table.insert_many(chunk, chunk_size=1000)
                count += len(chunk)
            if count > 0:
                log(f"Loaded {count} rows into {table_name}", fg="cyan")
            else:
                table.drop()
                log(f"No data in {table_name}, ignoring", fg="yellow")
        db.query("vacuum")

    log(f"Done", fg="green")
