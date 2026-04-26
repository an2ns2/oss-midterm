import streamlit as st


def initialize_session_state() -> None:
    defaults = {
        "logged_in": False,
        "login_error": "",
        "current_question_index": 0,
        "answers": {},
        "quiz_completed": False,
        "result_top3": [],
        "selected_profile_driver": None,
        "dialog_profile_driver": None,
        "show_share_text": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_quiz_state() -> None:
    st.session_state.current_question_index = 0
    st.session_state.answers = {}
    st.session_state.quiz_completed = False
    st.session_state.result_top3 = []
    st.session_state.selected_profile_driver = None
    st.session_state.dialog_profile_driver = None
    st.session_state.show_share_text = False
