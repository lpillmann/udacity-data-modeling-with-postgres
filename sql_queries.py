
# DROP TABLES
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""
    CREATE TABLE songplays (
        songplay_id integer NOT NULL,
        start_time timestamp with time zone,
        user_id integer NOT NULL,
        level text,
        song_id integer NOT NULL,
        artist_id integer NOT NULL,
        session_id integer NOT NULL,
        location text,
        user_agent text,
        UNIQUE (
            songplay_id,
            user_id,
            song_id,
            artist_id,
            session_id
        )
    )
""")

user_table_create = ("""
    CREATE TABLE users (
        user_id integer PRIMARY KEY,
        first_name text,
        last_name text,
        gender text,
        level text
    )
""")

song_table_create = ("""
    CREATE TABLE songs (
        song_id integer PRIMARY KEY,
        title text,
        artist_id integer,
        year integer,
        duration integer
    )
""")

artist_table_create = ("""
    CREATE TABLE artists (
        artist_id integer PRIMARY KEY,
        name text,
        location text,
        latitude float,
        longitude float
    )
""")

time_table_create = ("""
    CREATE TABLE time (
        start_time timestamp with time zone,
        hour integer,
        day integer,
        week integer,
        month integer,
        year integer,
        weekday text
    )
""")

# INSERT RECORDS

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")


time_table_insert = ("""
""")

# FIND SONGS

song_select = ("""
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]