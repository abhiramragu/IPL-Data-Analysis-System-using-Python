import pandas as pd
from pathlib import Path
import json
from datetime import datetime

SRC = Path("data\\raw\\ipl_json_files")

TEAM_CANONICAL = {
    "royal challengers bangalore": "rcb",
    "royal challengers bengaluru": "rcb",
    "rcb": "rcb",

    "chennai super kings": "csk",
    "csk": "csk",

    "mumbai indians": "mi",
    "mi": "mi",

    "kolkata knight riders": "kkr",
    "kkr": "kkr",

    "rajasthan royals": "rr",
    "rr": "rr",

    "sunrisers hyderabad": "srh",
    "srh": "srh",

    "delhi daredevils": "dc",
    "delhi capitals": "dc",
    "dc": "dc",
    "dd": "dc",

    "kings xi punjab": "pk",
    "punjab kings": "pk",
    "pk": "pk",
    "kxip": "pk",

    "gujarat titans": "gt",
    "gt": "gt",

    "gujarat lions": "gl",
    "gl": "gl",

    "rising pune supergiant": "rps",
    "rising pune supergiants": "rps",
    "rps": "rps",

    "pune warriors": "pw",
    "pw": "pw",

    "kochi tuskers kerala": "ktk",
    "ktk": "ktk",

    "deccan chargers": "dcg",
    "dcg": "dcg",

    "lucknow super giants": "lsg",
    "lsg": "lsg"
}

def canon(team):
    if team is None:
        return None
    key = team.lower().strip()
    return TEAM_CANONICAL.get(key)

players_rows = []

for json_file in SRC.glob("*.json"):
    with open(json_file, "r") as f:
        data = json.load(f)

    # --- match info ---
    match_id = int(json_file.stem)
    date = data["info"]["dates"][0]
    year = datetime.strptime(date, "%Y-%m-%d").year
    season = year - 2007

    # --- build team map  ---
    player_team_map = {}
    for team_name, team_players in data["info"]["players"].items():
        team_code = canon(team_name)
        for p in team_players:
            player_team_map[p] = team_code

    # --- initialize stats ---
    player_stats = {}
    for p in player_team_map:
        player_stats[p] = {
            "runs": 0,
            "balls_faced": 0,
            "fours": 0,
            "sixes": 0,
            "wickets": 0,
            "balls_bowled": 0,
            "runs_conceded": 0
        }


    # --- process deliveries ---
    for inning in data["innings"]:
        for over in inning["overs"]:
            for d in over["deliveries"]:

                batter = d["batter"]
                bowler = d["bowler"]
                runs = d["runs"]["batter"]
                total_runs = d["runs"]["total"]
                extras = d.get("extras", {})

                # batting
                if "wides" not in extras and "noballs" not in extras:
                    player_stats[batter]["balls_faced"] += 1

                player_stats[batter]["runs"] += runs
                if runs == 4:
                    player_stats[batter]["fours"] += 1
                elif runs == 6:
                    player_stats[batter]["sixes"] += 1

                # bowling
                if "byes" not in extras and "legbyes" not in extras:
                    player_stats[bowler]["runs_conceded"] += total_runs

                if "wides" not in extras:
                    player_stats[bowler]["balls_bowled"] += 1

                # wickets
                for w in d.get("wickets", []):
                    if w["kind"] != "run out":
                        player_stats[bowler]["wickets"] += 1

    # --- append rows ---
    for player, stats in player_stats.items():
        players_rows.append({
            "match_id": match_id,
            "season": season,
            "team": player_team_map[player],
            "player": player,
            **stats
        })

# --- DataFrame ---
df_players = pd.DataFrame(players_rows)
df_players["overs_display"]=(df_players["balls_bowled"] // 6) + (df_players["balls_bowled"] % 6) / 10
df_players["overs_math"]=(df_players["balls_bowled"]/6).round(2)
df_players["strike_rate"] = (
    df_players["runs"]
    .div(df_players["balls_faced"])
    .mul(100)
    .round(2)
)
df_players.loc[df_players["balls_faced"] == 0, "strike_rate"] = 0
df_players["economy"] = round(df_players["runs_conceded"] / df_players["overs_math"],2)
df_players.loc[df_players["overs_math"] == 0, "economy"] = 0

cols=list(df_players.columns)
cols.remove("strike_rate")
wickets_index = cols.index("wickets")
cols.insert(wickets_index, "strike_rate")
df_players = df_players[cols]
print(df_players.columns)
print(df_players.head())
print(df_players.shape)
print(df_players.isna().sum())
df_players.to_csv("data\\processed\\players_stats.csv",index=False)
print("Data successfully written ")