import requests

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

