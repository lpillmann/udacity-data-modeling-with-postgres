import glob
import json
import os
import uuid

import pandas as pd
import psycopg2
from psycopg2.errors import UniqueViolation, NotNullViolation

from sql_queries import *


def execute(conn, cur, query, data):
    """Custom execute function with error handling for each transaction"""
    try:
        cur.execute(query, data)
        conn.commit()
    except UniqueViolation as e:
        # ignore duplicated records
        print(f"Failed to insert record (skipping): {repr(e)}")
        conn.rollback()
    except NotNullViolation as e:
        # ignore records whose song title is not present in songs table, hence song_id is unknown
        if 'null value in column "song_id"' in str(e):
            print(f"Failed to insert record (skipping): {repr(e)}")
            conn.rollback()
        # keep raising for other cases of NotNullViolation occurrences
        else:
            raise e


def process_song_file(conn, cur, filepath):
    """Process song file to insert songs and artists data"""
    # read contents of the file
    with open(filepath, "r") as f:
        file_contents = json.load(f)

    # open song file
    df = pd.DataFrame.from_records(data=[file_contents], columns=file_contents.keys())

    # insert song record
    song_data = df[
        ["song_id", "title", "artist_id", "year", "duration"]
    ].values.tolist()[0]
    execute(conn, cur, song_table_insert, song_data)

    # insert artist record
    artist_data = df[
        [
            "artist_id",
            "artist_name",
            "artist_location",
            "artist_latitude",
            "artist_longitude",
        ]
    ].values.tolist()[0]
    execute(conn, cur, artist_table_insert, artist_data)


def process_log_file(conn, cur, filepath):
    """Process log file to insert time, users and songplays data"""
    # open log file
    file_contents = [json.loads(line) for line in open(filepath, "r")]
    df = pd.DataFrame.from_records(data=file_contents, columns=file_contents[0].keys())

    # filter by NextSong action and convert timestamp column to datetime
    df = df.query("page == 'NextSong'").assign(
        ts=lambda x: pd.to_datetime(x["ts"], unit="ms")
    )

    # build time dataframe from timestamp column
    time_df = (
        df["ts"]
        .to_frame()
        .rename(columns={"ts": "start_time"})
        .assign(hour=lambda x: x["start_time"].dt.hour)
        .assign(day=lambda x: x["start_time"].dt.day)
        .assign(week=lambda x: x["start_time"].dt.isocalendar().week)
        .assign(month=lambda x: x["start_time"].dt.month)
        .assign(year=lambda x: x["start_time"].dt.year)
        .assign(weekday=lambda x: x["start_time"].dt.weekday)
    )

    # insert time data records
    for _, row in time_df.iterrows():
        execute(conn, cur, time_table_insert, list(row))

    # load user table
    user_df = df[
        ["userId", "firstName", "lastName", "gender", "level"]
    ].drop_duplicates()

    # insert user records
    for _, row in user_df.iterrows():
        execute(conn, cur, user_table_insert, row)

    # insert songplay records
    for _, row in df.iterrows():

        # get songid and artistid from song and artist tables
        execute(conn, cur, song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (
            str(uuid.uuid4()),
            pd.to_datetime(row["ts"], unit="ms"),
            row["userId"],
            row["level"],
            songid,
            artistid,
            row["sessionId"],
            row["location"],
            row["userAgent"],
        )
        execute(conn, cur, songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """Generic caller function that gets all available files and calls desired process function to them in a loop"""
    # get all files matching extension from directory
    all_files = []
    for root, _, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, "*.json"))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print("{} files found in {}".format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(conn, cur, datafile)
        # conn.commit()
        print("{}/{} files processed.".format(i, num_files))


def main():
    """Scrip entrypoint"""
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=sparkifydb user=postgres password=1234"
    )
    cur = conn.cursor()

    process_data(cur, conn, filepath="data/song_data", func=process_song_file)
    process_data(cur, conn, filepath="data/log_data", func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
