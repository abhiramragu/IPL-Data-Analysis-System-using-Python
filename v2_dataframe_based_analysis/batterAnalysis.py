import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

players=pd.read_csv("data\\processed\\players_stats.csv")
# print(players.head())
#-------------------------Batsman Analysis-------------------------
def Runs_per_player(): 
    total_runs = (
        players[players["runs"] > 0]
        .groupby("player", as_index=False)["runs"]
        .sum()
        .sort_values("runs", ascending=False)
        .reset_index(drop=True)
    )
    total_runs=total_runs.head(10)
    print(total_runs)
    plt.figure(figsize=(8,6))
    plt.bar(total_runs["player"],total_runs["runs"])
    plt.xlabel("Player names",fontweight='bold')
    plt.xticks(total_runs["player"], rotation=60, ha="right")
    plt.ylabel("Runs scored",fontweight='bold')
    plt.title("Top 10 top run scorers",fontweight='bold')
    plt.tight_layout()
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\batterAnalysis\\top10_run_scorers.png")
    plt.show()

def runs_per_match():
    matches = (
        players
        .groupby("player", as_index=False)["match_id"]
        .nunique()
        .rename(columns={"match_id": "matches"})
    )
    total_runs = (
        players[players["runs"] > 0]
        .groupby("player", as_index=False)["runs"]
        .sum()
        .reset_index(drop=True)
    )
    runs_per_match_df=(
        total_runs
        .merge(matches, on="player", how="inner")
    ) 
    runs_per_match_df["Runs_per_Match"]=(runs_per_match_df["runs"]/runs_per_match_df["matches"]).round(2)
    runs_per_match_df=runs_per_match_df.sort_values("Runs_per_Match",ascending=False).reset_index(drop=True).head(10)
    print(runs_per_match_df)
    plt.figure(figsize=(8,6))
    plt.bar(runs_per_match_df["player"],runs_per_match_df["Runs_per_Match"])
    plt.xlabel("Player names",fontweight='bold')
    plt.xticks(runs_per_match_df["player"], rotation=60, ha="right")
    plt.ylabel("Runs per Match",fontweight='bold')
    plt.title("Top 10 Runs per Match",fontweight='bold')
    plt.tight_layout()
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\batterAnalysis\\top10_run_per_match.png")
    plt.show()
def Balls_per_player():
    total_balls=(
        players
        .groupby("player", as_index=False)["balls_faced"]
        .sum()
        .sort_values("balls_faced", ascending=False)
        .reset_index(drop=True)
    )
    total_balls=total_balls.head(10)
    print(total_balls)
    plt.figure(figsize=(8,6))
    plt.bar(total_balls["player"],total_balls["balls_faced"])
    plt.xlabel("Player names",fontweight='bold')
    plt.xticks(total_balls["player"], rotation=60, ha="right")
    plt.ylabel("balls played",fontweight='bold')
    plt.title("Top 10 Players by Balls Faced",fontweight='bold')
    plt.tight_layout()
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\batterAnalysis\\top10_balls_faced.png")
    plt.show()


def Avg_per_player():
    summary = (
        players
        .groupby("player", as_index=False)
        .agg(
            Total_Runs=("runs", "sum"),
            Total_Balls=("balls_faced", "sum"),
            Matches_Played=("match_id", "nunique")
        )
    )
    summary["Strike_Rate"] = (
        summary["Total_Runs"] / summary["Total_Balls"] * 100
    ).round(2)
    Avg_sr = (
        summary
        .sort_values("Strike_Rate", ascending=False)
    )
    Avg_sr = Avg_sr[Avg_sr["Matches_Played"] >= 50].reset_index(drop=True).head(10)
    print(Avg_sr)

    plt.figure(figsize=(8,6))
    plt.bar(Avg_sr["player"],Avg_sr["Strike_Rate"])
    plt.xlabel("Player names",fontweight='bold')
    plt.xticks(Avg_sr["player"], rotation=60, ha="right")
    plt.ylabel("Avg Strike Rate",fontweight='bold')
    plt.title("Top 10 best strikers ",fontweight='bold')
    plt.tight_layout()
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\batterAnalysis\\Top10_best_strikers.png")
    plt.show()

    plt.figure(figsize=(8,6))
    for _, row in Avg_sr.iterrows():
        plt.scatter(row["Total_Runs"],row["Strike_Rate"],label=row["player"],s=180)

    plt.xlabel("Total Runs", fontweight="bold")
    plt.ylabel("Strike Rate", fontweight="bold")
    plt.title("Runs vs Strike Rate ", fontweight="bold")
    plt.legend(title="Players",bbox_to_anchor=(1,1), loc="upper left")
    plt.tight_layout()
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\batterAnalysis\\Top10_runs_vs_strike_rate.png")
    plt.show()
def Boundary_contribution():
    boundary=(
        players
        .groupby("player", as_index=False)
        .agg(
            Fours=("fours", "sum"),
            Sixes=("sixes", "sum"),
        )
    )
    boundary["Total"]=boundary["Fours"]+boundary["Sixes"]
    boundary=boundary[boundary["Total"]>0].sort_values("Total",ascending=False).reset_index(drop=True).head(10)
    print(boundary)
    plt.figure(figsize=(8,6))
    plt.bar(boundary["player"],boundary["Total"])
    plt.xticks(rotation=65)
    plt.xlabel("Player names",fontweight='bold')
    plt.ylabel("Total boundaries",fontweight='bold')
    plt.title("Top 10 Players by Total Boundaries",fontweight='bold')
    plt.tight_layout()
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\batterAnalysis\\Top10_players_by_total_boundaries.png")
    plt.show()

    plt.figure(figsize=(8,6))
    x=np.arange(len(boundary))
    width=0.4
    plt.bar(x-width/2,boundary["Fours"],width,label="Fours hit")
    plt.bar(x+width/2,boundary["Sixes"],width,label="Sixes hit")
    plt.xticks(x,boundary["player"],rotation=65)
    plt.xlabel("Player names",fontweight='bold')
    plt.ylabel("Boundaries hit",fontweight='bold')
    plt.title("Boundary Breakdown - Top 10 Players",fontweight='bold')
    plt.legend()
    plt.tight_layout()
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\batterAnalysis\\Top10_players_boundary_breakdown.png")
    plt.show()

def Season_wise_runs():
    season_df=(
        players
        .pivot_table(
            index="player",
            columns="season",
            values="runs",
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
    plt.title("Season-wise Runs Scored by Players", fontweight="bold")
    plt.xticks(np.arange(1, len(season_cols) + 1))
    plt.grid()
    plt.tight_layout()
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\batterAnalysis\\Top10_players_season_wise_runs.png")
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.heatmap(
        season_df[season_cols],
        cmap="Blues",
        linewidths=0.5,
        cbar_kws={"label": "Runs Scored"}
    )

    plt.xlabel("Season", fontweight="bold")
    plt.ylabel("Player", fontweight="bold")
    plt.title("Season-wise Runs Distribution (Top 10 Players)", fontweight="bold")
    plt.tight_layout()
    plt.savefig(
        "v2_dataframe_based_analysis\\Graphs\\batterAnalysis\\Season_wise_runs_heatmap.png"
    )
    plt.show()

def Season_wise_boundaries():
    boundary_df = (
        players
        .assign(Boundaries=players["fours"] + players["sixes"])
        .pivot_table(
            index="player",
            columns="season",
            values="Boundaries",
            aggfunc="sum",
            fill_value=0
        )
    )
    boundary_df["Total"] = boundary_df.sum(axis=1)
    boundary_df = boundary_df.sort_values("Total", ascending=False).head(10)
    print(boundary_df)

    season_cols = boundary_df.columns.drop("Total")
    plt.figure(figsize=(10, 8))
    for player in boundary_df.index:
        y = boundary_df.loc[player, season_cols]
        plt.plot(season_cols, y, label=player)
    plt.legend(title="Players", bbox_to_anchor=(1, 1))
    plt.xlabel("Season", fontweight="bold")
    plt.ylabel("Boundaries", fontweight="bold")
    plt.title("Season-wise Boundaries Hit by Players", fontweight="bold")
    plt.xticks(np.arange(1, len(season_cols) + 1))
    plt.grid()
    plt.tight_layout()
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\batterAnalysis\\Top10_players_season_wise_boundaries.png")
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.heatmap(
        boundary_df[season_cols],
        cmap="Blues",
        linewidths=0.5,
        cbar_kws={"label": "Boundaries Hit"}
    )
    plt.xlabel("Season", fontweight="bold")
    plt.ylabel("Player", fontweight="bold")
    plt.title("Season-wise Boundary Distribution (Top 10 Players)", fontweight="bold")
    plt.tight_layout()
    plt.savefig(
        "v2_dataframe_based_analysis\\Graphs\\batterAnalysis\\Season_wise_boundaries_heatmap.png"
    )
    plt.show()


Runs_per_player()
runs_per_match()
Balls_per_player()
Avg_per_player()
Boundary_contribution()
Season_wise_runs()
Season_wise_boundaries()


