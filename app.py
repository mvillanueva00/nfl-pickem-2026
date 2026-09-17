import datetime as dt
import streamlit as st
import pandas as pd

from schedule_data import WEEKS, WEEK_NUMBERS, BYES
import sheets_utils as db
import scoring

st.set_page_config(page_title="NFL Pick'em 2026", page_icon="\U0001F3C8", layout="wide")

# ---------------------------------------------------------------------------
def now_et():
    return dt.datetime.now(dt.timezone.utc)


def games_by_id(week):
    return {g["id"]: g for g in WEEKS[week]}


def is_locked(game):
    return now_et() >= game["kickoff"]


def existing_pick_map(picks_df, name, week):
    if picks_df.empty:
        return {}
    sub = picks_df[(picks_df["Name"] == name) & (picks_df["Week"].astype(str) == str(week))]
    return dict(zip(sub["GameID"], sub["Pick"]))


def existing_tiebreaker(tb_df, name, week):
    if tb_df.empty:
        return None
    sub = tb_df[(tb_df["Name"] == name) & (tb_df["Week"].astype(str) == str(week))]
    if sub.empty:
        return None
    return int(sub.iloc[0]["Guess"])


def has_submitted(picks_df, name, week):
    if picks_df.empty:
        return False
    sub = picks_df[(picks_df["Name"] == name) & (picks_df["Week"].astype(str) == str(week))]
    return not sub.empty


# ---------------------------------------------------------------------------
st.title("\U0001F3C8 NFL Pick'em 2026 \u2014 Weeks 3\u201318")

tab_submit, tab_board, tab_admin = st.tabs(["\U0001F4DD Submit Picks", "\U0001F4CB Scoreboard", "\U0001F512 Admin"])

# ============================== SUBMIT PICKS ===============================
with tab_submit:
    st.subheader("Submit Your Picks")
    col1, col2 = st.columns([2, 1])
    with col1:
        roster = db.get_roster()
        if roster:
            options = roster + ["\u2795 Someone not on this list"]
            selection = st.selectbox("Your name", options, index=None, placeholder="Choose your name")
            if selection == "\u2795 Someone not on this list":
                name = st.text_input("Type your name (ask the admin to add you to the Roster sheet)").strip()
            else:
                name = (selection or "").strip()
        else:
            st.info(
                "No roster set up yet \u2014 add names to the **Roster** tab in the Google "
                "Sheet to turn this into a dropdown. Typing works for now."
            )
            name = st.text_input("Your name (use the same spelling every week!)").strip()
    with col2:
        week = st.selectbox("Week", WEEK_NUMBERS, format_func=lambda w: f"Week {w}")

    if not name:
        st.info("Enter your name above to load or start your picks for this week.")
    else:
        gbid = games_by_id(week)
        picks_df = db.read_tab("Picks")
        tb_df = db.read_tab("Tiebreakers")
        prior_picks = existing_pick_map(picks_df, name, week)
        prior_tb = existing_tiebreaker(tb_df, name, week)
        submitted = has_submitted(picks_df, name, week)

        byes = BYES.get(week, [])
        if byes:
            st.caption("Bye this week: " + ", ".join(byes))

        if submitted:
            # ---- LOCKED, READ-ONLY VIEW -----------------------------------
            st.success(
                f"\u2705 **{name}'s Week {week} picks are locked in.** "
                "Picks can't be changed once submitted \u2014 same as the bracket rule "
                "on the World Cup app."
            )
            st.divider()
            for g in WEEKS[week]:
                pick = prior_picks.get(g["id"], "\u2014 no pick \u2014")
                c1, c2 = st.columns([3, 2])
                with c1:
                    st.markdown(f"**{g['away']} @ {g['home']}**  \n_{g['label']}_")
                with c2:
                    st.markdown(f"\U0001F512 **{pick}**")
                st.divider()

            finale = WEEKS[week][-1]
            tb_shown = prior_tb if prior_tb is not None else "\u2014 no guess \u2014"
            st.markdown(
                f"**Tiebreaker \u2014 total combined points, {finale['away']} @ {finale['home']}**  \n"
                f"\U0001F512 **{tb_shown}**"
            )
        else:
            # ---- OPEN FORM (first submission only) -------------------------
            st.caption(
                "Heads up: once you hit Submit, your whole week locks \u2014 no going "
                "back to change a pick, so double check before you submit. Games "
                "that have already kicked off can't be picked."
            )
            st.divider()
            new_picks = {}
            editable_ids = set()

            for g in WEEKS[week]:
                locked = is_locked(g)
                label = f"**{g['away']} @ {g['home']}**  \n_{g['label']}_"
                c1, c2 = st.columns([3, 2])
                with c1:
                    st.markdown(label)
                with c2:
                    options = [g["away"], g["home"]]
                    if locked:
                        st.markdown("\U0001F512 Game already started \u2014 can't pick")
                    else:
                        editable_ids.add(g["id"])
                        choice = st.radio(
                            "pick", options, index=None, key=f"pick_{week}_{g['id']}",
                            horizontal=True, label_visibility="collapsed",
                        )
                        new_picks[g["id"]] = choice
                st.divider()

            finale = WEEKS[week][-1]
            finale_locked = is_locked(finale)
            st.markdown(
                f"**Tiebreaker \u2014 total combined points, {finale['away']} @ {finale['home']}**"
            )
            if finale_locked:
                st.markdown("\U0001F512 Finale game already started \u2014 tiebreaker unavailable")
                tb_guess = None
            else:
                tb_guess = st.number_input(
                    "Total points guess", min_value=0, max_value=120,
                    value=44, step=1, key=f"tb_{week}",
                )

            missing = [g["away"] + " @ " + g["home"] for g in WEEKS[week]
                       if g["id"] in editable_ids and not new_picks.get(g["id"])]

            if st.button("Submit Picks (final \u2014 can't be changed after)",
                         type="primary", disabled=not editable_ids):
                if missing:
                    st.error("Pick a winner for every open game first: " + ", ".join(missing))
                else:
                    db.submit_picks(name, week, new_picks, editable_ids, gbid)
                    db.submit_tiebreaker(name, week, tb_guess, editable=not finale_locked)
                    st.cache_data.clear()
                    st.rerun()

# ================================ SCOREBOARD ================================
with tab_board:
    st.subheader("Season Standings")
    picks_df = db.read_tab("Picks")
    results_df = db.read_tab("Results")
    tb_df = db.read_tab("Tiebreakers")
    tb_actual_df = db.read_tab("TiebreakerActuals")

    if picks_df.empty:
        st.info("No picks submitted yet.")
    else:
        standings = scoring.season_standings(picks_df, results_df, WEEK_NUMBERS)
        st.dataframe(standings, use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("Week-by-Week Detail")
        wk_pick = st.selectbox("Choose a week to inspect", WEEK_NUMBERS, format_func=lambda w: f"Week {w}", key="board_week")
        wk_scores = scoring.weekly_scoreboard(picks_df, results_df, wk_pick)
        if wk_scores.empty:
            st.info(f"No picks submitted for Week {wk_pick} yet.")
        else:
            st.dataframe(wk_scores, use_container_width=True, hide_index=True)

        tb_table = scoring.tiebreaker_diff(tb_df, tb_actual_df, wk_pick)
        if not tb_table.empty:
            st.caption("Tiebreaker guesses (closest to actual wins ties)")
            st.dataframe(tb_table, use_container_width=True, hide_index=True)

# ================================== ADMIN ===================================
with tab_admin:
    st.subheader("Admin \u2014 Enter Results")
    pin = st.text_input("Admin PIN", type="password")
    if pin != str(st.secrets.get("admin_pin", "")):
        if pin:
            st.error("Incorrect PIN.")
        st.stop()

    admin_week = st.selectbox("Week to score", WEEK_NUMBERS, format_func=lambda w: f"Week {w}", key="admin_week")
    gbid = games_by_id(admin_week)
    results_df = db.read_tab("Results")
    existing_results = {}
    if not results_df.empty:
        sub = results_df[results_df["Week"].astype(str) == str(admin_week)]
        existing_results = dict(zip(sub["GameID"], sub["Winner"]))

    new_results = {}
    for g in WEEKS[admin_week]:
        options = ["", g["away"], g["home"]]
        prior = existing_results.get(g["id"], "")
        idx = options.index(prior) if prior in options else 0
        choice = st.selectbox(
            f"{g['away']} @ {g['home']}", options, index=idx,
            key=f"result_{admin_week}_{g['id']}",
        )
        new_results[g["id"]] = choice

    tb_actual_df = db.read_tab("TiebreakerActuals")
    prior_actual = None
    if not tb_actual_df.empty:
        sub = tb_actual_df[tb_actual_df["Week"].astype(str) == str(admin_week)]
        if not sub.empty:
            prior_actual = int(sub.iloc[0]["ActualTotal"])
    tb_actual = st.number_input(
        "Tiebreaker actual total (finale game)", min_value=0, max_value=150,
        value=prior_actual if prior_actual is not None else 0, step=1,
    )

    if st.button("Save Results", type="primary"):
        db.save_results(admin_week, new_results, gbid, tb_actual)
        st.success(f"Week {admin_week} results saved.")
        st.cache_data.clear()
        st.rerun()
