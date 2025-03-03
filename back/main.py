from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv
from typing import List, Optional
from pydantic import BaseModel, Field
import uvicorn

# 환경 변수 로드
load_dotenv()

# FastAPI 앱 생성
app = FastAPI(title="Todo API", description="FastAPI와 MongoDB를 사용한 Todo API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포 환경에서는 특정 도메인으로 제한하세요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB 연결 설정
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "todo_app")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "todos")

# MongoDB 클라이언트
client = None
db = None
collection = None

# PyObjectId 클래스 정의
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("유효하지 않은 ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# Todo 모델 정의
class TodoModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    text: str
    completed: bool = False

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Todo 생성 모델
class TodoCreateModel(BaseModel):
    text: str
    completed: bool = False

# Todo 업데이트 모델
class TodoUpdateModel(BaseModel):
    text: Optional[str] = None
    completed: Optional[bool] = None

# 시작 이벤트
@app.on_event("startup")
async def startup_db_client():
    global client, db, collection
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

# 종료 이벤트
@app.on_event("shutdown")
async def shutdown_db_client():
    global client
    if client:
        client.close()

# 루트 엔드포인트
@app.get("/")
async def root():
    return {"message": "Todo API에 오신 것을 환영합니다!"}

# Todo 목록 조회
@app.get("/todos", response_model=List[TodoModel])
async def get_todos():
    todos = await collection.find().to_list(1000)
    return todos

# Todo 단일 조회
@app.get("/todos/{todo_id}", response_model=TodoModel)
async def get_todo(todo_id: str):
    if not ObjectId.is_valid(todo_id):
        raise HTTPException(status_code=400, detail="유효하지 않은 ID 형식입니다")
    
    todo = await collection.find_one({"_id": ObjectId(todo_id)})
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo를 찾을 수 없습니다")
    
    return todo

# Todo 생성
@app.post("/todos", response_model=TodoModel, status_code=201)
async def create_todo(todo: TodoCreateModel):
    new_todo = await collection.insert_one(todo.dict())
    created_todo = await collection.find_one({"_id": new_todo.inserted_id})
    return created_todo

# Todo 업데이트
@app.put("/todos/{todo_id}", response_model=TodoModel)
async def update_todo(todo_id: str, todo: TodoUpdateModel):
    if not ObjectId.is_valid(todo_id):
        raise HTTPException(status_code=400, detail="유효하지 않은 ID 형식입니다")
    
    # 빈 필드 제거
    update_data = {k: v for k, v in todo.dict().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="업데이트할 데이터가 없습니다")
    
    todo_exists = await collection.find_one({"_id": ObjectId(todo_id)})
    if todo_exists is None:
        raise HTTPException(status_code=404, detail="Todo를 찾을 수 없습니다")
    
    await collection.update_one({"_id": ObjectId(todo_id)}, {"$set": update_data})
    updated_todo = await collection.find_one({"_id": ObjectId(todo_id)})
    return updated_todo

# Todo 삭제
@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: str):
    if not ObjectId.is_valid(todo_id):
        raise HTTPException(status_code=400, detail="유효하지 않은 ID 형식입니다")
    
    todo_exists = await collection.find_one({"_id": ObjectId(todo_id)})
    if todo_exists is None:
        raise HTTPException(status_code=404, detail="Todo를 찾을 수 없습니다")
    
    await collection.delete_one({"_id": ObjectId(todo_id)})
    return None

# 메인 실행 부분
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 