@echo off
echo FastAPI 백엔드 서버 시작

REM 가상 환경 생성 (처음 실행 시)
if not exist venv (
    echo 가상 환경을 생성합니다...
    python -m venv venv
)

REM 가상 환경 활성화
call venv\Scripts\activate

REM 필요한 패키지 설치
echo 필요한 패키지를 설치합니다...
pip install -r requirements.txt

REM FastAPI 서버 실행
echo FastAPI 서버를 시작합니다...
uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause 