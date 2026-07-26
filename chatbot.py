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

You ONLY answer football (soccer) related questions.

If a user asks anything unrelated to football,
politely refuse by saying:

"I'm sorry, but I'm designed only to answer football-related questions."

Never answer non-football questions.

Keep answers concise and informative.
"""


def is_football_query(question):
    """Use Groq to classify whether a question is football-related."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content":
                "Reply ONLY with YES or NO.\n"
                "YES = football question.\n"
                "NO = not football."
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0
    )

    answer = response.choices[0].message.content.strip().upper()

    return answer.startswith("YES")


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

    if not is_football_query(user_input):
        return (
            "⚽ I'm a Football AI Assistant and can only answer football-related questions.\n\n"
            "You can ask me about:\n"
            "• Players\n"
            "• Clubs\n"
            "• Fixtures\n"
            "• Standings\n"
            "• Transfers\n"
            "• Football Rules\n"
            "• Competitions\n"
        )

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

        return ask_groq(user_input)

    except Exception:
        return (
            "⚠️ Sorry, I couldn't retrieve that information right now.\n\n"
            "Please try again in a few seconds."
        )