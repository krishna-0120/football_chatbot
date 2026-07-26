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
    "fc barcelona",
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
    "champions league",
    "europa league",
    "conference league"
]


def detect_team(text):
    text = text.lower()

    teams = [
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

    for team in teams:
        if team in text:
            return team

    return None


def detect_league(text):
    text = text.lower()

    leagues = {
        "premier league": [
            "premier league",
            "epl",
            "english league"
        ],
        "la liga": [
            "la liga",
            "laliga",
            "spanish league"
        ],
        "bundesliga": [
            "bundesliga",
            "german league"
        ],
        "serie a": [
            "serie a",
            "italian league"
        ],
        "ligue 1": [
            "ligue 1",
            "french league"
        ],
        "champions league": [
            "champions league",
            "ucl"
        ]
    }

    for league, aliases in leagues.items():
        if any(alias in text for alias in aliases):
            return league

    return None




def detect_intent(text):
    text = text.lower().strip()

    # ---------------- TEAM INFO ----------------
    if any(word in text for word in [
        "team info",
        "club info",
        "information",
        "tell me about",
        "about"
    ]):
        return "team_info"

    # ---------------- STANDINGS ----------------
    if any(word in text for word in [
        "standings",
        "table",
        "points table",
        "league table",
        "rankings",
        "ranking",
        "position"
    ]):
        return "standings"

    # ---------------- UPCOMING MATCHES ----------------
    if any(word in text for word in [
        "next match",
        "next matches",
        "fixtures",
        "fixture",
        "schedule",
        "upcoming",
        "play next"
    ]):
        return "next_matches"

    # ---------------- LAST MATCHES ----------------
    if any(word in text for word in [
        "last match",
        "last matches",
        "recent match",
        "recent matches",
        "previous match",
        "results",
        "latest results"
    ]):
        return "last_matches"

    return "general"