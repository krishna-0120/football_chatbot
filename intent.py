import re

# -----------------------------
# Supported Teams
# -----------------------------

TEAM_ALIASES = {
    "arsenal": ["arsenal"],
    "aston villa": ["aston villa", "villa"],
    "chelsea": ["chelsea"],
    "everton": ["everton"],
    "liverpool": ["liverpool"],
    "manchester city": ["manchester city", "man city", "city"],
    "manchester united": ["manchester united", "man utd", "man united", "united"],
    "newcastle": ["newcastle"],
    "tottenham": ["tottenham", "spurs"],
    "barcelona": ["barcelona", "fc barcelona", "barca"],
    "real madrid": ["real madrid", "madrid"],
    "atletico madrid": ["atletico madrid", "atletico"],
    "bayern munich": ["bayern", "bayern munich"],
    "borussia dortmund": ["dortmund", "borussia dortmund"],
    "juventus": ["juventus", "juve"],
    "inter": ["inter", "inter milan"],
    "milan": ["ac milan", "milan"],
    "napoli": ["napoli"],
    "psg": ["psg", "paris saint germain"]
}

# -----------------------------
# Supported Leagues
# -----------------------------

LEAGUE_ALIASES = {
    "premier league": [
        "premier league",
        "epl",
        "english premier league"
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


# -----------------------------
# Greetings
# -----------------------------

def is_greeting(text):

    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
        "bye",
        "goodbye",
        "thanks",
        "thank you",
        "how are you"
    ]

    text = text.lower().strip()

    return any(g in text for g in greetings)


# -----------------------------
# Team Detection
# -----------------------------

def detect_team(text):

    text = text.lower()

    for team, aliases in TEAM_ALIASES.items():
        if any(alias in text for alias in aliases):
            return team

    return None


# -----------------------------
# League Detection
# -----------------------------

def detect_league(text):

    text = text.lower()

    for league, aliases in LEAGUE_ALIASES.items():
        if any(alias in text for alias in aliases):
            return league

    return None


# -----------------------------
# Intent Detection
# -----------------------------

def detect_intent(text):

    text = text.lower()

    if any(word in text for word in [
        "standings",
        "table",
        "points table",
        "league table",
        "ranking",
        "rankings",
        "position"
    ]):
        return "standings"

    if any(word in text for word in [
        "fixture",
        "fixtures",
        "next match",
        "upcoming",
        "schedule",
        "play next"
    ]):
        return "next_matches"

    if any(word in text for word in [
        "last match",
        "last matches",
        "results",
        "recent matches",
        "recent match",
        "previous match"
    ]):
        return "last_matches"

    if any(word in text for word in [
        "team",
        "club",
        "stadium",
        "coach",
        "manager",
        "captain",
        "founded",
        "about"
    ]):
        return "team_info"

    return "general"


# -----------------------------
# Football Detection
# -----------------------------

FOOTBALL_TERMS = [

    "football",
    "soccer",
    "fifa",
    "uefa",
    "goal",
    "match",
    "fixture",
    "league",
    "club",
    "player",
    "coach",
    "stadium",
    "transfer",
    "offside",
    "penalty",
    "referee",
    "world cup",
    "champions league",
    "premier league",
    "la liga",
    "bundesliga",
    "serie a",
    "ligue 1",
    "messi",
    "ronaldo",
    "haaland",
    "mbappe",
    "neymar",
    "yamal",
    "bellingham",
    "vinicius"
]


def is_football_question(text):

    text = text.lower()

    if is_greeting(text):
        return True

    if detect_team(text):
        return True

    if detect_league(text):
        return True

    if any(term in text for term in FOOTBALL_TERMS):
        return True

    return False