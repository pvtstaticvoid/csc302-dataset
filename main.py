import sqlite3
import os
import json

# Setup database.
try:
    os.remove("database.db")
except:
    pass
con = sqlite3.connect("database.db")
cur = con.cursor()

# Load a small slice of the actual dataset.
with open("dataset_small.json", "r") as read_file:
    data_small = json.load(read_file)

# Create tables.
cur.execute("CREATE TABLE playlists(name, pid, num_tracks, num_albums, num_followers)")
cur.execute("CREATE TABLE songs(artist_name, track_uri, artist_uri, track_name, album_uri, duration_ms, album_name)")
cur.execute("CREATE TABLE songs_in_playlists(pid, track_uri)")

# Fill the "playlists" table.
for pl in data_small["playlists"]:
    cur.execute(f"INSERT INTO playlists VALUES (?, ?, ?, ?, ?)",
                (pl["name"], pl["pid"], pl["num_tracks"], pl["num_albums"], pl["num_followers"]))

# Fill the "songs" and "songs_in_playlists" tables.
songs = set()
for pl in data_small["playlists"]:
    for song in pl["tracks"]:
        cur.execute(f"INSERT INTO songs_in_playlists VALUES (?, ?)",
                    (pl["pid"], song["track_uri"]))
        songs.add(
            (song["artist_name"],
             song["track_uri"],
             song["artist_uri"],
             song["track_name"],
             song["album_uri"],
             song["duration_ms"],
             song["album_name"]))
# ...
for song in songs:
    cur.execute(f"INSERT INTO songs VALUES (?, ?, ?, ?, ?, ?, ?)",
                song)

# Commit our changes to disk.
con.commit()

# Make a sample query.
res = cur.execute("SELECT avg(num_tracks) FROM playlists WHERE num_followers > 10")
print(f"The average number of tracks in playlists with more than 10 followers is {res.fetchone()[0]}.")