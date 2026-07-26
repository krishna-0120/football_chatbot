import requests
from config import FOOTBALL_DATA_API_KEY

BASE_URL = "https://api.football-data.org/v4"

HEADERS = {
    "X-Auth-Token": FOOTBALL_DATA_API_KEY
}

TEAM_IDS = {
    "arsenal": 57,
    "aston villa": 58,
    "chelsea": 61,
    "everton": 62,
    "liverpool": 64,
    "manchester city": 65,
    "manchester united": 66,
    "newcastle": 67,
    "tottenham": 73,
    "barcelona": 81,
    "real madrid": 86,
    "atletico madrid": 78,
    "bayern munich": 5,
    "borussia dortmund": 4,
    "juventus": 109,
    "inter": 108,
    "milan": 98,
    "napoli": 113,
    "psg": 524
}

LEAGUES = {
    "premier league": "PL",
    "la liga": "PD",
    "bundesliga": "BL1",
    "serie a": "SA",
    "ligue 1": "FL1",
    "champions league": "CL"
}



def api_request(endpoint):
    try:
        response = requests.get(
            BASE_URL + endpoint,
            headers=HEADERS,
            timeout=20
        )

        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        return {"error": "The request timed out. Please try again."}

    except requests.exceptions.ConnectionError:
        return {"error": "Unable to connect to Football-Data API. Please check your internet connection."}

    except requests.exceptions.HTTPError as e:
        return {"error": f"API Error: {e.response.status_code}"}

    except Exception as e:
        return {"error": str(e)}


def get_team_id(team_name):
    return TEAM_IDS.get(team_name.lower())


def get_team_info(team_name):

    team_id = get_team_id(team_name)

    if not team_id:
        return "Team not supported."

    team = api_request(f"/teams/{team_id}")

    if "error" in team:
        return f"⚠️ {team['error']}"

    return f"""
## {team["name"]}

🏟 Stadium: {team["venue"]}

🌍 Country: {team["area"]["name"]}

🏆 Founded: {team["founded"]}

🎨 Club Colors: {team["clubColors"]}

🌐 Website: {team["website"]}
"""


def get_last_matches(team_name):

    team_id = get_team_id(team_name)

    if not team_id:
        return "Team not supported."

    data = api_request(f"/teams/{team_id}/matches?status=FINISHED&limit=5")

    if "error" in data:
        return f"⚠️ {data['error']}"

    matches = data["matches"]

    if not matches:
        return "No matches found."

    text = f"## Last 5 Matches - {team_name.title()}\n\n"

    for match in matches:

        home = match["homeTeam"]["shortName"]
        away = match["awayTeam"]["shortName"]

        home_score = match["score"]["fullTime"]["home"]
        away_score = match["score"]["fullTime"]["away"]

        date = match["utcDate"][:10]

        competition = match["competition"]["name"]

        text += (
            f"📅 {date}\n"
            f"🏆 {competition}\n"
            f"⚽ {home} {home_score}-{away_score} {away}\n\n"
        )

    return text


def get_next_matches(team_name):

    team_id = get_team_id(team_name)

    if not team_id:
        return "Team not supported."

    data = api_request(f"/teams/{team_id}/matches?status=SCHEDULED&limit=5")

    if "error" in data:
        return f"⚠️ {data['error']}"

    matches = data["matches"]

    if not matches:
        return "No upcoming matches."

    text = f"## Upcoming Matches - {team_name.title()}\n\n"

    for match in matches:

        home = match["homeTeam"]["shortName"]
        away = match["awayTeam"]["shortName"]

        date = match["utcDate"][:10]

        competition = match["competition"]["name"]

        text += (
            f"📅 {date}\n"
            f"🏆 {competition}\n"
            f"⚽ {home} vs {away}\n\n"
        )

    return text


def get_league_table(league):

    code = LEAGUES.get(league.lower())

    if not code:
        return "League not supported."

    data = api_request(f"/competitions/{code}/standings")

    if "error" in data:
        return f"⚠️ {data['error']}"

    table = data["standings"][0]["table"]

    text = f"## {data['competition']['name']} Standings\n\n"

    for club in table:

        text += (
            f"{club['position']:>2}. "
            f"{club['team']['shortName']:<20}"
            f"{club['points']} pts\n"
        )

    return text