"""Tally picks vs. results into weekly and season standings."""
import pandas as pd


def weekly_scoreboard(picks_df: pd.DataFrame, results_df: pd.DataFrame, week: int) -> pd.DataFrame:
    """Returns one row per participant: Name, Correct, Picked (games with a pick this week)."""
    wk_picks = picks_df[picks_df["Week"].astype(str) == str(week)].copy()
    wk_results = results_df[results_df["Week"].astype(str) == str(week)].copy()

    if wk_picks.empty:
        return pd.DataFrame(columns=["Name", "Correct", "Picked"])

    merged = wk_picks.merge(
        wk_results[["GameID", "Winner"]], on="GameID", how="left"
    )
    merged["IsCorrect"] = (merged["Pick"] == merged["Winner"]) & merged["Winner"].notna()

    out = merged.groupby("Name").agg(
        Correct=("IsCorrect", "sum"),
        Picked=("GameID", "nunique"),
    ).reset_index()
    out["Correct"] = out["Correct"].astype(int)
    return out.sort_values("Correct", ascending=False).reset_index(drop=True)


def season_standings(picks_df: pd.DataFrame, results_df: pd.DataFrame, all_weeks) -> pd.DataFrame:
    """One row per participant with a Total column plus a column per week."""
    if picks_df.empty:
        return pd.DataFrame(columns=["Name", "Total"])

    names = sorted(picks_df["Name"].dropna().unique())
    table = pd.DataFrame({"Name": names})

    for wk in all_weeks:
        wk_score = weekly_scoreboard(picks_df, results_df, wk)
        col = f"Wk{wk}"
        table = table.merge(
            wk_score[["Name", "Correct"]].rename(columns={"Correct": col}),
            on="Name", how="left",
        )
        table[col] = table[col].fillna(0).astype(int)

    week_cols = [f"Wk{wk}" for wk in all_weeks]
    table["Total"] = table[week_cols].sum(axis=1)
    table = table.sort_values("Total", ascending=False).reset_index(drop=True)
    table.insert(0, "Rank", table.index + 1)
    return table[["Rank", "Name", "Total"] + week_cols]


def tiebreaker_diff(tb_df: pd.DataFrame, tb_actual_df: pd.DataFrame, week: int) -> pd.DataFrame:
    wk_tb = tb_df[tb_df["Week"].astype(str) == str(week)].copy()
    if wk_tb.empty:
        return pd.DataFrame(columns=["Name", "Guess", "Actual", "Diff"])
    actual_row = tb_actual_df[tb_actual_df["Week"].astype(str) == str(week)]
    actual = None
    if not actual_row.empty:
        actual = int(actual_row.iloc[0]["ActualTotal"])
    wk_tb["Actual"] = actual
    wk_tb["Diff"] = wk_tb["Guess"].apply(
        lambda g: abs(int(g) - actual) if actual is not None else None
    )
    return wk_tb.rename(columns={"Guess": "Guess"})[["Name", "Guess", "Actual", "Diff"]].sort_values(
        "Diff", na_position="last"
    ).reset_index(drop=True)
