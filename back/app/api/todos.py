from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from ..models.todo import TodoModel, TodoCreateModel, TodoUpdateModel
from ..database.mongodb import collection

router = APIRouter()

@router.get("/", response_model=List[TodoModel])
async def get_todos():
    todos = await collection.find().to_list(1000)
    return todos

@router.get("/{todo_id}", response_model=TodoModel)
async def get_todo(todo_id: str):
    if not ObjectId.is_valid(todo_id):
        raise HTTPException(status_code=400, detail="유효하지 않은 ID 형식입니다")
    
    todo = await collection.find_one({"_id": ObjectId(todo_id)})
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo를 찾을 수 없습니다")
    
    return todo

@router.post("/", response_model=TodoModel, status_code=201)
async def create_todo(todo: TodoCreateModel):
    new_todo = await collection.insert_one(todo.dict())
    created_todo = await collection.find_one({"_id": new_todo.inserted_id})
    return created_todo

@router.put("/{todo_id}", response_model=TodoModel)
async def update_todo(todo_id: str, todo: TodoUpdateModel):
    if not ObjectId.is_valid(todo_id):
        raise HTTPException(status_code=400, detail="유효하지 않은 ID 형식입니다")
    
    update_data = {k: v for k, v in todo.dict().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="업데이트할 데이터가 없습니다")
    
    todo_exists = await collection.find_one({"_id": ObjectId(todo_id)})
    if todo_exists is None:
        raise HTTPException(status_code=404, detail="Todo를 찾을 수 없습니다")
    
    await collection.update_one({"_id": ObjectId(todo_id)}, {"$set": update_data})
    updated_todo = await collection.find_one({"_id": ObjectId(todo_id)})
    return updated_todo

@router.delete("/{todo_id}", status_code=204)
async def delete_todo(todo_id: str):
    if not ObjectId.is_valid(todo_id):
        raise HTTPException(status_code=400, detail="유효하지 않은 ID 형식입니다")
    
    todo_exists = await collection.find_one({"_id": ObjectId(todo_id)})
    if todo_exists is None:
        raise HTTPException(status_code=404, detail="Todo를 찾을 수 없습니다")
    
    await collection.delete_one({"_id": ObjectId(todo_id)})
    return None 