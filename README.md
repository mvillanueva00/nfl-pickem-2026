# NFL Pick'em 2026 (Weeks 3-18)

A Streamlit app so your pool submits picks online instead of passing around
Excel files. Same architecture as your World Cup predictor: a Google Sheet
acts as the database, a service account reads/writes it, and the app
deploys automatically via Streamlit Community Cloud on every GitHub push.

Three tabs:
- **Submit Picks** \u2014 each person types their name, picks a week, and selects
  a winner for every game. Once a game's kickoff time passes, that pick
  locks and can't be changed (still shows what was submitted, or "no pick"
  if they missed it). The week's last game also has a tiebreaker
  (combined total points), same as the printable sheet.
- **Scoreboard** \u2014 season standings (auto-totaled across all weeks) plus a
  week-by-week breakdown and tiebreaker comparison.
- **Admin** \u2014 PIN-gated. Enter each week's actual winners and the
  tiebreaker's actual point total; the scoreboard updates immediately.

## 1. Create the Google Sheet

1. Go to [sheets.google.com](https://sheets.google.com) and create a new,
   blank spreadsheet. Name it whatever you like (e.g. "NFL Pickem 2026").
2. Copy the Sheet's ID out of its URL:
   `https://docs.google.com/spreadsheets/d/`**`THIS_PART_IS_THE_ID`**`/edit`
3. Leave it otherwise empty \u2014 the app creates its own tabs (Picks,
   Tiebreakers, Results, TiebreakerActuals) automatically the first time it
   runs.

## 2. Create a Google Cloud service account

(Same steps as the World Cup app, if you still have that project you can
reuse it \u2014 otherwise:)

1. Go to [console.cloud.google.com](https://console.cloud.google.com), create
   or select a project.
2. Enable the **Google Sheets API** and **Google Drive API** for that
   project (APIs & Services -> Enable APIs and Services -> search each one).
3. Go to APIs & Services -> Credentials -> Create Credentials -> Service
   Account. Give it any name.
4. Open the new service account -> Keys -> Add Key -> Create new key -> JSON.
   This downloads a `.json` file \u2014 keep it private, you'll paste its
   contents into Streamlit's secrets in step 4.
5. Copy the service account's email address (looks like
   `xxx@xxx.iam.gserviceaccount.com`, also in that JSON file).
6. Open your Google Sheet from step 1 -> Share -> paste that service
   account email in -> give it **Editor** access.

## 3. Push this code to GitHub

Create a new repo (e.g. `nfl-pickem-2026`) and push everything in this
folder to it. `secrets.toml.example` is safe to commit; the real
`secrets.toml` is git-ignored on purpose \u2014 never commit real credentials.

## 4. Deploy on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io), sign in, and
   click "New app". Point it at your new repo, branch `main`, file `app.py`.
2. Before (or right after) it deploys, open the app's Settings -> Secrets
   and paste in a filled-out version of `secrets.toml.example`:
   - `sheet_id` \u2014 from step 1
   - `admin_pin` \u2014 whatever PIN you want to gate the Admin tab with
   - `[gcp_service_account]` \u2014 every field from the JSON key file you
     downloaded in step 2 (the field names match exactly; just copy each
     value over, keeping the `private_key` field's `\n` characters as-is)
3. Save. The app redeploys automatically and is now live at a
   `your-app-name.streamlit.app` URL you can share with the pool.

From here on, every `git push` to the repo redeploys the app automatically
\u2014 exactly like the World Cup app.

## Updating kickoff times

`schedule_data.py` estimates most kickoff times (early Sunday games default
to 1:00 PM ET, Thursday/Monday night games to their usual primetime slot,
etc.) since the NFL doesn't lock in every exact time this far ahead. As the
league flexes/confirms times closer to each week, open `schedule_data.py`
and add the real time as the 4th item in that game's tuple, e.g.:

```python
("Kansas City Chiefs", "Buffalo Bills", "2026-11-26", (20, 20)),
```

(hour, minute) in 24-hour ET. Push the change and the lock logic picks it
up automatically.

## Local testing

```bash
pip install -r requirements.txt
mkdir -p .streamlit && cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# edit .streamlit/secrets.toml with your real values, then:
streamlit run app.py
```
