"""
Google Sheets backend for the Pick'em app.

Mirrors the pattern from marksworldcuppredictor: a service account (creds
stored in Streamlit secrets) reads/writes a Google Sheet that acts as the
database. Four tabs are used, auto-created on first run if missing:

  Picks               Timestamp | Name | Week | GameID | Away | Home | Pick
  Tiebreakers         Timestamp | Name | Week | Guess
  Results             Week | GameID | Away | Home | Winner
  TiebreakerActuals   Week | ActualTotal
"""
import datetime as dt
import pandas as pd
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

TABS = {
    "Picks": ["Timestamp", "Name", "Week", "GameID", "Away", "Home", "Pick"],
    "Tiebreakers": ["Timestamp", "Name", "Week", "Guess"],
    "Results": ["Week", "GameID", "Away", "Home", "Winner"],
    "TiebreakerActuals": ["Week", "ActualTotal"],
}


@st.cache_resource(show_spinner=False)
def _client():
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    return gspread.authorize(creds)


@st.cache_resource(show_spinner=False)
def _spreadsheet():
    gc = _client()
    sheet_id = st.secrets["sheet_id"]
    return gc.open_by_key(sheet_id)


def _get_or_create_tab(name):
    ss = _spreadsheet()
    try:
        ws = ss.worksheet(name)
    except gspread.WorksheetNotFound:
        ws = ss.add_worksheet(title=name, rows=1000, cols=len(TABS[name]) + 1)
        ws.append_row(TABS[name])
    return ws


@st.cache_data(ttl=20, show_spinner=False)
def read_tab(name) -> pd.DataFrame:
    # Cached for 20s: Streamlit reruns this whole script on every click, and
    # without caching that means a fresh Google Sheets API call per tab per
    # click -- which blows through the free 60-reads/minute quota almost
    # immediately. Writes below call st.cache_data.clear() so a submission
    # is reflected right away instead of waiting out the cache window.
    ws = _get_or_create_tab(name)
    records = ws.get_all_records()
    df = pd.DataFrame(records)
    if df.empty:
        df = pd.DataFrame(columns=TABS[name])
    return df


def _now():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def submit_picks(name: str, week: int, picks: dict, editable_game_ids: set, games_by_id: dict):
    """
    Replaces this participant's picks for `week`, but ONLY for game ids in
    editable_game_ids (i.e. games that haven't kicked off yet). Any existing
    picks for locked games are left untouched.

    picks: {game_id: chosen_team_name}
    """
    ws = _get_or_create_tab("Picks")
    df = read_tab("Picks")

    if not df.empty:
        keep_mask = ~(
            (df["Name"] == name)
            & (df["Week"].astype(str) == str(week))
            & (df["GameID"].isin(editable_game_ids))
        )
        df = df[keep_mask]

    new_rows = []
    ts = _now()
    for gid, pick in picks.items():
        if gid not in editable_game_ids or not pick:
            continue
        g = games_by_id[gid]
        new_rows.append({
            "Timestamp": ts, "Name": name, "Week": week, "GameID": gid,
            "Away": g["away"], "Home": g["home"], "Pick": pick,
        })

    if new_rows:
        df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)

    ws.clear()
    ws.append_row(TABS["Picks"])
    if not df.empty:
        ws.append_rows(df[TABS["Picks"]].values.tolist())


def submit_tiebreaker(name: str, week: int, guess: int, editable: bool):
    if not editable:
        return
    ws = _get_or_create_tab("Tiebreakers")
    df = read_tab("Tiebreakers")
    if not df.empty:
        df = df[~((df["Name"] == name) & (df["Week"].astype(str) == str(week)))]
    new_row = pd.DataFrame([{
        "Timestamp": _now(), "Name": name, "Week": week, "Guess": guess,
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    ws.clear()
    ws.append_row(TABS["Tiebreakers"])
    if not df.empty:
        ws.append_rows(df[TABS["Tiebreakers"]].values.tolist())


def save_results(week: int, results: dict, games_by_id: dict, tiebreaker_actual):
    """results: {game_id: winner_team_name}"""
    ws = _get_or_create_tab("Results")
    df = read_tab("Results")
    if not df.empty:
        df = df[df["Week"].astype(str) != str(week)]
    new_rows = []
    for gid, winner in results.items():
        if not winner:
            continue
        g = games_by_id[gid]
        new_rows.append({
            "Week": week, "GameID": gid, "Away": g["away"], "Home": g["home"], "Winner": winner,
        })
    if new_rows:
        df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
    ws.clear()
    ws.append_row(TABS["Results"])
    if not df.empty:
        ws.append_rows(df[TABS["Results"]].values.tolist())

    tb_ws = _get_or_create_tab("TiebreakerActuals")
    tb_df = read_tab("TiebreakerActuals")
    if not tb_df.empty:
        tb_df = tb_df[tb_df["Week"].astype(str) != str(week)]
    if tiebreaker_actual is not None:
        tb_df = pd.concat([tb_df, pd.DataFrame([{"Week": week, "ActualTotal": tiebreaker_actual}])], ignore_index=True)
    tb_ws.clear()
    tb_ws.append_row(TABS["TiebreakerActuals"])
    if not tb_df.empty:
        tb_ws.append_rows(tb_df[TABS["TiebreakerActuals"]].values.tolist())


def clear_caches():
    st.cache_resource.clear()
