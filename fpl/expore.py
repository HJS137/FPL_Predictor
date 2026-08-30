import requests
import sqlite3

data  = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()


print(data.keys())


# -- Whats in each top level key --
print("===Top Level Keys===")

for key in data.keys():
    value = data[key]
    size = len(value) if isinstance(value, list) else value
    print(f"{key:<20} : {size}")

# --- How many players ? ---

players = data['elements']
print("===Players===")
print(f"Number of players: {len(players)}")

# --- Every field for one player ---
player  = players[0]
print("\n===One Player===")
for field, value in player.items():
    print(f"{field:<40} : {value}")

# - - - position mapping, from the data not from memopry--

positions = {} # this is going to be a data dicitonary
for et in data["element_types"]:
    positions[et["id"]] = et["singular_name_short"]


print("\n===Position Mapping===")
print(positions)
print("this player is a:", positions[player["element_type"]])



###----Designing the Schema---###

conn = sqlite3.connect("fpl.db")


# --- create the table -----------------------------------------------
conn.execute("""
CREATE TABLE IF NOT EXISTS teams (
    team_id                 INTEGER PRIMARY KEY,
    name                    TEXT,
    short_name              TEXT,
    strength_attack_home    INTEGER,
    strength_attack_away    INTEGER,
    strength_defence_home   INTEGER,
    strength_defence_away   INTEGER
)
""")

# ---- load the rows -------
for team in data["teams"]:                        # BLANK 1
    conn.execute(
        "INSERT OR REPLACE INTO teams VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            team["id"],
            team["name"],
            team["short_name"],
            team["strength_attack_home"],
            team["strength_attack_away"],
            team["strength_defence_home"],                        # BLANK 2
            team["strength_defence_away"],
        )
    )

conn.commit()

# --- read it back ---------------------------------------------------
rows = conn.execute("""
    SELECT name, strength_attack_home, strength_defence_home
    FROM teams
    ORDER BY strength_attack_home DESC
    LIMIT 5
""").fetchall()

print("Strongest attacks at home:")
for row in rows:
    print(row)



print(data["teams"][0])


# --- players table --------------------------------------------------
conn.execute("""
CREATE TABLE IF NOT EXISTS players (
    player_id   INTEGER PRIMARY KEY,
    web_name    TEXT,
    first_name  TEXT,
    second_name TEXT,
    team_id     INTEGER,
    position    TEXT
)
""")


positions = {}
for et in data["element_types"]:
    positions[et["id"]] = et["singular_name_short"]

for p in data["elements"]:
    conn.execute(
        "INSERT OR REPLACE INTO players VALUES (?, ?, ?, ?, ?, ?)",
        (
            p["id"],
            p["web_name"],
            p["first_name"],
            p["second_name"],
            p["team"],                    # BLANK 1
            positions[p["element_type"]],         # BLANK 2
        )
    )

conn.commit()


### - query

rows = conn.execute("""
    SELECT players.web_name, players.position, teams.short_name
    FROM players
    JOIN teams ON players.team_id = teams.team_id
    WHERE players.position = 'GKP'
    LIMIT 10
""").fetchall()

for row in rows:
    print(row)



#### -  - - -Snapshots

from datetime import datetime, timezone

conn.execute("""
CREATE TABLE IF NOT EXISTS player_snapshots (
    snapshot_ts                     TEXT,
    player_id                       INTEGER,
    now_cost                        INTEGER,
    status                          TEXT,
    news                            TEXT,
    chance_of_playing_next_round    INTEGER,
    selected_by_percent             REAL,
    form                            REAL,
    ep_next                         REAL,
    transfers_in_event              INTEGER,
    transfers_out_event             INTEGER,
    PRIMARY KEY (snapshot_ts, player_id)
)
""")

stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

for p in data["elements"]:
    conn.execute(
        "INSERT OR REPLACE INTO player_snapshots VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            stamp,
            p["id"],
            p["now_cost"],
            p["status"],
            p["news"],
            p["chance_of_playing_next_round"],
            p["selected_by_percent"],
            p["form"],
            p["ep_next"],
            p["transfers_in_event"],
            p["transfers_out_event"],
        )
    )

conn.commit()

#### Query Check - everyone that is currently flagged 


rows = conn.execute("""
    SELECT p.web_name, s.status, s.chance_of_playing_next_round, s.news
    FROM player_snapshots s
    JOIN players p ON p.player_id = s.player_id
    WHERE s.status != 'a'
    LIMIT 15
""").fetchall()

for row in rows:
    print(row)



