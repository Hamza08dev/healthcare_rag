from typing import List, Dict, Any
import streamlit as st


def render_header(logo_path: str) -> None:
    cols = st.columns([1, 6])
    with cols[0]:
        st.image(logo_path, width=130)
    with cols[1]:
        st.write("")


def render_chat(messages: List[Dict[str, Any]], doc_name: str | None) -> None:
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

    if doc_name:
        st.caption(f"Indexed document: **{doc_name}**")

    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    st.markdown("</div>", unsafe_allow_html=True)


def render_footer_notice() -> None:
    st.markdown(
        "<p style='text-align:center;color:#9ca3af;font-size:0.8rem;'>"
        "AI can make mistakes. Please double-check responses."
        "</p>",
        unsafe_allow_html=True,
    )
