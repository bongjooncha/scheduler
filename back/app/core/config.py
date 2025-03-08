import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# MongoDB 설정
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "todo_app")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "todos")

# CORS 설정
CORS_ORIGINS = ["*"]  # 실제 배포 환경에서는 특정 도메인으로 제한하세요 