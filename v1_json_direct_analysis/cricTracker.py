import json
from pathlib import Path
from datetime import datetime

SRC = Path("data\\raw\\ipl_json_files")
MATCHES = []
for json_file in SRC.glob("*.json"):
    with open(json_file, "r") as f:
        MATCHES.append(json.load(f))
# teams=set()
TEAM_CANONICAL = {
    # Royal Challengers Bangalore / Bengaluru
    "royal challengers bangalore": "rcb",
    "royal challengers bengaluru": "rcb",
    "rcb": "rcb",

    # Chennai Super Kings
    "chennai super kings": "csk",
    "csk": "csk",

    # Mumbai Indians
    "mumbai indians": "mi",
    "mi": "mi",

    # Kolkata Knight Riders
    "kolkata knight riders": "kkr",
    "kkr": "kkr",

    # Rajasthan Royals
    "rajasthan royals": "rr",
    "rr": "rr",

    # Sunrisers Hyderabad
    "sunrisers hyderabad": "srh",
    "srh": "srh",

    # Delhi Daredevils / Delhi Capitals
    "delhi daredevils": "dc",
    "delhi capitals": "dc",
    "dc": "dc",
    "dd": "dc",

    # Kings XI Punjab / Punjab Kings
    "kings xi punjab": "pk",
    "punjab kings": "pk",
    "pk": "pk",
    "kxip": "pk",

    # Gujarat Titans
    "gujarat titans": "gt",
    "gt": "gt",

    # Gujarat Lions
    "gujarat lions": "gl",
    "gl": "gl",

    # Rising Pune Supergiant(s)
    "rising pune supergiant": "rps",
    "rising pune supergiants": "rps",
    "rps": "rps",

    # Pune Warriors
    "pune warriors": "pw",
    "pw": "pw",

    # Kochi Tuskers Kerala
    "kochi tuskers kerala": "ktk",
    "ktk": "ktk",

    # Deccan Chargers
    "deccan chargers": "dcg",
    "dcg": "dcg",

    # Lucknow Super Giants
    "lucknow super giants": "lsg",
    "lsg": "lsg"
}

PW=RCB=SRH=GL=KKR=DC=PK=MI=D=LSG=RR=RPS=CSK=KTK=GT=count=0
def total_wins():
    global PW, RCB, SRH, GL, KKR, DC, PK, MI, D, LSG, RR, RPS, CSK, KTK, GT, count

    for data in MATCHES:

        count+=1
        outcome = data["info"].get("outcome", {})
        winner=outcome.get("winner")

        if winner is None:
            continue

        if winner == 'Gujarat Titans':
            GT += 1
        elif winner in {'Rising Pune Supergiant', 'Rising Pune Supergiants'}:
            RPS += 1
        elif winner == 'Kochi Tuskers Kerala':
            KTK += 1
        elif winner == 'Chennai Super Kings':
            CSK += 1
        elif winner in {'Royal Challengers Bengaluru', 'Royal Challengers Bangalore'}:
            RCB += 1
        elif winner == 'Pune Warriors':
            PW += 1
        elif winner == 'Sunrisers Hyderabad':
            SRH += 1
        elif winner == 'Gujarat Lions':
            GL += 1
        elif winner == 'Kolkata Knight Riders':
            KKR += 1
        elif winner in {'Delhi Capitals', 'Delhi Daredevils'}:
            DC += 1
        elif winner in {'Punjab Kings', 'Kings XI Punjab'}:
            PK += 1
        elif winner == 'Deccan Chargers':
            D += 1
        elif winner == 'Rajasthan Royals':
            RR += 1
        elif winner == 'Mumbai Indians':
            MI += 1
    # teams.add(data["info"]["teams"][0])
    # teams.add(data["info"]["teams"][1])
def team_wins_per_season(team,season):
    wins=0
    for data in MATCHES:
        outcome = data["info"].get("outcome", {})
        winner=outcome.get("winner")
        date=data["info"]["dates"]
        dt=datetime.strptime(date[0],"%Y-%m-%d")
        year=dt.year

        if winner is None:
            continue
        if TEAM_CANONICAL.get(winner.lower()) == TEAM_CANONICAL.get(team.lower()) and year == 2007 + season:
            wins+=1
            
    return wins
def points_table(season):
    matches_played = {}
    wins = {}
    losses = {}
    no_result = {}
    points={}
    for data in MATCHES:

        date = data["info"]["dates"]
        dt = datetime.strptime(date[0], "%Y-%m-%d")
        year = dt.year

        if year != 2007 + season:
            continue
        
        if len(data["innings"]) != 2:
            continue 
        event = data.get("info", {}).get("event", {})

        stage = event.get("stage")

        if stage in {"Final", "Qualifier", "Eliminator", "Super Over"}:
            continue
        teams = data["info"]["teams"]
        team_keys = []

        for t in teams:
            key = TEAM_CANONICAL.get(t.lower())
            if key is not None:
                team_keys.append(key)
                matches_played[key] = matches_played.get(key, 0) + 1

        outcome = data["info"].get("outcome", {})
        winner = outcome.get("winner")

        # No result / abandoned / tie
        if winner is None:
            for key in team_keys:
                no_result[key] = no_result.get(key, 0) + 1
            continue

        winner_key = TEAM_CANONICAL.get(winner.lower())

        if winner_key is not None:
            wins[winner_key] = wins.get(winner_key, 0) + 1

            for key in team_keys:
                if key != winner_key:
                    losses[key] = losses.get(key, 0) + 1
    for team in matches_played:
        points[team] = wins.get(team, 0) * 2 + no_result.get(team, 0)
    print(f"-------------------Points table IPL season {season}-------------------")
    print("Teams\tMatches\tWins\tLose\tNR\tPoints")
    for team in sorted(matches_played, key=lambda t: wins.get(t,0), reverse=True):
        print(f"{team.upper()}\t{matches_played.get(team, 0)}\t{wins.get(team, 0)}\t{losses.get(team, 0)}\t{no_result.get(team, 0)}\t{points.get(team, 0)}")

def player_in_team(player,season):
    team_name = None
    player = player.lower()

    for data in MATCHES:
        players = data["info"]["players"]
        dt = datetime.strptime(data["info"]["dates"][0], "%Y-%m-%d")
        year = dt.year

        if year != 2007 + season:
            continue

        for team in players:
            for pl in players[team]:
                if pl.lower() == player:  
                    team_name = team
                    return team_name

    return team_name

def runs_scored(player,season):
    runs=0
    seasons = range(1, 19) if season == 0 else [season]
    for s in seasons:
        team = player_in_team(player, s)
        if team is None:
            continue
        for data in MATCHES:
            date=data["info"]["dates"]
            dt=datetime.strptime(date[0],"%Y-%m-%d")
            year=dt.year
            if year != 2007 + s:
                continue
            for i in data["innings"]:
                if TEAM_CANONICAL.get(i["team"].lower()) == TEAM_CANONICAL.get(team.lower()):
                    overs=i["overs"]
                    for j in overs:
                        delivery=j["deliveries"]
                        for k in delivery:
                            if k.get("batter", "").lower() == player.lower():
                                runs+=k["runs"]["batter"]
    return runs
                
def wickets_taken(player,season):
    wickets=0
    seasons = range(1, 19) if season == 0 else [season]
    non_bowler_kinds = {"run out", "retired hurt", "obstructing the field"}
    for s in seasons:
        team = player_in_team(player, s)
        if team is None:
            continue
        for data in MATCHES:
            date=data["info"]["dates"]
            dt=datetime.strptime(date[0],"%Y-%m-%d")
            year=dt.year
            if year != 2007 + s:
                continue
            for i in data["innings"]:
                if TEAM_CANONICAL.get(i["team"].lower()) != TEAM_CANONICAL.get(team.lower()):
                    overs=i["overs"]
                    for j in overs:
                            delivery=j["deliveries"]
                            for k in delivery:
                                if k.get("bowler", "").lower() == player.lower():
                                    if "wickets" in k:
                                        for w in k.get("wickets", []):
                                            if w.get("kind", "").lower() not in non_bowler_kinds:
                                                wickets+=1
                                                
    return wickets
def details(player,season):
    match_played=runs=balls_played=dots_played=wickets=dots=fours=sixes=0
    seasons = range(1, 19) if season == 0 else [season]
    non_bowler_kinds = {"run out", "retired hurt", "obstructing the field"}
    for s in seasons:
        team = player_in_team(player, s)
        if team is None:
            continue
        for data in MATCHES:
            if data.get("info", {}).get("event", {}).get("stage") == "Super Over":
                continue
            date=data["info"]["dates"]
            dt=datetime.strptime(date[0],"%Y-%m-%d")
            year=dt.year
            if year != 2007 + s:
                continue
            for team_players in data["info"]["players"].values():
                if player.lower() in map(str.lower, team_players):
                    match_played += 1
                    break
            for i in data["innings"]:
                if TEAM_CANONICAL.get(i["team"].lower()) == TEAM_CANONICAL.get(team.lower()):
                    overs=i["overs"]
                    for j in overs:
                        delivery=j["deliveries"]
                        for k in delivery:
                            if k.get("batter", "").lower() == player.lower():
                                extras = k.get("extras", {})
                                if "extras" not in k or "wides" not in k["extras"]:
                                    balls_played += 1
                                    if k["runs"]["total"] == 0:
                                        dots_played += 1
                                if k["runs"]["batter"]==4 and not extras:
                                    fours+=1
                                elif k["runs"]["batter"]==6 and not extras:
                                    sixes+=1
                                if "noballs" not in k.get("extras", {}):
                                    runs+=k["runs"]["batter"]
            for i in data["innings"]:
                if TEAM_CANONICAL.get(i["team"].lower()) != TEAM_CANONICAL.get(team.lower()):
                    overs=i["overs"]
                    for j in overs:
                            delivery=j["deliveries"]
                            for k in delivery:
                                if k.get("bowler", "").lower() == player.lower():
                                    if "runs" in k:
                                        if k["runs"]["total"]==0:
                                            dots+=1
                                    if "wickets" in k:
                                        for w in k.get("wickets", []):
                                            if w.get("kind", "").lower() not in non_bowler_kinds:
                                                wickets+=1
    return match_played,runs,balls_played,dots_played,fours,sixes,wickets,dots
def check_season(season):
    while True:
        if 0 <= season <= 18:
            return season
        
        if 2008 <= season <= 2025:
            return season - 2007

        print("Invalid season. Please try again.")
        season = int(input("Enter season again: "))

# print("These are all the teams that played in these 10 teams: ")
# for team in teams:
#     print(team)
choise=int(input('''
Enter 1 for total wins of each team in all seasons
Enter 2 for wins of a team for any season
Enter 3 for points table for a season
Enter 4 for finding team which a player played in
Enter 5 for finding runs made by a player
Enter 6 for finding wickets taken by a player
Enter 7 for finding all details about a player\n'''))
if(choise==1):
    total_wins()
    team_wins = {
        "RCB": RCB,
        "CSK": CSK,
        "MI": MI,
        "RR": RR,
        "SRH": SRH,
        "KKR": KKR,
        "PK": PK,
        "DC": DC,
        "Deccan Chargers": D,
        "RPS": RPS,
        "GL": GL,
        "GT": GT,
        "LSG": LSG,
        "PW": PW,
        "KTK": KTK
    }
    print(f"Total matches played:{count}")
    print("Number of wins for each team:")
    for team, wins in team_wins.items():
        print(f"{team}: {wins}")
elif choise==2:
    team=input("Enter a team name to name :")
    season=int(input("Enter the season:"))
    s=check_season(season)
    wins=team_wins_per_season(team,s)
    print(f"Number of wins by {team} in {s}:{wins}")
elif choise==3:
    season=int(input("Enter the season:"))
    s=check_season(season)
    points_table(s)
elif choise==4:
    name=input("Enter a name :")
    season=int(input("Enter the season:"))
    s=check_season(season)
    team_played=player_in_team(name,s)
    if team_played is not None:
        print(f"{name} played IPL season {season} in {team_played}")
    else:
        print(F"{name} is incorrect or did not play IPL season {season}")
elif choise==5:
    name=input("Enter a name :")
    season=int(input("Enter the season:"))
    s=check_season(season)
    runs=runs_scored(name,s)
    if s==0:
        print(f"{name} scored {runs} in all IPL season")
    else:
        print(f"{name} scored {runs} in IPL season {s}")
elif choise==6:
    name=input("Enter a name :")
    season=int(input("Enter the season:"))
    s=check_season(season)
    wickets=wickets_taken(name,s)
    if s==0:
        print(f"{name} has taken {wickets} in all IPL season")
    else:
        print(f"{name} has taken {wickets} wickets in IPL season {s}")
elif choise==7:
    name=input("Enter a name :")
    season=int(input("Enter the season:"))
    s=check_season(season)
    match_played,runs,balls_played,dots_played,fours,sixes,wickets,dots=details(name,s)
    SR=f"{runs*100/balls_played:.2f}"
    if balls_played ==0:
        SR=0
    if s==0:
        print(f'''These are the details about {name} of all IPL season
            Matches played: {match_played}
            Runs scored: {runs}
            Balls faced: {balls_played}
            Strike rate: {SR}
            Dots played: {dots_played} 
            Fours hit:{fours} 
            Sixes hit: {sixes}
            Wickets taken: {wickets}
            Dots bowled: {dots}''')
    else:
        print(f'''These are the details about {name} of all IPL season {s}
            Matches played: {match_played}
            Runs scored: {runs}
            Balls faced: {balls_played}
            Strike rate: {SR}
            Dots played: {dots_played} 
            Fours hit:{fours} 
            Sixes hit: {sixes}
            Wickets taken: {wickets}
            Dots bowled: {dots}''')
else:
    print("Wrong input enter (1-3)")