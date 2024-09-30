# UKSI Importer

## Installation

This tool requires [mdb-tools](https://github.com/mdbtools/mdbtools) to be installed.
Specifically, this tool uses the following CLI utilities provided by this lib:

- `mdb-tables`
- `mdb-json`

Then for local use:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

## Usage

Assuming installation into .venv:

```bash
uksi create_db <access-db-path> uksi.db
```
