import streamlit as st

def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
        /* Global background and text (no black) */
        body, .stApp {
            background-color: #f7f7f8;
            color: #374151;
        }

        /* Remove Streamlit default padding and make page full-height */
        .block-container {
            padding-top: 0;
            padding-bottom: 0;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* Wrapper for logo + hero, fills full viewport */
        .hero-wrapper {
            flex: 1;
            display: flex;
            flex-direction: column;
        }

        /* Centered landing container */
        .landing-container {
            max-width: 880px;
            margin: 0 auto;
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;   /* vertical center */
            align-items: center;       /* horizontal center */
            gap: 1.25rem;
        }

        .hero-title {
            text-align: center;
            color: #374151;
            margin-bottom: 0.75rem;
        }

        /* Bottom area + chat input background */
        [data-testid="stBottomBlock"] {
            background: #f7f7f8;
        }

        /* Main chat input bar (after first message) – white pill */
        [data-testid="stChatInput"] {
            background: #f7f7f8 !important;
            border-top: 1px solid #e5e7eb;
        }

        [data-testid="stChatInput"] > div {
            background: #ffffff !important;
            border-radius: 999px !important;
            border: 1px solid #e5e7eb !important;
        }

        /* Landing page text input styled as white pill */
        .landing-container [data-testid="stTextInput"] > div,
        .landing-container [data-testid="stTextInput"] > div > div {
            background: #ffffff !important;
            border-radius: 999px !important;
            border: 1px solid #e5e7eb !important;
        }

        .landing-container input {
            background: transparent !important;
            color: #4b5563 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )