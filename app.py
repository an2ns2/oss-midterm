import streamlit as st
import datetime  # 날짜/시간 출력을 위해 추가

from src.config import PAGE_CONFIG
from src.data import load_drivers, load_questions
from src.state import initialize_session_state
from src.ui import inject_styles, render_login_screen, render_quiz_screen, render_result_screen

st.set_page_config(**PAGE_CONFIG)

def main() -> None:

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{now}] [Log]")
    
    if st.session_state:
        print(">>> [상태 변경 내역] <<<")
        for key, value in st.session_state.items():
            print(f"  - {key}: {value}")
    else:
        print(">>> [초기 접속] <<<")
    print("-" * 50)
    # ----------------------------------------------------

    inject_styles()
    initialize_session_state()

    drivers = load_drivers()
    questions = load_questions()

    if not st.session_state.logged_in:
        render_login_screen()
    elif st.session_state.quiz_completed:
        render_result_screen(drivers)
    else:
        render_quiz_screen(drivers, questions)

if __name__ == "__main__":
    main()