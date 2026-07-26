from groq import Groq

from config import GROQ_API_KEY

from football_api import (
    get_team_info,
    get_last_matches,
    get_next_matches,
    get_league_table
)

from intent import (
    detect_intent,
    detect_team,
    detect_league
)

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are FootballGPT.

You are an expert football assistant.

Answer football questions accurately and concisely.
"""


def ask_groq(user_message):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        temperature=0.5
    )

    return response.choices[0].message.content


def get_response(messages):

    user_input = messages[-1]["content"]

    intent = detect_intent(user_input)

    team = detect_team(user_input)

    league = detect_league(user_input)

    if intent == "team_info":

        if team:
            return get_team_info(team)

        return "Please specify a supported team."

    elif intent == "last_matches":

        if team:
            return get_last_matches(team)

        return "Please specify a supported team."

    elif intent == "next_matches":

        if team:
            return get_next_matches(team)

        return "Please specify a supported team."

    elif intent == "standings":

        if league:
            return get_league_table(league)

        return "Please specify a supported league."

    return ask_groq(user_input)