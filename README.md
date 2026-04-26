# F1 드라이버 매칭 퀴즈

이 프로젝트는 **Streamlit 기반의 F1 드라이버 성향 매칭 퀴즈**입니다.  
사용자가 로그인한 뒤 8개의 객관식 질문에 답하면, 점수 계산 로직을 통해 사용자와 가장 잘 맞는 현역 F1 드라이버 TOP 3 결과를 보여줍니다.

아래 순서대로 실행하시면 됩니다.

## 실행 전 준비

Python: **Python 3.10 이상**이 설치되어 있으면 됩니다.

## 가상환경 생성 및 활성화

아래 명령어로 가상환경을 구축합니다.

**Mac / Linux 사용자:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows 사용자:**
```bash
python -m venv .venv
.\.venv\Scripts\activate  
```


## 필요한 패키지 설치

아래 명령어를 실행합니다.

```bash
pip install -r requirements.txt
```

설치되는 주요 패키지는 다음과 같습니다.

- `streamlit==1.44.1`


## 프로그램 실행

아래 명령어로 앱을 실행합니다.

```bash
streamlit run app.py
```

정상 실행되면 터미널에 로컬 주소가 출력됩니다.  

```text
http://localhost:8501
```

이 프로젝트는 로그인 후 퀴즈를 진행하도록 구현되어 있습니다.  
아래 계정으로 바로 테스트할 수 있습니다.

- 아이디: `ahran`
- 비밀번호: `1234`

## 5. 프로젝트 구조

- `app.py`: 메인 실행 파일
- `src/config.py`: 상수, 경로, 로그인 정보 관리
- `src/state.py`: 세션 상태 초기화 및 리셋
- `src/data.py`: JSON 데이터 로딩, 에셋 처리
- `src/logic.py`: 점수 계산 및 결과 산출
- `src/ui.py`: 로그인 화면, 퀴즈 화면, 결과 화면 렌더링
- `assets/`: 이미지 및 JSON 데이터 파일
- `requirements.txt`: 의존성 목록