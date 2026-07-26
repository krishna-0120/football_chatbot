import streamlit as st
from chatbot import get_response
from utils import export_chat


st.set_page_config(
    page_title="Football AI Assistant",
    page_icon="⚽",
    layout="wide"
)



def load_css():
    with open("styles/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )


load_css()



if "messages" not in st.session_state:
    st.session_state.messages = []

if "quick_prompt" not in st.session_state:
    st.session_state.quick_prompt = None



with st.sidebar:

    st.title("⚽ Football AI")

    st.caption("Your Personal Football Assistant")

    st.divider()

    st.metric(
        "Messages",
        len(st.session_state.messages)
    )

    st.divider()

    st.subheader("Quick Questions")

    quick_questions = [
    "Barcelona team info",
    "Explain the offside rule",
    "Premier League standings",
    "Who has won the most Champions League titles?",
    "Top 10 football players of all time"
]

    for question in quick_questions:
        if st.button(question):
            st.session_state.quick_prompt = question

    st.divider()

    st.download_button(
        label="📄 Export Chat",
        data=export_chat(st.session_state.messages),
        file_name="football_chat.txt",
        mime="text/plain",
    )

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.session_state.quick_prompt = None
        st.rerun()



st.title("⚽ Football AI Assistant")

st.markdown(
    "Ask me anything about football. "
    "From World Cups to tactics, players, clubs and history."
)



if len(st.session_state.messages) == 0:

    st.info(
        """
### Welcome!

You can ask questions about:

- 🏆 FIFA World Cup
- ⚽ UEFA Champions League
- 👑 Lionel Messi & Cristiano Ronaldo
- 📊 Football tactics
- 🎯 Rules of football
- 🌍 International football
- 🏅 Club football

Or use one of the quick questions in the sidebar.
"""
    )



for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])




prompt = st.chat_input("Ask a football question...")

if st.session_state.quick_prompt:
    prompt = st.session_state.quick_prompt
    st.session_state.quick_prompt = None



if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("⚽ Analyzing football knowledge..."):

            try:

                response = get_response(
                    st.session_state.messages
                )

            except Exception as e:

                response = f"❌ Error:\n\n{e}"

            st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )