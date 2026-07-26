import re

TEAM_NAMES = [
    "arsenal",
    "aston villa",
    "chelsea",
    "everton",
    "liverpool",
    "manchester city",
    "manchester united",
    "newcastle",
    "tottenham",
    "barcelona",
    "real madrid",
    "atletico madrid",
    "bayern munich",
    "borussia dortmund",
    "juventus",
    "inter",
    "milan",
    "napoli",
    "psg"
]

LEAGUES = [
    "premier league",
    "la liga",
    "bundesliga",
    "serie a",
    "ligue 1",
    "champions league"
]


def detect_team(text):
    text = text.lower()

    for team in TEAM_NAMES:
        if team in text:
            return team

    return None


def detect_league(text):
    text = text.lower()

    for league in LEAGUES:
        if league in text:
            return league

    return None


def detect_intent(text):

    text = text.lower()

    if any(word in text for word in [
        "standings",
        "table",
        "points table",
        "league table"
    ]):
        return "standings"

    if any(word in text for word in [
        "last match",
        "last matches",
        "previous matches",
        "recent matches"
    ]):
        return "last_matches"

    if any(word in text for word in [
        "next match",
        "next matches",
        "fixtures",
        "upcoming"
    ]):
        return "next_matches"

    if any(word in text for word in [
        "team info",
        "information",
        "stadium",
        "founded",
        "club"
    ]):
        return "team_info"

    return "chat"