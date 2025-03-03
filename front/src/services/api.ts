import axios from "axios";
import { Task } from "../types/Task";

const API_URL = "http://localhost:8000";

// API 클라이언트 생성
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Todo 목록 조회
export const fetchTodos = async (): Promise<Task[]> => {
  try {
    const response = await apiClient.get("/todos");
    // MongoDB의 _id를 id로 변환
    return response.data.map((todo: any) => ({
      id: todo._id,
      text: todo.text,
      completed: todo.completed,
    }));
  } catch (error) {
    console.error("할 일 목록을 가져오는 중 오류 발생:", error);
    throw error;
  }
};

// Todo 생성
export const createTodo = async (text: string): Promise<Task> => {
  try {
    const response = await apiClient.post("/todos", { text, completed: false });
    return {
      id: response.data._id,
      text: response.data.text,
      completed: response.data.completed,
    };
  } catch (error) {
    console.error("할 일을 생성하는 중 오류 발생:", error);
    throw error;
  }
};

// Todo 업데이트
export const updateTodo = async (
  id: string,
  updates: Partial<Task>
): Promise<Task> => {
  try {
    const response = await apiClient.put(`/todos/${id}`, updates);
    return {
      id: response.data._id,
      text: response.data.text,
      completed: response.data.completed,
    };
  } catch (error) {
    console.error("할 일을 업데이트하는 중 오류 발생:", error);
    throw error;
  }
};

// Todo 삭제
export const deleteTodo = async (id: string): Promise<void> => {
  try {
    await apiClient.delete(`/todos/${id}`);
  } catch (error) {
    console.error("할 일을 삭제하는 중 오류 발생:", error);
    throw error;
  }
};
