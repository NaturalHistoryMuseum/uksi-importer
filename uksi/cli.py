from pathlib import Path

import click

from uksi.db import make_db


@click.group()
def cli():
    pass


@cli.command("create_db")
@click.argument(
    "access_db", type=click.Path(exists=True, dir_okay=False, path_type=Path)
)
@click.argument("sqlite_db", type=click.Path(dir_okay=False, path_type=Path))
def create_db(access_db: Path, sqlite_db: Path):
    """
    Given an access database, creates an SQLite database with the same data in it.

    :param access_db: Path to the access database
    :param sqlite_db: Path to the SQLite database (if a file exists here it will be
                      deleted before loading)
    """
    make_db(access_db, sqlite_db)


if __name__ == "__main__":
    cli()
