# Data Modeling with Postgres
This repository contains the code for the first project in Udacity's Data Engineering Nanodegree program.

## Overview
The project consists of extracting data from JSON files and load them into a Postgres database, modeling in a star schema with a fact table for **songplays** and several dimensions for **songs**, **artists**, **users** and **time**.

Below the repository structure and files are described:
```
.
├── create_tables.py     -> Initial script to create database and tables
├── data                 -> Repository with raw data in JSON format
│   ├── log_data         -> Logs of requests
│   └── song_data        -> Descriptive data about songs, artists, albums, etc
├── etl.ipynb            -> Notebook to prototype and test core ETL transformations
├── etl.py               -> Script to run the actual ETL process for all files
├── poetry.lock          -> Poetry frozen set of dependencies
├── pyproject.toml       -> Poetry project and dependencies description
├── README.md            -> Intro to project and how to use (this file you are reading)
├── sql_queries.py       -> Declaration of CREATE, DROP and INSERT query templates
└── test.ipynb           -> Test notebook to query all tables and see their contents
```

# How to use
## Install
The project uses [`poetry`](https://python-poetry.org/) as package manager. You need to have it installed before proceeding.

```bash
poetry install
```

## Run
**NOTE**: Before running, make sure you have a local Postgres database running with database `studentdb` with credentials user `student` and password `student`.

1. Activate environment
```bash
poetry shell
```

2. Create tables
```bash
python create_tables.py
```

3. Extract, transform and load data
```bash
python etl.py
```

4. Check results
    1. Run JupyterLab
    ```bash
    jupyter lab
    ```
    2. Open `test.ipynb`
    3. Click _Kernel > Restart Kernel and Run All Cells_ to run all cells after a fresh start
    4. Verify results. All tables should be populated. The table `songplays` is expected to have only one record.

# Changes to template code
Below is a list of changes performed on the code template provided.

- Simplified transformation steps to create `time_df` in `etl.py`, by using pandas method chaining with suggested `dt` accessor
- Error handling at the transaction level in `etl.py`. The template code would only commit at the end of `process_data()`, but since errors happened during the execution (e.g. uniqueness or not null constraints violated), it was not possible to proceed without rolling back all steps. To solve that, I've implemented the `execute()` method that treats each execution individually and handles known exceptions, printing the information on the screen for visibility. With that, I was able to successfully insert the "good" records while responsibly ignoring bad quality (or repeated) data.
