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
    detect_league,
    is_greeting,
    is_football_question
)

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are FootballGPT, a professional football (soccer) assistant.

Rules:
- Answer ONLY football-related questions.
- If a question is unrelated to football, politely reply:
  "I'm sorry, but I'm designed only to answer football-related questions."
- Never answer questions outside football.
- Be concise, accurate and friendly.
"""


def ask_groq(question):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()


def get_response(messages):

    user_input = messages[-1]["content"].strip()

    # ---------------- Greetings ----------------

    if is_greeting(user_input):

        greeting = user_input.lower()

        if "bye" in greeting or "goodbye" in greeting:
            return "👋 Goodbye! Feel free to come back anytime for football news, fixtures and player information."

        if "thank" in greeting:
            return "⚽ You're welcome! Ask me anything about football."

        return "⚽ Hello! I'm FootballGPT.\n\nAsk me anything about clubs, players, fixtures, standings, transfers or football history."

    # ---------------- Reject non-football ----------------

    if not is_football_question(user_input):
        return (
            "⚽ I'm a Football AI Assistant.\n\n"
            "I can only answer football-related questions.\n\n"
            "Examples:\n"
            "• Tell me about Arsenal\n"
            "• Premier League standings\n"
            "• Barcelona next match\n"
            "• Who is Lionel Messi?\n"
            "• Explain the offside rule"
        )

    intent = detect_intent(user_input)
    team = detect_team(user_input)
    league = detect_league(user_input)

    try:

        if intent == "team_info":

            if team:
                return get_team_info(team)

            return "⚽ Please mention a supported football club."

        elif intent == "last_matches":

            if team:
                return get_last_matches(team)

            return "⚽ Please mention a supported football club."

        elif intent == "next_matches":

            if team:
                return get_next_matches(team)

            return "⚽ Please mention a supported football club."

        elif intent == "standings":

            if league:
                return get_league_table(league)

            return "⚽ Please mention a supported league."

        # Everything else goes to Groq
        return ask_groq(user_input)

    except Exception as e:
        return f"⚠️ Something went wrong.\n\n{str(e)}"