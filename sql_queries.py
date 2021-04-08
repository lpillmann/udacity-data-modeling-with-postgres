# DROP TABLES
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = """
    CREATE TABLE songplays (
        songplay_id text NOT NULL,
        start_time timestamp with time zone,
        user_id text NOT NULL,
        level text,
        song_id text NOT NULL,
        artist_id text NOT NULL,
        session_id text NOT NULL,
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
"""

user_table_create = """
    CREATE TABLE users (
        user_id text PRIMARY KEY,
        first_name text,
        last_name text,
        gender text,
        level text
    )
"""

song_table_create = """
    CREATE TABLE songs (
        song_id text PRIMARY KEY,
        title text,
        artist_id text,
        year integer,
        duration float
    )
"""

artist_table_create = """
    CREATE TABLE artists (
        artist_id text PRIMARY KEY,
        name text,
        location text,
        latitude float,
        longitude float
    )
"""

time_table_create = """
    CREATE TABLE time (
        start_time timestamp with time zone,
        hour integer,
        day integer,
        week integer,
        month integer,
        year integer,
        weekday text
    )
"""

# INSERT RECORDS

songplay_table_insert = """
    INSERT INTO songplays (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

user_table_insert = """
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    VALUES (%s, %s, %s, %s, %s)
"""

song_table_insert = """
    INSERT INTO songs (song_id, title, artist_id, year, duration) 
    VALUES (%s, %s, %s, %s, %s)
"""

artist_table_insert = """
    INSERT INTO artists (artist_id, name, location, latitude, longitude) 
    VALUES (%s, %s, %s, %s, %s)
"""


time_table_insert = """
    INSERT INTO time (start_time, hour, day, week, month, year, weekday) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

# FIND SONGS

song_select = """
    select
        s.song_id,
        a.artist_id
    from
        songs s
        inner join
        artists a on s.artist_id = a.artist_id
    where
        s.title = %s
        and
        a.name = %s
        and
        s.duration = %s
"""

# QUERY LISTS

create_table_queries = [
    songplay_table_create,
    user_table_create,
    song_table_create,
    artist_table_create,
    time_table_create,
]
drop_table_queries = [
    songplay_table_drop,
    user_table_drop,
    song_table_drop,
    artist_table_drop,
    time_table_drop,
]
