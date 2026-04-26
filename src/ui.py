import base64

import streamlit as st

from src.config import (
    PODIUM_IMAGE_PATH,
    STUDENT_ID,
    STUDENT_NAME,
    VALID_PASSWORD,
    VALID_USERNAME,
)
from src.data import (
    encode_image_to_base64,
    get_driver_map,
    get_driver_profile_image_path,
)
from src.logic import calculate_top3
from src.state import reset_quiz_state


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

        html, body { background: #09090D !important; }
        .stApp {
            background:
                repeating-linear-gradient(
                    -57deg,
                    transparent 0px, transparent 28px,
                    rgba(255,255,255,0.016) 28px, rgba(255,255,255,0.016) 29px
                ),
                #09090D;
            color: #f0f0f5;
            font-family: 'Orbitron', 'Noto Sans KR', system-ui, sans-serif;
        }
        .stApp::before {
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, #E8002D 0%, #FF4500 100%);
            z-index: 9999;
            pointer-events: none;
        }
        .hero-card { background: transparent; border: none; padding: 0; }
        .info-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-top: 2px solid #E8002D;
            border-radius: 0;
            padding: 1rem 1.2rem;
        }
        .info-card h3 {
            font-family: 'Orbitron', 'Noto Sans KR', sans-serif;
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 2.5px;
            text-transform: uppercase;
            color: #E8002D;
            margin: 0 0 0.5rem 0;
        }
        .info-card p {
            color: rgba(255,255,255,0.5);
            font-size: 0.82rem;
            line-height: 1.55;
            margin-bottom: 0.3rem;
        }
        .info-card strong { color: rgba(255,255,255,0.85); }
        .info-card code {
            background: rgba(232,0,45,0.15);
            color: #ff7090;
            padding: 0.1rem 0.45rem;
            border-radius: 0;
            font-size: 0.82rem;
        }
        .result-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 0;
            padding: 1.2rem;
        }
        .student-badge {
            display: inline-flex;
            align-items: center;
            padding: 0.28rem 0.75rem;
            background: rgba(232,0,45,0.08);
            border: 1px solid rgba(232,0,45,0.22);
            border-radius: 0;
            margin-bottom: 0.6rem;
            font-family: 'Orbitron', 'Noto Sans KR', sans-serif;
            font-size: 0.7rem;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: rgba(255,255,255,0.6);
        }
        [data-testid="stAppViewContainer"] > .main > .block-container {
            padding-top: 1.2rem !important;
            padding-bottom: 1rem !important;
        }
        .small-note { color: rgba(255,255,255,0.4); font-size: 0.875rem; line-height: 1.7; }
        .result-rank {
            font-size: 0.75rem; color: #E8002D;
            letter-spacing: 0.15em; text-transform: uppercase; font-weight: 700;
            font-family: 'Orbitron', 'Noto Sans KR', sans-serif;
        }
        .result-name { font-size: 1.35rem; font-weight: 700; margin: 0.3rem 0 0.15rem 0; }
        .result-team { color: rgba(255,255,255,0.45); margin-bottom: 0.75rem; }
        [data-testid="stTextInput"] input {
            background: rgba(255,255,255,0.06) !important;
            color: #ffffff !important;
            border: 1px solid rgba(255,255,255,0.14) !important;
            border-radius: 0 !important;
            font-family: 'Orbitron', 'Noto Sans KR', sans-serif !important;
            font-size: 1rem !important;
            letter-spacing: 0.3px !important;
        }
        [data-testid="stTextInput"] input:focus {
            background: rgba(255,255,255,0.09) !important;
            border-color: #E8002D !important;
            box-shadow: 0 0 0 1px rgba(232,0,45,0.25) !important;
        }
        [data-testid="stTextInput"] label {
            font-family: 'Orbitron', 'Noto Sans KR', sans-serif !important;
            font-size: 0.68rem !important;
            letter-spacing: 2px !important;
            text-transform: uppercase !important;
            color: rgba(255,255,255,0.38) !important;
        }
        [data-testid="stFormSubmitButton"] button {
            background: #E8002D !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 0 !important;
            font-family: 'Orbitron', 'Noto Sans KR', sans-serif !important;
            font-size: 1rem !important;
            font-weight: 700 !important;
            letter-spacing: 3px !important;
            text-transform: uppercase !important;
        }
        [data-testid="stFormSubmitButton"] button:hover {
            background: #c4001f !important;
            box-shadow: 0 0 22px rgba(232,0,45,0.4) !important;
        }
        [class*="st-key-quiz_reset_btn"] button,
        [class*="st-key-quiz_prev_btn"] button {
            background: transparent !important;
            color: rgba(255,255,255,0.35) !important;
            border: 1px solid rgba(255,255,255,0.12) !important;
            border-radius: 0 !important;
            font-family: 'Orbitron', 'Noto Sans KR', sans-serif !important;
            font-size: 0.72rem !important;
            letter-spacing: 2px !important;
            text-transform: uppercase !important;
        }
        [class*="st-key-quiz_reset_btn"] button:hover,
        [class*="st-key-quiz_prev_btn"] button:hover {
            color: rgba(255,255,255,0.7) !important;
            border-color: rgba(255,255,255,0.28) !important;
            background: rgba(255,255,255,0.05) !important;
        }
        [class*="st-key-quiz_prev_btn"] button:disabled { opacity: 0.2 !important; }
        [data-testid="stProgressBar"] > div {
            background: rgba(255,255,255,0.07) !important;
            border-radius: 0 !important;
            height: 3px !important;
        }
        [data-testid="stProgressBar"] > div > div {
            background: linear-gradient(90deg, #E8002D 0%, #FF4500 100%) !important;
            border-radius: 0 !important;
            box-shadow: 0 0 8px rgba(232,0,45,0.5) !important;
        }
        [data-testid="stAlert"] {
            background: rgba(232,0,45,0.08) !important;
            border: 1px solid rgba(232,0,45,0.22) !important;
            border-radius: 0 !important;
            color: #ff8099 !important;
        }
        details summary { color: rgba(255,255,255,0.4) !important; font-size: 0.82rem !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_student_header() -> None:
    st.markdown(
        f"""
        <div class="student-badge" style="padding: 6px 10px; font-size: 0.7rem; font-weight: bold;">
            <span style="color:#E8002D; margin-right:0.5rem;">&#9632;</span>
            {STUDENT_ID} &nbsp;&nbsp; {STUDENT_NAME}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_profile_contents(driver: dict) -> None:
    image_col, info_col = st.columns([0.95, 1.35], gap="large")

    with image_col:
        profile_image_path = get_driver_profile_image_path(driver)
        if profile_image_path:
            st.image(str(profile_image_path), use_container_width=True)
        else:
            st.caption("드라이버 프로필 이미지가 없습니다.")

    with info_col:
        st.markdown(f"### {driver['name']}")
        st.write(f"**팀**: {driver['team']}")
        st.write(f"**국적**: {driver['nationality']}")
        st.write(f"**드라이버 소개**: {driver['short_profile']}")
        st.write(f"**팀 소개**: {driver['team_profile']}")
        st.write(f"**주요 특성**: {', '.join(driver['traits'])}")


HAS_DIALOG = hasattr(st, "dialog")

if HAS_DIALOG:

    @st.dialog("드라이버 + 팀 프로필")
    def show_profile_dialog(driver: dict) -> None:
        render_profile_contents(driver)


def render_login_screen() -> None:
    render_student_header()
    st.markdown(
        """
        <div style="position:relative; padding:1rem 0 0.8rem 0; overflow:hidden;">
            <div style="
                position:absolute; right:-1rem; top:-1rem;
                font-family:'Orbitron','Noto Sans KR',sans-serif;
                font-size:10rem; line-height:1; color:rgba(255,255,255,0.022);
                pointer-events:none; user-select:none; letter-spacing:-4px;
            ">F1</div>
            <div style="
                position:absolute; left:0; top:0; bottom:0;
                width:3px;
                background:linear-gradient(180deg,#E8002D 0%,rgba(232,0,45,0) 100%);
            "></div>
            <div style="padding-left:1.5rem; position:relative; z-index:1;">
                <p style="
                    font-family:'Orbitron','Noto Sans KR',sans-serif;
                    font-size:0.65rem; font-weight:700;
                    letter-spacing:3px; text-transform:uppercase;
                    color:#E8002D; margin:0 0 0.5rem 0;
                ">FORMULA 1 &nbsp;·&nbsp; DRIVER QUIZ &nbsp;·&nbsp; 2026</p>
                <h1 style="
                    font-family:'Orbitron','Noto Sans KR',sans-serif;
                    font-size:clamp(2rem,3.5vw,3rem);
                    font-weight:400; line-height:1.15;
                    color:#ffffff; margin:0 0 0.7rem 0;
                    letter-spacing:3px; text-transform:uppercase;
                ">나의 최애 드라이버는?!</h1>
                <p style="
                    color:rgba(255,255,255,0.38);
                    font-size:0.82rem; line-height:1.55;
                    max-width:420px; margin:0; letter-spacing:0.3px;
                ">8개 항목에 답하면, 현역 F1 드라이버 22명 중 취향에 가장 잘 맞는 TOP 3를 추천해드릴게용</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left_col, right_col = st.columns([1.1, 0.9])

    with left_col:
        st.markdown(
            """
            <div class="info-card">
                <h3>F1과 22명의 선수들</h3>
                <p>포뮬러 원(Formula 1)은 세계 최고 수준의 단일 시트 오픈 휠 레이싱 시리즈입니다.
                매 시즌 10개 팀, <strong>22명의 드라이버</strong>가 20개 이상의 그랑프리를 누비며
                드라이버 챔피언십과 컨스트럭터 챔피언십을 다툽니다.</p>
                <p>2026 시즌에는 레드불·페라리·맥라렌·메르세데스 등 전통 강호들과
                신생팀 캐딜락이 합류해 역대 가장 치열한 그리드가 완성됐습니다.</p>
                <p><strong>데모 로그인</strong>: <code>ahran</code> / <code>1234</code></p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.expander("F1 기본 규칙 & 역사 알아보기"):
            st.markdown(
                """
**포뮬러 원이란?**  
F1은 1950년 영국 실버스톤에서 첫 번째 월드 챔피언십 레이스가 열리며 시작됐습니다.
현재는 FIA(국제자동차연맹)가 주관하는 세계 최상위 모터스포츠 시리즈입니다.

**레이스 주말 구조**  
- **FP1 · FP2 · FP3** — 자유 연습 세션 (금·토)
- **예선(Qualifying)** — 토요일, Q1→Q2→Q3 방식으로 그리드 결정
- **결승(Race)** — 일요일, 305km 이상 완주

**포인트 시스템**  
1위 25점 · 2위 18점 · 3위 15점 … 10위 1점, 패스티스트 랩 +1점(포인트권 내)

**드라이버 챔피언 계보**  
아이르톤 세나, 미하엘 슈마허(7회), 루이스 해밀턴(7회), 막스 페르스타펜(4연속) 등
전설적인 이름들이 F1의 역사를 수놓았습니다.
                """
            )

    with right_col:
        with st.form("login_form"):
            username = st.text_input("아이디")
            password = st.text_input("비밀번호", type="password")
            submitted = st.form_submit_button("로그인", use_container_width=True)

        if submitted:
            if username == VALID_USERNAME and password == VALID_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.login_error = ""
                reset_quiz_state()
                st.rerun()
            else:
                st.session_state.logged_in = False
                st.session_state.login_error = "로그인 실패: 아이디 또는 비밀번호를 확인하세요."

        if st.session_state.login_error:
            st.error(st.session_state.login_error)


def render_quiz_screen(drivers, questions) -> None:
    total_questions = len(questions)
    current_index = st.session_state.current_question_index
    current_question = questions[current_index]
    answered_count = len(st.session_state.answers)

    header_left, header_right = st.columns([0.58, 0.42])
    with header_left:
        st.markdown(
            f"""
            <div style="display:flex; align-items:baseline; gap:0.9rem; margin-bottom:0.1rem; padding-top:0.2rem;">
                <p style="
                    font-family:'Orbitron','Noto Sans KR',sans-serif;
                    font-size:0.65rem; font-weight:700;
                    letter-spacing:3px; text-transform:uppercase;
                    color:#E8002D; margin:0;
                ">F1 DRIVER QUIZ</p>
                <span style="
                    font-family:'Orbitron','Noto Sans KR',sans-serif;
                    font-size:0.65rem; font-weight:600;
                    letter-spacing:2px; text-transform:uppercase;
                    color:rgba(255,255,255,0.32);
                ">{answered_count}&nbsp;/&nbsp;{total_questions} ANSWERED</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with header_right:
        btn_prev_col, btn_reset_col = st.columns(2)
        with btn_prev_col:
            if st.button("이전 항목", key="quiz_prev_btn", disabled=current_index == 0, use_container_width=True):
                st.session_state.current_question_index -= 1
                st.rerun()
        with btn_reset_col:
            if st.button("처음부터 다시", key="quiz_reset_btn", use_container_width=True):
                reset_quiz_state()
                st.rerun()

    st.progress((current_index + 1) / total_questions, text="")

    question_text = current_question["title"]
    if ". " in question_text:
        question_text = question_text.split(". ", 1)[1]
    question_num_str = f"{current_index + 1:02d}"

    st.markdown(
        f"""
        <div style="position:relative; padding:0.9rem 0 0.8rem 0; overflow:hidden; margin-bottom:0.8rem;">
            <div style="
                position:absolute; right:-0.5rem; top:-0.5rem;
                font-family:'Orbitron','Noto Sans KR',sans-serif;
                font-size:7rem; line-height:1;
                color:rgba(255,255,255,0.035);
                pointer-events:none; user-select:none;
            ">{question_num_str}</div>
            <div style="
                position:absolute; left:0; top:0; bottom:0;
                width:2px;
                background:linear-gradient(180deg,#E8002D 0%,rgba(232,0,45,0.1) 100%);
            "></div>
            <div style="padding-left:1.2rem; position:relative; z-index:1;">
                <p style="
                    font-family:'Orbitron','Noto Sans KR',sans-serif;
                    font-size:0.65rem; font-weight:700;
                    letter-spacing:2.5px; text-transform:uppercase;
                    color:rgba(255,255,255,0.3); margin:0 0 0.35rem 0;
                ">Q{question_num_str} &nbsp;/&nbsp; {total_questions:02d}</p>
                <h3 style="
                    font-family:'Orbitron','Noto Sans KR',sans-serif;
                    font-size:1.25rem; font-weight:700;
                    color:#ffffff; margin:0;
                    line-height:1.2; letter-spacing:0.5px;
                ">{question_text}</h3>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    existing_answer = st.session_state.answers.get(current_question["id"])

    st.markdown(
        """
        <style>
        [class*="st-key-option_btn_"] { margin-bottom: 5px; }
        [class*="st-key-option_btn_"] button {
            width: 100%;
            text-align: left;
            padding: 0.6rem 1.1rem;
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.09);
            border-radius: 0;
            color: rgba(255,255,255,0.62);
            font-family: 'Orbitron', 'Noto Sans KR', system-ui, sans-serif;
            font-size: 0.88rem;
            font-weight: 500;
            white-space: normal;
            height: auto;
            min-height: 2.4rem;
            letter-spacing: 0.02em;
            transform: none !important;
            transition: background 0.15s, border-color 0.15s, color 0.15s !important;
        }
        [class*="st-key-option_btn_"] button:active {
            transform: none !important;
        }
        [class*="st-key-option_btn_"] button:hover {
            background: rgba(255,255,255,0.075) !important;
            border-color: rgba(255,255,255,0.22) !important;
            color: #ffffff !important;
            transform: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    for i, option in enumerate(current_question["options"]):
        is_selected = existing_answer == i
        btn_key = f"option_btn_{current_question['id']}_{i}"
        if is_selected:
            st.markdown(
                f"""
                <style>
                .st-key-{btn_key} button {{
                    background: rgba(232,0,45,0.28) !important;
                    border: 1px solid rgba(232,0,45,0.8) !important;
                    border-left: 3px solid #E8002D !important;
                    color: #ffffff !important;
                    box-shadow: inset 0 0 18px rgba(232,0,45,0.18), 0 0 10px rgba(232,0,45,0.35) !important;
                    text-shadow: 0 0 8px rgba(255,80,100,0.5) !important;
                }}
                .st-key-{btn_key} button:active {{
                    transform: none !important;
                }}
                </style>
                """,
                unsafe_allow_html=True,
            )
        if st.button(option["label"], key=btn_key, use_container_width=True):
            st.session_state.answers[current_question["id"]] = i
            is_last_question = current_index == total_questions - 1
            if is_last_question:
                st.session_state.result_top3 = calculate_top3(drivers, questions, st.session_state.answers)
                st.session_state.quiz_completed = True
            else:
                st.session_state.current_question_index += 1
            st.rerun()


def render_result_screen(drivers) -> None:
    driver_map = get_driver_map(drivers)
    top3 = st.session_state.result_top3
    if len(top3) < 3:
        st.error("결과 데이터를 불러오지 못했습니다. 퀴즈를 다시 진행해 주세요.")
        if st.button("다시하기", key="result_retry_fallback_btn", use_container_width=True):
            reset_quiz_state()
            st.rerun()
        return
    second_driver, first_driver, third_driver = top3[1], top3[0], top3[2]
    share_text = (
        f"나의 F1 드라이버 TOP 3: 1위 {top3[0]['name']}, "
        f"2위 {top3[1]['name']}, 3위 {top3[2]['name']}"
    )

    st.markdown(
        """
        <style>
        html, body {
            overflow: hidden !important;
            height: 100vh !important;
        }
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] > .main,
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"],
        [data-testid="stAppViewContainer"] > .main > .block-container {
            overflow: hidden !important;
            height: 100vh !important;
            max-height: 100vh !important;
        }
        [class*="st-key-result_retry_btn"] button {
            background-color: #E8002D !important;
            color: #ffffff !important;
            border: none !important;
            font-weight: 700 !important;
        }
        [class*="st-key-result_retry_btn"] button:hover {
            background-color: #bf001f !important;
        }
        [class*="st-key-result_share_btn"] button {
            background: rgba(0, 0, 0, 0.90) !important;
            color: #f5f7fb !important;
            border: 1px solid rgba(255, 255, 255, 0.20) !important;
        }
        [class*="st-key-result_share_btn"] button:hover {
            background: rgba(10, 10, 10, 0.78) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    header_left, header_right = st.columns([0.65, 0.35])
    with header_right:
        retry_col, share_col = st.columns(2)
        with retry_col:
            if st.button("다시하기", key="result_retry_btn", use_container_width=True):
                reset_quiz_state()
                st.rerun()
        with share_col:
            if st.button("공유하기", key="result_share_btn", use_container_width=True):
                st.session_state.show_share_text = not st.session_state.show_share_text

    if st.session_state.show_share_text:
        st.text_area("복사해서 공유할 결과 문구", share_text, height=90)
    first_driver_image = encode_image_to_base64(get_driver_profile_image_path(first_driver))
    second_driver_image = encode_image_to_base64(get_driver_profile_image_path(second_driver))
    third_driver_image = encode_image_to_base64(get_driver_profile_image_path(third_driver))

    podium_b64 = ""
    if PODIUM_IMAGE_PATH.exists():
        with open(PODIUM_IMAGE_PATH, "rb") as img_file:
            podium_b64 = base64.b64encode(img_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url('data:image/png;base64,{podium_b64}') no-repeat center center !important;
            background-size: cover !important;
        }}
        [data-testid="stAppViewContainer"] > .main > .block-container {{
            padding: 0 !important;
            max-width: 100% !important;
        }}
        .podium-wrapper {{
            position: relative;
            width: 100%;
            min-height: 85vh;
            margin-bottom: -64vh;
        }}
        .podium-card {{
            position: absolute;
            transform: translateX(-50%);
            text-align: center;
            background: rgba(15, 16, 20, 0.72);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 18px;
            padding: 0.9rem 0.9rem 0.7rem;
            backdrop-filter: blur(8px);
            color: #f5f7fb;
            min-width: 170px;
        }}
        .podium-card .p-name {{
            font-size: 0.98rem;
            font-weight: 700;
            margin-bottom: 0.18rem;
            white-space: nowrap;
        }}
        .podium-card .p-team {{
            font-size: 0.76rem;
            color: #ced3de;
            margin-bottom: 0.45rem;
            white-space: nowrap;
        }}
        [class*="st-key-profile_btn_"] {{
            position: relative;
            z-index: 30;
        }}
        [class*="st-key-profile_btn_"] button {{
            padding: 0;
            border: none;
            background: transparent !important;
            box-shadow: none !important;
            color: transparent !important;
        }}
        [class*="st-key-profile_btn_"] button:hover {{
            border: none;
            background: transparent !important;
            box-shadow: none !important;
        }}
        [class*="st-key-profile_btn_"] button:focus {{
            box-shadow: none !important;
            outline: none !important;
        }}
        [class*="st-key-profile_btn_"] button p {{
            font-size: 0 !important;
            line-height: 0 !important;
        }}
        .podium-image {{
            position: absolute;
            transform: translateX(-50%);
            z-index: 8;
            width: 160px;
            height: 240px;
            object-fit: contain;
            object-position: center bottom;
            pointer-events: none;
            transition: filter 0.3s ease;
        }}
        .podium-image.p-first {{
            left: 51%; top: -10%;
            filter:
                drop-shadow(0 0 3px rgba(255,215,0,1))
                drop-shadow(0 0 6px rgba(255,215,0,0.9));
        }}
        .podium-image.p-second {{
            left: 23%; top: 15%;
            filter:
                drop-shadow(0 0 3px rgba(210,220,240,1))
                drop-shadow(0 0 6px rgba(210,220,240,0.9));
        }}
        .podium-image.p-third {{
            left: 79%; top: 20%;
            filter:
                drop-shadow(0 0 3px rgba(220,140,60,1))
                drop-shadow(0 0 6px rgba(220,140,60,0.9));
        }}
        .podium-card.p-first  {{ left: 51%;  top: 33%; }}
        .podium-card.p-second {{ left: 23%;  top: 58%; }}
        .podium-card.p-third  {{ left: 79%;  top: 64%; }}
        </style>
        <div class="podium-wrapper">
            <img class="podium-image p-first" src="data:image/jpeg;base64,{first_driver_image}" alt="{first_driver['name']}" />
            <img class="podium-image p-second" src="data:image/jpeg;base64,{second_driver_image}" alt="{second_driver['name']}" />
            <img class="podium-image p-third" src="data:image/jpeg;base64,{third_driver_image}" alt="{third_driver['name']}" />
            <div class="podium-card p-first">
                <div class="p-name">{first_driver['name']}</div>
                <div class="p-team">{first_driver['team']}</div>
            </div>
            <div class="podium-card p-second">
                <div class="p-name">{second_driver['name']}</div>
                <div class="p-team">{second_driver['team']}</div>
            </div>
            <div class="podium-card p-third">
                <div class="p-name">{third_driver['name']}</div>
                <div class="p-team">{third_driver['team']}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    profile_cols = st.columns(3)
    button_layouts = [
        {
            "col": profile_cols[0],
            "driver": second_driver,
            "offset": "18vh",
            "left": "200px",
            "top": "-100px",
            "width": "180px",
            "height": "320px",
        },
        {
            "col": profile_cols[1],
            "driver": first_driver,
            "offset": "0vh",
            "left": "130px",
            "top": "-200px",
            "width": "180px",
            "height": "320px",
        },
        {
            "col": profile_cols[2],
            "driver": third_driver,
            "offset": "26vh",
            "left": "80px",
            "top": "-100px",
            "width": "180px",
            "height": "320px",
        },
    ]
    for layout in button_layouts:
        driver = layout["driver"]
        with layout["col"]:
            st.markdown(
                f"<div style='height: {layout['offset']}; margin-bottom: -100px;'></div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
                <style>
                .st-key-profile_btn_{driver['id']} {{
                    left: {layout['left']};
                    top: {layout['top']};
                }}
                .st-key-profile_btn_{driver['id']} button {{
                    width: {layout['width']};
                    height: {layout['height']};
                }}
                </style>
                """,
                unsafe_allow_html=True,
            )
            if st.button(
                "open profile",
                key=f"profile_btn_{driver['id']}",
                use_container_width=False,
            ):
                if HAS_DIALOG:
                    st.session_state.dialog_profile_driver = driver["id"]
                else:
                    st.session_state.selected_profile_driver = driver["id"]
                st.rerun()

    st.markdown("<div style='height: 54vh;'></div>", unsafe_allow_html=True)

    if HAS_DIALOG and st.session_state.dialog_profile_driver:
        selected_driver = driver_map[st.session_state.dialog_profile_driver]
        st.session_state.dialog_profile_driver = None
        show_profile_dialog(selected_driver)

    if not HAS_DIALOG and st.session_state.selected_profile_driver:
        selected_driver = driver_map[st.session_state.selected_profile_driver]
        st.write("")
        with st.container():
            st.markdown("### 프로필")
            render_profile_contents(selected_driver)
            if st.button("프로필 닫기", use_container_width=False):
                st.session_state.selected_profile_driver = None
                st.rerun()
