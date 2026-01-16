import pandas as pd 
from pathlib import Path
import json
from datetime import datetime

SRC=Path("data\\raw\\ipl_json_files")
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

matches=[]
for json_file in SRC.glob("*.json"):
    with open(json_file,'r') as f:
        data=json.load(f)

    event = data["info"].get("event", {})
    matchNo = event.get("match_number") or event.get("stage", "Unknown")

    date=data["info"]["dates"][0]
    year=datetime.strptime(date,"%Y-%m-%d").year
    Season=year-2007

    teams = data["info"]["teams"]
    team1 = canon(teams[0])
    team2 = canon(teams[1])

    outcome = data["info"].get("outcome", {})
    winner_raw = outcome.get("winner")
    winner = canon(winner_raw) if winner_raw else None

    win_type = None
    win_margin = None
    result_type = "normal"

    by = outcome.get("by")
    if by:
        if "runs" in by:
            win_type = "runs"
            win_margin =by["runs"]
        elif "wickets" in by:
            win_type = "wickets"
            win_margin = by["wickets"]
    else:
        result_type = outcome.get("result", "no result")

    venue=data["info"].get("venue")
    matches.append({
        "Match_No":matchNo,
        "Season":Season,
        "Team_1":team1,
        "Team_2":team2,
        "Winner":winner,
        "Win_Type": win_type,
        "Win_Margin": win_margin,
        "Result_Type":result_type,
        "Date":date,
        "Venue":venue
    })
df=pd.DataFrame(matches)
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values(by="Date").reset_index(drop=True)
print(len(df))
print(df.head())
df.to_csv("data\\processed\\matches.csv", index=False)
print("Data successfully written")