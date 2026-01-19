import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

VENUE_CANONICAL={
    "Arun Jaitley Stadium":"Arun Jaitley Stadium, Delhi",                                             
    "Arun Jaitley Stadium, Delhi":"Arun Jaitley Stadium, Delhi",
    "Feroz Shah Kotla":"Arun Jaitley Stadium, Delhi",

    "Barabati Stadium":"Barabati Stadium, Guwahati",
    "Barsapara Cricket Stadium, Guwahati":"Barabati Stadium, Guwahati",

    "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow":"Ekana Cricket Stadium, Lucknow",

    "Brabourne Stadium":"Brabourne Stadium, Mumbai",
    "Brabourne Stadium, Mumbai":"Brabourne Stadium, Mumbai",

    "Buffalo Park":"Buffalo Park",
    "De Beers Diamond Oval":"De Beers Diamond Oval",

    "Dr DY Patil Sports Academy":"Dr DY Patil Sports Academy, Mumbai",
    "Dr DY Patil Sports Academy, Mumbai":"Dr DY Patil Sports Academy, Mumbai",

    "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium":"Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium, Visakhapatnam",
    "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium, Visakhapatnam":"Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium, Visakhapatnam",

    "Dubai International Cricket Stadium":"Dubai International Cricket Stadium",

    "Eden Gardens":"Eden Gardens, Kolkata",
    "Eden Gardens, Kolkata":"Eden Gardens, Kolkata",

    "Green Park":"Green Park",

    "Himachal Pradesh Cricket Association Stadium":"Himachal Pradesh Cricket Association Stadium, Dharamsala",
    "Himachal Pradesh Cricket Association Stadium, Dharamsala":"Himachal Pradesh Cricket Association Stadium, Dharamsala",

    "Holkar Cricket Stadium":"Holkar Cricket Stadium",

    "JSCA International Stadium Complex":"JSCA International Stadium Complex",

    "Kingsmead":"Kingsmead",

    "M Chinnaswamy Stadium":"M Chinnaswamy Stadium, Bengaluru",
    "M Chinnaswamy Stadium, Bengaluru":"M Chinnaswamy Stadium, Bengaluru",
    "M.Chinnaswamy Stadium":"M Chinnaswamy Stadium, Bengaluru",

    "MA Chidambaram Stadium":"MA Chidambaram Stadium, Chepauk",
    "MA Chidambaram Stadium, Chepauk":"MA Chidambaram Stadium, Chepauk",
    "MA Chidambaram Stadium, Chepauk, Chennai":"MA Chidambaram Stadium, Chepauk",

    "Maharaja Yadavindra Singh International Cricket Stadium, Mullanpur":"Maharaja Yadavindra Singh International Cricket Stadium, New Chandigarh",
    "Maharaja Yadavindra Singh International Cricket Stadium, New Chandigarh":"Maharaja Yadavindra Singh International Cricket Stadium, New Chandigarh",

    "Maharashtra Cricket Association Stadium":"Maharashtra Cricket Association Stadium, Pune",
    "Maharashtra Cricket Association Stadium, Pune":"Maharashtra Cricket Association Stadium, Pune",

    "Narendra Modi Stadium, Ahmedabad":"Narendra Modi Stadium, Ahmedabad",

    "Nehru Stadium":"Nehru Stadium",

    "New Wanderers Stadium":"New Wanderers Stadium",

    "Newlands":"Newlands",

    "OUTsurance Oval":"OUTsurance Oval",

    "Punjab Cricket Association IS Bindra Stadium":"Punjab Cricket Association Stadium, Mohali",
    "Punjab Cricket Association IS Bindra Stadium, Mohali":"Punjab Cricket Association Stadium, Mohali",
    "Punjab Cricket Association IS Bindra Stadium, Mohali, Chandigarh":"Punjab Cricket Association Stadium, Mohali",
    "Punjab Cricket Association Stadium, Mohali":"Punjab Cricket Association Stadium, Mohali",

    "Rajiv Gandhi International Stadium":"Rajiv Gandhi International Stadium, Uppal",
    "Rajiv Gandhi International Stadium, Uppal":"Rajiv Gandhi International Stadium, Uppal",
    "Rajiv Gandhi International Stadium, Uppal, Hyderabad":"Rajiv Gandhi International Stadium, Uppal",

    "Sardar Patel Stadium, Motera":"Sardar Patel Stadium, Motera",

    "Sawai Mansingh Stadium":"Sawai Mansingh Stadium, Jaipur",
    "Sawai Mansingh Stadium, Jaipur":"Sawai Mansingh Stadium, Jaipur",

    "Shaheed Veer Narayan Singh International Stadium":"Shaheed Veer Narayan Singh International Stadium",

    "Sharjah Cricket Stadium":"Sharjah Cricket Stadium",

    "Sheikh Zayed Stadium":"Sheikh Zayed Stadium",

    "St George's Park":"St George's Park",

    "Subrata Roy Sahara Stadium":"Subrata Roy Sahara Stadium",

    "SuperSport Park":"SuperSport Park",

    "Vidarbha Cricket Association Stadium, Jamtha":"Vidarbha Cricket Association Stadium, Jamtha",

    "Wankhede Stadium":"Wankhede Stadium, Mumbai",
    "Wankhede Stadium, Mumbai":"Wankhede Stadium, Mumbai",

    "Zayed Cricket Stadium, Abu Dhabi":"Zayed Cricket Stadium, Abu Dhabi"
}

matches=pd.read_csv("data\\processed\\matches.csv")
matches["Venue"] = (
    matches["Venue"]
    .str.strip()
    .replace(VENUE_CANONICAL)
)
def matches_per_season():
    matches_df = (
        matches
        .groupby("Season")
        .size()
        .reset_index(name="No. of Matches")
    )
    print(matches_df.to_string(index=False))

    plt.figure(figsize=(10,6))
    plt.bar(matches_df["Season"],matches_df["No. of Matches"])
    plt.xlabel("Season",fontweight='bold')
    plt.ylabel("No. of Matches",fontweight='bold')
    plt.xticks(np.arange(min(matches_df["Season"]), max(matches_df["Season"]) +1, 1))
    plt.title("Matches per Season",fontweight='bold')
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\matches_per_season.png")
    plt.show()

def result_type():
    result_df = (
        matches
        .groupby("Result_Type")
        .size()
        .reset_index(name="No. of Matches")
    )
    result_df = result_df.sort_values("No. of Matches",ascending=False)
    result_df=result_df.reset_index(drop=True)
    print(result_df.to_string(index=False))

    plt.figure(figsize=(10,6))
    plt.bar(result_df["Result_Type"],result_df["No. of Matches"])
    plt.xlabel("Result type",fontweight='bold')
    plt.ylabel("No. of Matches",fontweight='bold')
    plt.title("Matches for eash result type",fontweight='bold')
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\matches_by_result_type.png")
    plt.show()

def result_counts():
    result_counts_df = (
        matches
        .groupby(["Season", "Result_Type"])
        .size()
        .unstack(fill_value=0)
    )
    print(result_counts_df.to_string(index=False))
    result_counts_df.plot(kind="bar", stacked=True)

    plt.xlabel("Season")
    plt.ylabel("Number of Matches")
    plt.title("Match Result Distribution per Season")
    plt.legend(title="Result Type")
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\season_wise_match_results.png")
    plt.show()

def no_of_venues():
    venues=(
        matches
        .groupby("Venue")
        .size()
        .reset_index(name="No. of Matches")
    )
    venues=venues.sort_values("No. of Matches",ascending=False)
    venues = venues.reset_index(drop=True)
    print(venues.to_string(index=False))

def unique_venues():
    unique_venues_per_season = (
        matches
        .groupby("Season")["Venue"]
        .nunique()
        .reset_index(name="Unique Venues")
    )
    print(unique_venues_per_season.to_string(index=False))

    plt.figure(figsize=(10,6))
    plt.bar(
        unique_venues_per_season["Season"],
        unique_venues_per_season["Unique Venues"]
    )
    plt.xlabel("Season", fontweight="bold")
    plt.ylabel("Unique Venues", fontweight="bold")
    plt.title("Unique Venues per Season", fontweight="bold")
    plt.xticks(np.arange(min(unique_venues_per_season["Season"]),max(unique_venues_per_season["Season"])+1,1))
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\unique_venues_per_season.png")
    plt.show()
def matches_played_per_team():
    df = (
        matches[["Team_1", "Team_2"]]
        .stack()
        .value_counts()
        .reset_index()
    )
    df.columns = ["Team", "Matches_Played"]
    print(df.to_string(index=False))

    plt.figure(figsize=(10,6))
    plt.barh(df["Team"], df["Matches_Played"])
    plt.xlabel("Total matches played", fontweight="bold")
    plt.ylabel("Teams", fontweight="bold")
    plt.title("Matches played by each team", fontweight="bold")
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\matches_played_by_teams.png")
    plt.show()

def wins_per_team():
    df = (
        matches["Winner"]
        .dropna()
        .value_counts()
        .reset_index()
    )
    df.columns = ["Team", "Matches_Won"]
    print(df.to_string(index=False))

    plt.figure(figsize=(10,6))
    plt.barh(df["Team"], df["Matches_Won"])
    plt.xlabel("Total matches won", fontweight="bold")
    plt.ylabel("Teams", fontweight="bold")
    plt.title("Matches won by each team", fontweight="bold")
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\matches_won_by_teams.png")
    plt.show()

def matches_played_vs_won_per_team():
    played = (
        matches[["Team_1", "Team_2"]]
        .stack()
        .value_counts()
    )
    won = (
        matches["Winner"]
        .dropna()
        .value_counts()
    )

    df = pd.DataFrame({
        "Matches_Played": played,
        "Matches_Won": won
    }).fillna(0).astype(int)

    df = df.sort_values("Matches_Played", ascending=False).reset_index()
    df.rename(columns={"index": "Team"}, inplace=True)

    print(df.to_string(index=False))

    y = np.arange(len(df))
    height = 0.4

    plt.figure(figsize=(12, 7))
    plt.barh(y - height/2, df["Matches_Played"], height, label="Matches Played")
    plt.barh(y + height/2, df["Matches_Won"], height, label="Matches Won")

    plt.yticks(y, df["Team"])
    plt.xlabel("Number of Matches", fontweight="bold")
    plt.ylabel("Teams", fontweight="bold")
    plt.title("Matches Played vs Matches Won by Each Team", fontweight="bold")
    plt.legend()

    plt.tight_layout()
    plt.savefig(
        "v2_dataframe_based_analysis\\Graphs\\matches_played_vs_won_by_teams.png"
    )
    plt.show()
 
def win_percentage_per_team():
    played = (
        matches[["Team_1", "Team_2"]]
        .stack()
        .value_counts()
    )
    won = (
        matches["Winner"]
        .dropna()
        .value_counts()
    )
    df = pd.DataFrame({
        "Played": played,
        "Won": won
    }).fillna(0)

    df["Win_Percentage"] = (df["Won"] / df["Played"] * 100).round(2)
    df=df[["Win_Percentage"]].reset_index().rename(columns={"index": "Team"}).sort_values("Win_Percentage",ascending=False)
    print(df.to_string(index=False))

    plt.figure(figsize=(10,6))
    plt.barh(df["Team"], df["Win_Percentage"])
    plt.xlabel("Win Percentage", fontweight="bold")
    plt.ylabel("Teams", fontweight="bold")
    plt.title("Win percentage of each team", fontweight="bold")
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\win_percentage_by_teams.png")
    plt.show()

def team_wins_across_seasons():
    df = (
        matches[["Season", "Winner"]]
        .dropna(subset=["Winner"])     # remove NR / abandoned
        .groupby(["Season", "Winner"])
        .size()
        .reset_index(name="Matches_Won")
        .rename(columns={"Winner": "Team"})
        .sort_values(["Season", "Matches_Won"], ascending=[True, False])
    )
    print(df)

    plt.figure(figsize=(12,9))
    for team in df["Team"].unique():
        team_df = df[df["Team"] == team]
        plt.plot(
            team_df["Season"],
            team_df["Matches_Won"],
            marker="o",
            label=team
        )
    plt.xlabel("Season", fontweight="bold")
    plt.ylabel("Matches Won", fontweight="bold")
    plt.title("Team Wins Across Seasons", fontweight="bold")
    plt.xticks(np.arange(min(df["Season"]),max(df["Season"])+1,1))
    plt.yticks(np.arange(min(df["Matches_Won"]),max(df["Matches_Won"])+1,1))
    plt.legend(bbox_to_anchor=(1, 0.75))
    plt.grid()
    plt.tight_layout()
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\team_wins_across_seasons.png")
    plt.show()

def seasonwise_win_type_distribution():
    df = (
        matches.pivot_table(
            index="Season",
            columns="Win_Type",
            aggfunc="size",
            fill_value=0
        )
        .reset_index()
    )
    print(df.to_string(index=False))

    x = np.arange(len(df.index))
    width = 0.4
    plt.figure(figsize=(10, 6))
    plt.bar(x - width/2,df["runs"],width,label="Wins by Runs")
    plt.bar(x + width/2,df["wickets"],width,label="Wins by Wickets")
    plt.xlabel("Season",fontweight='bold')
    plt.ylabel("Matches won ",fontweight='bold')
    plt.title("Distribution of Match Wins by Result Type Across Seasons",fontweight='bold')
    plt.xticks(x, df["Season"])
    plt.legend(title='Type',bbox_to_anchor=(1,1),loc='center')
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\seasonwise_win_type_comparison.png")
    plt.show()

def win_margin():
    dfruns=matches[matches["Win_Type"]=="runs"]
    dfwic=matches[matches["Win_Type"]=="wickets"]
    print(f"The average win margin by runs is: {(dfruns["Win_Margin"].mean()).round(2)}")
    print(f"The average win margin by wickets is: {(dfwic["Win_Margin"].mean()).round(2)}")

    print(f"The minimum and maximum win margin by runs is: {dfruns["Win_Margin"].min()},{dfruns["Win_Margin"].max()}")
    print(f"The minimum and maximum win margin by wickets is: {dfwic["Win_Margin"].min()},{dfwic["Win_Margin"].max()}")

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.hist(dfruns["Win_Margin"])
    plt.xlabel("Win Margin (Runs)", fontweight="bold")
    plt.ylabel("Frequency", fontweight="bold")
    plt.title("Win Margin by Runs", fontweight="bold")

    plt.subplot(1, 2, 2)
    plt.hist(dfwic["Win_Margin"])
    plt.xlabel("Win Margin (Wickets)", fontweight="bold")
    plt.ylabel("Frequency", fontweight="bold")
    plt.title("Win Margin by Wickets", fontweight="bold")

    plt.tight_layout()
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\win_margin_distribution.png")
    plt.show()

def matches_per_venue():
    df = (
        matches
        .groupby("Venue")
        .size()                        
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .reset_index(drop=True)
    )
    dfTop10=df.head(10)
    print(dfTop10)

    plt.figure(figsize=(12,6))
    plt.barh(dfTop10["Venue"],dfTop10["count"])
    plt.xlabel("Matches played",fontweight='bold')
    plt.ylabel("Venue",fontweight='bold')
    plt.yticks(fontsize=9)
    plt.title("Matches played in the top 10 venues",fontweight='bold')
    plt.tight_layout()
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\matches_per_venue.png")
    plt.show()

def wins_per_venue():
    matches_df = (
        matches
        .groupby("Venue")
        .size()
        .reset_index(name="matches_played")
    )
    wins_df = (
        matches
        .groupby("Venue")["Winner"]
        .count()   
        .reset_index(name="wins")
    )
    df = (
        matches_df
        .merge(wins_df, on="Venue")
        .sort_values("matches_played", ascending=False)
        .head(10)
        .reset_index(drop=True)
    )
    print(df)

    x = np.arange(len(df))
    width = 0.4
    plt.figure(figsize=(12,6))
    plt.bar(x - width/2, df["matches_played"], width, label="Matches Played")
    plt.bar(x + width/2, df["wins"], width, label="Wins")
    plt.xticks(x, df["Venue"], rotation=45, ha="right")
    plt.xlabel("Venue", fontweight="bold")
    plt.ylabel("Count", fontweight="bold")
    plt.title("Top 10 Venues: Matches Played vs Wins")
    plt.legend()

    plt.tight_layout()
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\total_matches_vs_completedmatches.png")
    plt.show()


def stacked_bar_venue_vs_team():
    df = (
        matches[matches["Winner"].notna()]     
        .groupby(["Venue", "Winner"])
        .size()
        .reset_index(name="wins")
    )

    top_venues = (
        df.groupby("Venue")["wins"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .index
    )

    df = df[df["Venue"].isin(top_venues)]
    pivot_df = df.pivot(
        index="Venue",
        columns="Winner",
        values="wins"
    ).fillna(0)
    print(pivot_df)
    pivot_df.plot(
        kind="bar",
        stacked=True,
        figsize=(14, 7)
    )

    plt.xlabel("Venue", fontweight="bold")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Number of Wins", fontweight="bold")
    plt.title("Venue vs Winning Team (Stacked Bar Chart)")
    plt.legend(title="Team", bbox_to_anchor=(1,1), loc="upper left")
    plt.tight_layout()
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\stacked_bar_venue_vs_team.png")
    plt.show()

def win_type_per_venue():
    df = (
        matches
        .dropna(subset=["Win_Type"])
        .groupby(["Venue", "Win_Type"])
        .size()
        .reset_index(name="count")
    )
    df_pivot=df.pivot(index="Venue",columns="Win_Type",values="count").fillna(0)
    df_pivot = (
        df_pivot
        .assign(total=df_pivot.sum(axis=1))
        .sort_values("total", ascending=False)
        .drop(columns="total")
        .head(10)
    )
    print(df_pivot)
    x=np.arange(len(df_pivot))
    width=0.4
    plt.figure(figsize=(12,9))

    plt.bar(x - width/2, df_pivot["runs"], width, label="By runs")
    plt.bar(x + width/2, df_pivot["wickets"], width, label="By wickets")
    plt.xticks(x, df_pivot.index, rotation=45, ha="right")
    plt.xlabel("Venue", fontweight="bold")
    plt.ylabel("Count", fontweight="bold")
    plt.title("Win Type Distribution Across Venues",fontweight="bold")
    plt.legend()

    plt.tight_layout()
    plt.savefig("v2_dataframe_based_analysis\\Graphs\\win_type_per_venue.png")
    plt.show()

# matches_per_season()
# result_type()
# result_counts()
# no_of_venues()
# unique_venues()
# matches_played_per_team()
# wins_per_team()
matches_played_vs_won_per_team()
# win_percentage_per_team()
# team_wins_across_seasons()
# seasonwise_win_type_distribution()
# win_margin()
# matches_per_venue()
# wins_per_venue()
# stacked_bar_venue_vs_team()
# win_type_per_venue()

