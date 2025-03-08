from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import CORS_ORIGINS
from app.api.todos import router as todos_router
from app.database.mongodb import connect_to_mongo, close_mongo_connection

# FastAPI 앱 생성
app = FastAPI(title="Todo API", description="FastAPI와 MongoDB를 사용한 Todo API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(todos_router, prefix="/todos", tags=["todos"])

# 시작 이벤트
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

# 종료 이벤트
@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

# 루트 엔드포인트
@app.get("/")
async def root():
    return {"message": "Todo API에 오신 것을 환영합니다!"} 