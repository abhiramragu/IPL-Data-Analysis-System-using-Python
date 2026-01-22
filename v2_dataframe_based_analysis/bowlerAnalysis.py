import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

players=pd.read_csv("data\\processed\\players_stats.csv")
# print(players.head())
#------------------------------------Bowler analysis------------------------------------------
def wickets_per_player():
    matches = (
        players
        .groupby("player", as_index=False)["match_id"]
        .nunique()
        .rename(columns={"match_id": "matches"})
    )
    total_wic=(
         players[players["wickets"] > 0]
        .groupby("player", as_index=False)["wickets"]
        .sum()
        .sort_values("wickets", ascending=False)
        .reset_index(drop=True)
    )
    total_wickets=(
        total_wic
        .merge(matches,on="player")
    ).head(10)
    print(total_wickets)

    plt.figure(figsize=(8,6))
    x=np.arange(len(total_wickets))
    width=0.4
    plt.bar(x-width/2,total_wickets["wickets"],width,label="wickets taken")
    plt.bar(x+width/2,total_wickets["matches"],width,label="matches played")
    plt.legend()
    plt.xlabel("Player names",fontweight='bold')
    plt.ylabel("Count",fontweight='bold')
    plt.title("Top 10 wicket takers in IPL",fontweight='bold')
    plt.xticks(x,total_wickets["player"],rotation=65)
    plt.tight_layout()
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\bowlerAnalysis\\Top10_wicket_takers.png")
    plt.show()

def overs_per_player():
    matches = (
        players
        .groupby("player", as_index=False)["match_id"]
        .nunique()
        .rename(columns={"match_id": "matches"})
    )
    total_ov=(
         players[players["balls_bowled"] > 0]
        .groupby("player", as_index=False)["balls_bowled"]
        .sum()
        .sort_values("balls_bowled", ascending=False)
        .reset_index(drop=True)
    )
    total_overs=(
        total_ov
        .merge(matches,on="player")
    ).head(10)
    total_overs["Total_overs"]=(total_overs["balls_bowled"] // 6) +(total_overs["balls_bowled"] % 6) / 10
    total_overs=total_overs.drop("balls_bowled",axis=1)
    print(total_overs)

    plt.figure(figsize=(8,6))
    plt.bar(total_overs["player"],total_overs["Total_overs"])
    plt.xlabel("Player names",fontweight='bold')
    plt.ylabel("Overs bowled",fontweight='bold')
    plt.title("Most overs bowled by players",fontweight='bold')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\bowlerAnalysis\\Most_overs_bowled.png")
    plt.show()

def economy_rate():
    total_overs = (
        players[players["balls_bowled"] > 0]
        .groupby("player", as_index=False)["balls_bowled"]
        .sum()
    )
    total_overs["Total_overs"] = total_overs["balls_bowled"] / 6
    total_overs.drop("balls_bowled", axis=1, inplace=True)

    runs_conceded = (
        players[players["runs_conceded"] > 0]
        .groupby("player", as_index=False)["runs_conceded"]
        .sum()
    )

    bowler_stats = total_overs.merge(runs_conceded, on="player")

    bowler_stats["Economy"] = (
        bowler_stats["runs_conceded"] / bowler_stats["Total_overs"]
    )

    bowler_df = bowler_stats.sort_values("runs_conceded", ascending=False).head(10).reset_index(drop=True)

    print(bowler_df)

    plt.figure(figsize=(8,6))
    plt.bar(bowler_df["player"], bowler_df["runs_conceded"])
    plt.xlabel("Player names", fontweight="bold")
    plt.ylabel("Runs conceded", fontweight="bold")
    plt.title("Most runs conceded by players (minimum 200 overs)", fontweight="bold")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\bowlerAnalysis\\Most_runs_conceded.png")
    plt.show()

    best_economy = bowler_stats[bowler_stats["Total_overs"]>200]
    best_economy=best_economy.sort_values("Economy", ascending=True).head(10).reset_index(drop=True)

    print(best_economy)

    plt.figure(figsize=(8,6))
    plt.bar(best_economy["player"], best_economy["Economy"])
    plt.xlabel("Player names", fontweight="bold")
    plt.ylabel("Economy", fontweight="bold")
    plt.title("Best economy by players (minimum 200 overs)", fontweight="bold")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\bowlerAnalysis\\Best_economy.png")
    plt.show()

def wickets_vs_economy():
    stats = (
        players
        .groupby("player", as_index=False)
        .agg(
            balls_bowled=("balls_bowled", "sum"),
            wickets=("wickets", "sum"),
            runs_conceded=("runs_conceded", "sum")
        )
    )

    stats["Total_overs"] = stats["balls_bowled"] / 6
    stats["Economy"] = stats["runs_conceded"] / stats["Total_overs"]

    stats = stats[stats["Total_overs"] >= 200]

    stats = (
        stats
        .sort_values("Economy", ascending=True)
        .head(10)
        .reset_index(drop=True)
    )

    print(stats)

    plt.figure(figsize=(9,6))
    for _, row in stats.iterrows():
        plt.scatter(row["Economy"],row["wickets"],label=row["player"],s=150)

    plt.xlabel("Economy Rate", fontweight="bold")
    plt.ylabel("Total Wickets", fontweight="bold")
    plt.title("Wickets vs Economy (Top 10, Min 200 Overs)", fontweight="bold")
    plt.grid()
    plt.legend(title="Players", bbox_to_anchor=(1,1), loc="upper left")
    plt.tight_layout()
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\bowlerAnalysis\\Wickets_vs_economy.png")
    plt.show()

def strike_rate():
    stats = (
        players
        .groupby("player", as_index=False)
        .agg(
            balls_bowled=("balls_bowled", "sum"),
            wickets=("wickets", "sum"),
        )
    )
    stats["Total_overs"] = (stats["balls_bowled"] / 6).round(2)
    stats = stats[(stats["wickets"] > 0) & (stats["Total_overs"] >= 200)]
    stats["strike rate"]=(stats["balls_bowled"]/stats["wickets"]).round(2)
    stats=stats.sort_values("strike rate").head(10).reset_index(drop=True)
    print(stats)

    plt.figure(figsize=(8,6))
    plt.bar(stats["player"], stats["strike rate"])
    plt.xlabel("Player names", fontweight="bold")
    plt.ylabel("Strike rate", fontweight="bold")
    plt.title("Best bowling strike rate by players (minimum 200 overs)", fontweight="bold")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\bowlerAnalysis\\Best_bowling_sr.png")
    plt.show()

def average():
    stats = (
        players
        .groupby("player", as_index=False)
        .agg(
            runs_conceded=("runs_conceded", "sum"),
            wickets=("wickets", "sum"),
            balls_bowled=("balls_bowled", "sum")
        )
    )
    stats["Total_overs"] = (stats["balls_bowled"] / 6)
    stats["average"]=(stats["runs_conceded"]/stats["wickets"]).round(2)
    stats=stats[stats["Total_overs"] >= 200]
    stats=stats.sort_values("average").head(10).reset_index(drop=True)
    print(stats)

    plt.figure(figsize=(8,6))
    plt.bar(stats["player"], stats["average"])
    plt.xlabel("Player names", fontweight="bold")
    plt.ylabel("Average", fontweight="bold")
    plt.title("Best bowling average by players (minimum 200 overs)", fontweight="bold")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\bowlerAnalysis\\Best_bowling_average.png")
    plt.show()

def Season_wise_wickets():
    season_df=(
        players
        .pivot_table(
            index="player",
            columns="season",
            values="wickets",
            aggfunc="sum",
            fill_value=0
        )
    )
    season_df["Total"]=season_df.sum(axis=1)
    season_df=season_df.sort_values("Total",ascending=False).head(10)
    print(season_df)

    season_cols = season_df.columns.drop("Total")

    plt.figure(figsize=(10,8))
    for player in season_df.index:
        y = season_df.loc[player, season_cols]
        plt.plot(season_cols, y, label=player)
    plt.legend(title="Players",bbox_to_anchor=(1,1))
    plt.xlabel("Season", fontweight="bold")
    plt.ylabel("Runs", fontweight="bold")
    plt.title("Season-wise wickets Scored by Players", fontweight="bold")
    plt.xticks(np.arange(1, len(season_cols) + 1))
    plt.grid()
    plt.tight_layout()
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\bowlerAnalysis\\Top10_players_season_wise_wickets.png")
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.heatmap(
        season_df[season_cols],
        cmap="Blues",
        linewidths=0.5,
        cbar_kws={"label": "Wickets taken"}
    )

    plt.xlabel("Season", fontweight="bold")
    plt.ylabel("Player", fontweight="bold")
    plt.title("Season-wise wickets Distribution (Top 10 Players)", fontweight="bold")
    plt.tight_layout()
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\bowlerAnalysis\\Season_wise_runs_heatmap.png")
    plt.show()

wickets_per_player()
overs_per_player()
economy_rate()
wickets_vs_economy()
strike_rate()
average()
Season_wise_wickets()