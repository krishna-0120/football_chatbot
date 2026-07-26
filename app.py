import streamlit as st
from chatbot import get_response
from utils import export_chat


st.set_page_config(
    page_title="Football AI Assistant",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_css():
    with open("styles/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()


if "messages" not in st.session_state:
    st.session_state.messages = []

if "quick_prompt" not in st.session_state:
    st.session_state.quick_prompt = None



with st.sidebar:

    st.markdown(
        """
        <h2 style="color:#1F2937; margin-bottom:0;">
            ⚽ Football AI
        </h2>
            Your Personal Football Assistant
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.metric(
        label="Messages",
        value=len(st.session_state.messages)
    )

    st.divider()

    st.subheader("🔥 Quick Questions")

    quick_questions = [
        "🏆 Premier League Standings",
        "⚽ Barcelona Team Info",
        "📅 Liverpool Fixtures",
        "👑 Lionel Messi",
        "🚩 Explain Offside"
    ]

    for question in quick_questions:
        if st.button(question):
            st.session_state.quick_prompt = question

    st.divider()

    st.download_button(
        "📄 Export Chat",
        data=export_chat(st.session_state.messages),
        file_name="football_chat.txt",
        mime="text/plain"
    )

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.session_state.quick_prompt = None
        st.rerun()



st.markdown(
    """
    <div style="text-align:center; margin-top:10px; margin-bottom:25px;">
        <h1 style="
            color:#2563EB;
            margin-bottom:5px;
            font-size:48px;
            font-weight:700;
        ">
            ⚽ Football AI Assistant
        </h1>

            Powered by Groq + Football-Data API
    </div>
    """,
    unsafe_allow_html=True
)


if len(st.session_state.messages) == 0:

    st.markdown(
        """
        <div style="
            background:white;
            border:1px solid #E5E7EB;
            border-radius:14px;
            padding:20px;
            margin-bottom:20px;
            box-shadow:0 2px 8px rgba(0,0,0,.05);
        ">

        <h3 style="margin-top:0;">
            👋 Welcome!
        </h3>

        <p>
            Ask me anything about football.
        </p>

        <b>Popular questions</b>

        <ul>
            <li>🏆 Premier League Standings</li>
            <li>⚽ Barcelona Team Info</li>
            <li>📅 Liverpool Fixtures</li>
            <li>👑 Who is Lionel Messi?</li>
            <li>🚩 Explain the Offside Rule</li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )



for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])



prompt = st.chat_input("Ask anything about football...")


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

        with st.spinner("⚽ Thinking..."):

            response = get_response(st.session_state.messages)

            st.markdown(response)

    
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )


st.markdown(
    """
    <hr style="margin-top:30px;margin-bottom:10px;">

    <div style="
        text-align:center;
        color:#6B7280;
        font-size:14px;
        padding-bottom:15px;
    ">

    ⚽ Football AI Assistant • Built with Streamlit, Groq & Football-Data API

    </div>
    """,
    unsafe_allow_html=True
)