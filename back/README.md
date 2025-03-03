# Todo API 백엔드

FastAPI와 MongoDB를 사용한 Todo API 백엔드 서버입니다.

## 요구 사항

- Python 3.7 이상
- MongoDB (로컬 또는 원격)

## 설치 및 실행

### 1. MongoDB 설치 및 실행

MongoDB가 설치되어 있지 않다면 [MongoDB 공식 사이트](https://www.mongodb.com/try/download/community)에서 다운로드하여 설치하세요.

MongoDB를 실행합니다:

```
mongod
```

### 2. 환경 설정

`.env` 파일에서 MongoDB 연결 정보를 설정할 수 있습니다:

```
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=todo_app
COLLECTION_NAME=todos
```

### 3. 서버 실행

#### Linux/Mac:

```
chmod +x run.sh
./run.sh
```

#### Windows:

```
run.bat
```

또는 직접 실행:

```
# 가상 환경 생성
python -m venv venv

# 가상 환경 활성화
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt

# 서버 실행
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API 엔드포인트

서버가 실행되면 다음 URL에서 API 문서를 확인할 수 있습니다:

```
http://localhost:8000/docs
```

### 주요 엔드포인트

- `GET /todos`: 모든 할 일 목록 조회
- `GET /todos/{todo_id}`: 특정 할 일 조회
- `POST /todos`: 새로운 할 일 생성
- `PUT /todos/{todo_id}`: 할 일 업데이트
- `DELETE /todos/{todo_id}`: 할 일 삭제

## 프론트엔드 연동

프론트엔드 애플리케이션에서 다음 URL로 API를 호출할 수 있습니다:

```
http://localhost:8000
```
