import pandas as pd 
import matplotlib.pyplot as plt


players=pd.read_csv("data\\processed\\players_stats.csv")
# print(players.head())

def allrounder():
    allrounder_df=(
        players
        .groupby("player", as_index=False)
        .agg(
            runs_scored=("runs","sum"),
            wickets_taken=("wickets","sum")
           
        )
    )
    allrounder_df=allrounder_df[(allrounder_df["runs_scored"]>1000)&(allrounder_df["wickets_taken"]>50)]
    allrounder_df = allrounder_df.sort_values(["runs_scored", "wickets_taken"], ascending=False).reset_index(drop=True)

    print(allrounder_df)

    plt.figure(figsize=(9,6))
    for _, row in allrounder_df.iterrows():
        plt.scatter(row["runs_scored"],row["wickets_taken"],label=row["player"],s=150)
    plt.xlabel("Total runs", fontweight="bold")
    plt.ylabel("Total Wickets", fontweight="bold")
    plt.title("All rounder analysis  (Min 1000 runs and 50 wickets)", fontweight="bold")
    plt.grid()
    plt.legend(title="Players", bbox_to_anchor=(1,1), loc="upper left")
    plt.tight_layout()
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\allrounderAnalysis\\Runs_vs_wickets.png")
    plt.show()

allrounder()