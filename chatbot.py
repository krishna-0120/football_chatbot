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
You are FootballGPT, an expert football assistant.

Guidelines:
- Answer football-related questions accurately and clearly.
- Keep responses concise but informative.
- Use bullet points when appropriate.
- If the question is not related to football, politely answer it normally.
"""


def ask_groq(user_message):
    """Send general football questions to Groq."""

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
    """Route user requests to either Football API or Groq."""

    user_input = messages[-1]["content"]

    intent = detect_intent(user_input)
    team = detect_team(user_input)
    league = detect_league(user_input)

    try:

        if intent == "team_info":

            if not team:
                return "⚠️ Please mention a supported football team."

            return get_team_info(team)

        elif intent == "last_matches":

            if not team:
                return "⚠️ Please mention a supported football team."

            return get_last_matches(team)

        elif intent == "next_matches":

            if not team:
                return "⚠️ Please mention a supported football team."

            return get_next_matches(team)

        elif intent == "standings":

            if not league:
                return "⚠️ Please mention a supported league."

            return get_league_table(league)

        # Everything else goes to Groq
        return ask_groq(user_input)

    except Exception:
        return (
            "⚠️ Sorry, I couldn't retrieve that information right now.\n\n"
            "Please check your internet connection or try again in a few seconds."
        )