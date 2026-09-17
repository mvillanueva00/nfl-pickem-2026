"""
2026 NFL season schedule, Weeks 3-18, for the Pick'em app.

Kickoff times are NOT all officially confirmed this far in advance (the NFL
sets/flexes exact Sunday windows closer to each week). To keep the lock
feature working today, each game is assigned a placeholder kickoff time
based on its day of the week (see DEFAULT_KICKOFF_ET below). Update the
`time` field for any game below once the real time is announced -- that's
the only thing you ever need to touch here as the season goes on.
"""
from datetime import datetime, time as dtime
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")

# Fallback kickoff time by weekday, used when a game's `time` field is None.
DEFAULT_KICKOFF_ET = {
    "Wed": dtime(20, 0),
    "Thu": dtime(20, 15),
    "Fri": dtime(15, 0),
    "Sat": dtime(16, 30),
    "Sun": dtime(13, 0),   # early window placeholder; late/SNF games will
                           # show as "locks earlier than reality" until you
                           # fill in the real time below
    "Mon": dtime(20, 15),
}

WEEKDAY_ABBR = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def _kickoff(date_str, time_override=None):
    """date_str: 'YYYY-MM-DD'. Returns a tz-aware datetime in ET."""
    d = datetime.strptime(date_str, "%Y-%m-%d")
    weekday = WEEKDAY_ABBR[d.weekday()]
    t = time_override or DEFAULT_KICKOFF_ET[weekday]
    return datetime.combine(d.date(), t, tzinfo=ET)


# (away, home, date "YYYY-MM-DD", optional time override as (hour, minute) in ET)
RAW_WEEKS = {
3: [
    ("Atlanta Falcons", "Green Bay Packers", "2026-09-24", None),
    ("LA Chargers", "Buffalo Bills", "2026-09-27", None),
    ("Carolina Panthers", "Cleveland Browns", "2026-09-27", None),
    ("NY Jets", "Detroit Lions", "2026-09-27", None),
    ("Houston Texans", "Indianapolis Colts", "2026-09-27", None),
    ("New England Patriots", "Jacksonville Jaguars", "2026-09-27", None),
    ("Kansas City Chiefs", "Miami Dolphins", "2026-09-27", None),
    ("Tennessee Titans", "NY Giants", "2026-09-27", None),
    ("Cincinnati Bengals", "Pittsburgh Steelers", "2026-09-27", None),
    ("Seattle Seahawks", "Washington Commanders", "2026-09-27", None),
    ("Arizona Cardinals", "San Francisco 49ers", "2026-09-27", None),
    ("Minnesota Vikings", "Tampa Bay Buccaneers", "2026-09-27", None),
    ("Baltimore Ravens", "Dallas Cowboys", "2026-09-27", None),
    ("Las Vegas Raiders", "New Orleans Saints", "2026-09-27", None),
    ("LA Rams", "Denver Broncos", "2026-09-27", None),
    ("Philadelphia Eagles", "Chicago Bears", "2026-09-28", None),
],
4: [
    ("Pittsburgh Steelers", "Cleveland Browns", "2026-10-01", None),
    ("Indianapolis Colts", "Washington Commanders", "2026-10-04", None),
    ("Tennessee Titans", "Baltimore Ravens", "2026-10-04", None),
    ("New England Patriots", "Buffalo Bills", "2026-10-04", None),
    ("NY Jets", "Chicago Bears", "2026-10-04", None),
    ("Jacksonville Jaguars", "Cincinnati Bengals", "2026-10-04", None),
    ("Dallas Cowboys", "Houston Texans", "2026-10-04", None),
    ("Arizona Cardinals", "NY Giants", "2026-10-04", None),
    ("LA Rams", "Philadelphia Eagles", "2026-10-04", None),
    ("Green Bay Packers", "Tampa Bay Buccaneers", "2026-10-04", None),
    ("Miami Dolphins", "Minnesota Vikings", "2026-10-04", None),
    ("Kansas City Chiefs", "Las Vegas Raiders", "2026-10-04", None),
    ("LA Chargers", "Seattle Seahawks", "2026-10-04", None),
    ("Denver Broncos", "San Francisco 49ers", "2026-10-04", None),
    ("Detroit Lions", "Carolina Panthers", "2026-10-04", None),
    ("Atlanta Falcons", "New Orleans Saints", "2026-10-05", None),
],
5: [
    ("Tampa Bay Buccaneers", "Dallas Cowboys", "2026-10-08", None),
    ("Philadelphia Eagles", "Jacksonville Jaguars", "2026-10-11", None),
    ("Cincinnati Bengals", "Miami Dolphins", "2026-10-11", None),
    ("Las Vegas Raiders", "New England Patriots", "2026-10-11", None),
    ("Minnesota Vikings", "New Orleans Saints", "2026-10-11", None),
    ("Cleveland Browns", "NY Jets", "2026-10-11", None),
    ("Indianapolis Colts", "Pittsburgh Steelers", "2026-10-11", None),
    ("Houston Texans", "Tennessee Titans", "2026-10-11", None),
    ("NY Giants", "Washington Commanders", "2026-10-11", None),
    ("Denver Broncos", "LA Chargers", "2026-10-11", None),
    ("Detroit Lions", "Arizona Cardinals", "2026-10-11", None),
    ("Chicago Bears", "Green Bay Packers", "2026-10-11", None),
    ("San Francisco 49ers", "Seattle Seahawks", "2026-10-11", None),
    ("Baltimore Ravens", "Atlanta Falcons", "2026-10-11", None),
    ("Buffalo Bills", "LA Rams", "2026-10-12", None),
],
6: [
    ("Seattle Seahawks", "Denver Broncos", "2026-10-15", None),
    ("Houston Texans", "Jacksonville Jaguars", "2026-10-18", None),
    ("Chicago Bears", "Atlanta Falcons", "2026-10-18", None),
    ("Baltimore Ravens", "Cleveland Browns", "2026-10-18", None),
    ("Tennessee Titans", "Indianapolis Colts", "2026-10-18", None),
    ("NY Jets", "New England Patriots", "2026-10-18", None),
    ("New Orleans Saints", "NY Giants", "2026-10-18", None),
    ("Carolina Panthers", "Philadelphia Eagles", "2026-10-18", None),
    ("Pittsburgh Steelers", "Tampa Bay Buccaneers", "2026-10-18", None),
    ("Arizona Cardinals", "LA Rams", "2026-10-18", None),
    ("LA Chargers", "Kansas City Chiefs", "2026-10-18", None),
    ("Buffalo Bills", "Las Vegas Raiders", "2026-10-18", None),
    ("Dallas Cowboys", "Green Bay Packers", "2026-10-18", None),
    ("Washington Commanders", "San Francisco 49ers", "2026-10-19", None),
],
7: [
    ("New England Patriots", "Chicago Bears", "2026-10-22", None),
    ("Pittsburgh Steelers", "New Orleans Saints", "2026-10-25", None),
    ("San Francisco 49ers", "Atlanta Falcons", "2026-10-25", None),
    ("Cincinnati Bengals", "Baltimore Ravens", "2026-10-25", None),
    ("Tampa Bay Buccaneers", "Carolina Panthers", "2026-10-25", None),
    ("NY Giants", "Houston Texans", "2026-10-25", None),
    ("Indianapolis Colts", "Minnesota Vikings", "2026-10-25", None),
    ("Miami Dolphins", "NY Jets", "2026-10-25", None),
    ("Cleveland Browns", "Tennessee Titans", "2026-10-25", None),
    ("Denver Broncos", "Arizona Cardinals", "2026-10-25", None),
    ("Green Bay Packers", "Detroit Lions", "2026-10-25", None),
    ("LA Rams", "Las Vegas Raiders", "2026-10-25", None),
    ("Kansas City Chiefs", "Seattle Seahawks", "2026-10-25", None),
    ("Dallas Cowboys", "Philadelphia Eagles", "2026-10-26", None),
],
8: [
    ("Carolina Panthers", "Green Bay Packers", "2026-10-29", None),
    ("Atlanta Falcons", "Tampa Bay Buccaneers", "2026-11-01", None),
    ("Baltimore Ravens", "Buffalo Bills", "2026-11-01", None),
    ("Tennessee Titans", "Cincinnati Bengals", "2026-11-01", None),
    ("Arizona Cardinals", "Dallas Cowboys", "2026-11-01", None),
    ("Minnesota Vikings", "Detroit Lions", "2026-11-01", None),
    ("Indianapolis Colts", "Jacksonville Jaguars", "2026-11-01", None),
    ("Las Vegas Raiders", "NY Jets", "2026-11-01", None),
    ("Cleveland Browns", "Pittsburgh Steelers", "2026-11-01", None),
    ("LA Chargers", "LA Rams", "2026-11-01", None),
    ("Kansas City Chiefs", "Denver Broncos", "2026-11-01", None),
    ("New England Patriots", "Miami Dolphins", "2026-11-01", None),
    ("Philadelphia Eagles", "Washington Commanders", "2026-11-01", None),
    ("Chicago Bears", "Seattle Seahawks", "2026-11-02", None),
],
9: [
    ("Jacksonville Jaguars", "Baltimore Ravens", "2026-11-05", None),
    ("Cincinnati Bengals", "Atlanta Falcons", "2026-11-08", None),
    ("Denver Broncos", "Carolina Panthers", "2026-11-08", None),
    ("Dallas Cowboys", "Indianapolis Colts", "2026-11-08", None),
    ("NY Jets", "Kansas City Chiefs", "2026-11-08", None),
    ("Detroit Lions", "Miami Dolphins", "2026-11-08", None),
    ("Cleveland Browns", "New Orleans Saints", "2026-11-08", None),
    ("NY Giants", "Philadelphia Eagles", "2026-11-08", None),
    ("LA Rams", "Washington Commanders", "2026-11-08", None),
    ("Houston Texans", "LA Chargers", "2026-11-08", None),
    ("Las Vegas Raiders", "San Francisco 49ers", "2026-11-08", None),
    ("Green Bay Packers", "New England Patriots", "2026-11-08", None),
    ("Arizona Cardinals", "Seattle Seahawks", "2026-11-08", None),
    ("Tampa Bay Buccaneers", "Chicago Bears", "2026-11-08", None),
    ("Buffalo Bills", "Minnesota Vikings", "2026-11-09", None),
],
10: [
    ("Washington Commanders", "NY Giants", "2026-11-12", None),
    ("New England Patriots", "Detroit Lions", "2026-11-15", None),
    ("Kansas City Chiefs", "Atlanta Falcons", "2026-11-15", None),
    ("Houston Texans", "Cleveland Browns", "2026-11-15", None),
    ("Minnesota Vikings", "Green Bay Packers", "2026-11-15", None),
    ("Miami Dolphins", "Indianapolis Colts", "2026-11-15", None),
    ("Carolina Panthers", "New Orleans Saints", "2026-11-15", None),
    ("Buffalo Bills", "NY Jets", "2026-11-15", None),
    ("Jacksonville Jaguars", "Tennessee Titans", "2026-11-15", None),
    ("LA Rams", "Arizona Cardinals", "2026-11-15", None),
    ("Seattle Seahawks", "Las Vegas Raiders", "2026-11-15", None),
    ("San Francisco 49ers", "Dallas Cowboys", "2026-11-15", None),
    ("Pittsburgh Steelers", "Cincinnati Bengals", "2026-11-15", None),
    ("LA Chargers", "Baltimore Ravens", "2026-11-16", None),
],
11: [
    ("Indianapolis Colts", "Houston Texans", "2026-11-19", None),
    ("Miami Dolphins", "Buffalo Bills", "2026-11-22", None),
    ("Baltimore Ravens", "Carolina Panthers", "2026-11-22", None),
    ("New Orleans Saints", "Chicago Bears", "2026-11-22", None),
    ("Tennessee Titans", "Dallas Cowboys", "2026-11-22", None),
    ("Tampa Bay Buccaneers", "Detroit Lions", "2026-11-22", None),
    ("Arizona Cardinals", "Kansas City Chiefs", "2026-11-22", None),
    ("Jacksonville Jaguars", "NY Giants", "2026-11-22", None),
    ("NY Jets", "LA Chargers", "2026-11-22", None),
    ("Las Vegas Raiders", "Denver Broncos", "2026-11-22", None),
    ("Pittsburgh Steelers", "Philadelphia Eagles", "2026-11-22", None),
    ("Minnesota Vikings", "San Francisco 49ers", "2026-11-22", None),
    ("Cincinnati Bengals", "Washington Commanders", "2026-11-23", None),
],
12: [
    ("Green Bay Packers", "LA Rams", "2026-11-25", None),
    ("Chicago Bears", "Detroit Lions", "2026-11-26", (13, 0)),
    ("Philadelphia Eagles", "Dallas Cowboys", "2026-11-26", (16, 30)),
    ("Kansas City Chiefs", "Buffalo Bills", "2026-11-26", (20, 20)),
    ("Denver Broncos", "Pittsburgh Steelers", "2026-11-27", None),
    ("New Orleans Saints", "Cincinnati Bengals", "2026-11-29", None),
    ("Las Vegas Raiders", "Cleveland Browns", "2026-11-29", None),
    ("Baltimore Ravens", "Houston Texans", "2026-11-29", None),
    ("NY Giants", "Indianapolis Colts", "2026-11-29", None),
    ("NY Jets", "Miami Dolphins", "2026-11-29", None),
    ("Atlanta Falcons", "Minnesota Vikings", "2026-11-29", None),
    ("Tennessee Titans", "Jacksonville Jaguars", "2026-11-29", None),
    ("Washington Commanders", "Arizona Cardinals", "2026-11-29", None),
    ("Seattle Seahawks", "San Francisco 49ers", "2026-11-29", None),
    ("New England Patriots", "LA Chargers", "2026-11-29", None),
    ("Carolina Panthers", "Tampa Bay Buccaneers", "2026-11-30", None),
],
13: [
    ("Kansas City Chiefs", "LA Rams", "2026-12-03", None),
    ("Detroit Lions", "Atlanta Falcons", "2026-12-06", None),
    ("Jacksonville Jaguars", "Chicago Bears", "2026-12-06", None),
    ("Cincinnati Bengals", "Cleveland Browns", "2026-12-06", None),
    ("Green Bay Packers", "New Orleans Saints", "2026-12-06", None),
    ("San Francisco 49ers", "NY Giants", "2026-12-06", None),
    ("LA Chargers", "Tampa Bay Buccaneers", "2026-12-06", None),
    ("Washington Commanders", "Tennessee Titans", "2026-12-06", None),
    ("Philadelphia Eagles", "Arizona Cardinals", "2026-12-06", None),
    ("Miami Dolphins", "Denver Broncos", "2026-12-06", None),
    ("Carolina Panthers", "Minnesota Vikings", "2026-12-06", None),
    ("Buffalo Bills", "New England Patriots", "2026-12-06", None),
    ("Houston Texans", "Pittsburgh Steelers", "2026-12-06", None),
    ("Dallas Cowboys", "Seattle Seahawks", "2026-12-07", None),
],
14: [
    ("Minnesota Vikings", "New England Patriots", "2026-12-10", None),
    ("Tampa Bay Buccaneers", "Baltimore Ravens", "2026-12-13", None),
    ("New Orleans Saints", "Carolina Panthers", "2026-12-13", None),
    ("Atlanta Falcons", "Cleveland Browns", "2026-12-13", None),
    ("Tennessee Titans", "Detroit Lions", "2026-12-13", None),
    ("Chicago Bears", "Miami Dolphins", "2026-12-13", None),
    ("Denver Broncos", "NY Jets", "2026-12-13", None),
    ("Indianapolis Colts", "Philadelphia Eagles", "2026-12-13", None),
    ("Houston Texans", "Washington Commanders", "2026-12-13", None),
    ("LA Chargers", "Las Vegas Raiders", "2026-12-13", None),
    ("Kansas City Chiefs", "Cincinnati Bengals", "2026-12-13", None),
    ("NY Giants", "Seattle Seahawks", "2026-12-13", None),
    ("LA Rams", "San Francisco 49ers", "2026-12-13", None),
    ("Buffalo Bills", "Green Bay Packers", "2026-12-13", None),
    ("Pittsburgh Steelers", "Jacksonville Jaguars", "2026-12-14", None),
],
15: [
    ("San Francisco 49ers", "LA Chargers", "2026-12-17", None),
    ("Seattle Seahawks", "Philadelphia Eagles", "2026-12-19", None),
    ("Chicago Bears", "Buffalo Bills", "2026-12-19", None),
    ("Cincinnati Bengals", "Carolina Panthers", "2026-12-20", None),
    ("Miami Dolphins", "Green Bay Packers", "2026-12-20", None),
    ("Jacksonville Jaguars", "Houston Texans", "2026-12-20", None),
    ("Cleveland Browns", "NY Giants", "2026-12-20", None),
    ("Baltimore Ravens", "Pittsburgh Steelers", "2026-12-20", None),
    ("New Orleans Saints", "Tampa Bay Buccaneers", "2026-12-20", None),
    ("Indianapolis Colts", "Tennessee Titans", "2026-12-20", None),
    ("Atlanta Falcons", "Washington Commanders", "2026-12-20", None),
    ("NY Jets", "Arizona Cardinals", "2026-12-20", None),
    ("Dallas Cowboys", "LA Rams", "2026-12-20", None),
    ("Denver Broncos", "Las Vegas Raiders", "2026-12-20", None),
    ("Detroit Lions", "Minnesota Vikings", "2026-12-20", None),
    ("New England Patriots", "Kansas City Chiefs", "2026-12-21", None),
],
16: [
    ("Houston Texans", "Philadelphia Eagles", "2026-12-24", None),
    ("Green Bay Packers", "Chicago Bears", "2026-12-25", (13, 0)),
    ("Buffalo Bills", "Denver Broncos", "2026-12-25", (16, 30)),
    ("LA Rams", "Seattle Seahawks", "2026-12-25", (20, 0)),
    ("Tampa Bay Buccaneers", "Atlanta Falcons", "2026-12-27", None),
    ("Cincinnati Bengals", "Indianapolis Colts", "2026-12-27", None),
    ("Washington Commanders", "Minnesota Vikings", "2026-12-27", None),
    ("Carolina Panthers", "Pittsburgh Steelers", "2026-12-27", None),
    ("Arizona Cardinals", "New Orleans Saints", "2026-12-27", None),
    ("New England Patriots", "NY Jets", "2026-12-27", None),
    ("Cleveland Browns", "Baltimore Ravens", "2026-12-27", None),
    ("LA Chargers", "Miami Dolphins", "2026-12-27", None),
    ("Tennessee Titans", "Las Vegas Raiders", "2026-12-27", None),
    ("San Francisco 49ers", "Kansas City Chiefs", "2026-12-27", None),
    ("Jacksonville Jaguars", "Dallas Cowboys", "2026-12-27", None),
    ("NY Giants", "Detroit Lions", "2026-12-28", None),
],
17: [
    ("Baltimore Ravens", "Cincinnati Bengals", "2026-12-31", None),
    ("Washington Commanders", "Jacksonville Jaguars", "2027-01-03", None),
    ("Kansas City Chiefs", "LA Chargers", "2027-01-03", None),
    ("Denver Broncos", "New England Patriots", "2027-01-03", None),
    ("LA Rams", "Tampa Bay Buccaneers", "2027-01-03", None),
    ("New Orleans Saints", "Atlanta Falcons", "2027-01-03", None),
    ("Seattle Seahawks", "Carolina Panthers", "2027-01-03", None),
    ("Indianapolis Colts", "Cleveland Browns", "2027-01-03", None),
    ("NY Giants", "Dallas Cowboys", "2027-01-03", None),
    ("Buffalo Bills", "Miami Dolphins", "2027-01-03", None),
    ("Minnesota Vikings", "NY Jets", "2027-01-03", None),
    ("Pittsburgh Steelers", "Tennessee Titans", "2027-01-03", None),
    ("Las Vegas Raiders", "Arizona Cardinals", "2027-01-03", None),
    ("Detroit Lions", "Chicago Bears", "2027-01-03", None),
    ("Philadelphia Eagles", "San Francisco 49ers", "2027-01-03", None),
    ("Houston Texans", "Green Bay Packers", "2027-01-04", None),
],
18: [
    ("San Francisco 49ers", "Arizona Cardinals", "2027-01-10", None),
    ("Pittsburgh Steelers", "Baltimore Ravens", "2027-01-10", None),
    ("NY Jets", "Buffalo Bills", "2027-01-10", None),
    ("Atlanta Falcons", "Carolina Panthers", "2027-01-10", None),
    ("Cleveland Browns", "Cincinnati Bengals", "2027-01-10", None),
    ("LA Chargers", "Denver Broncos", "2027-01-10", None),
    ("Detroit Lions", "Green Bay Packers", "2027-01-10", None),
    ("Tennessee Titans", "Houston Texans", "2027-01-10", None),
    ("Jacksonville Jaguars", "Indianapolis Colts", "2027-01-10", None),
    ("Las Vegas Raiders", "Kansas City Chiefs", "2027-01-10", None),
    ("Seattle Seahawks", "LA Rams", "2027-01-10", None),
    ("Chicago Bears", "Minnesota Vikings", "2027-01-10", None),
    ("Miami Dolphins", "New England Patriots", "2027-01-10", None),
    ("Tampa Bay Buccaneers", "New Orleans Saints", "2027-01-10", None),
    ("Philadelphia Eagles", "NY Giants", "2027-01-10", None),
    ("Dallas Cowboys", "Washington Commanders", "2027-01-10", None),
],
}

BYES = {
    3: [], 4: [], 5: ["Carolina Panthers", "Kansas City Chiefs"],
    6: ["Cincinnati Bengals", "Detroit Lions", "Miami Dolphins", "Minnesota Vikings"],
    7: ["Buffalo Bills", "Jacksonville Jaguars", "LA Chargers", "Washington Commanders"],
    8: ["Houston Texans", "New Orleans Saints", "NY Giants", "San Francisco 49ers"],
    9: ["Pittsburgh Steelers", "Tennessee Titans"],
    10: ["Chicago Bears", "Denver Broncos", "Philadelphia Eagles", "Tampa Bay Buccaneers"],
    11: ["Atlanta Falcons", "Cleveland Browns", "Green Bay Packers", "LA Rams", "New England Patriots", "Seattle Seahawks"],
    12: [], 13: ["Baltimore Ravens", "Indianapolis Colts", "Las Vegas Raiders", "NY Jets"],
    14: ["Arizona Cardinals", "Dallas Cowboys"], 15: [], 16: [], 17: [], 18: [],
}


def build_weeks():
    """Returns {week: [{"id","away","home","kickoff"(tz-aware dt),"label"}]}"""
    weeks = {}
    for wk, games in RAW_WEEKS.items():
        out = []
        for i, (away, home, date_str, time_override) in enumerate(games, start=1):
            kickoff = _kickoff(date_str, dtime(*time_override) if time_override else None)
            out.append({
                "id": f"w{wk}_g{i}",
                "away": away,
                "home": home,
                "kickoff": kickoff,
                # built manually instead of strftime's %-d / %-I, which
                # aren't supported on Windows
                "label": (
                    f"{kickoff.strftime('%a %b')} {kickoff.day}, "
                    f"{((kickoff.hour - 1) % 12) + 1}:{kickoff.strftime('%M %p')} ET"
                ),
            })
        weeks[wk] = out
    return weeks


WEEKS = build_weeks()
WEEK_NUMBERS = sorted(WEEKS.keys())
