import React, { useState, useEffect } from "react";
import "./TaskPage.css";
import Header from "../../components/Header/Header";
import TaskInput from "../../components/TaskInput/TaskInput";
import TaskList from "../../components/TaskList/TaskList";
import { Task } from "../../types/Task";
import {
  fetchTodos,
  createTodo,
  updateTodo,
  deleteTodo,
} from "../../services/api";

const TaskPage: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // 할 일 목록 불러오기
  useEffect(() => {
    const loadTasks = async () => {
      try {
        setLoading(true);
        const data = await fetchTodos();
        setTasks(data);
        setError(null);
      } catch (err) {
        console.error("할 일 목록을 불러오는 중 오류 발생:", err);
        setError("할 일 목록을 불러오는 중 오류가 발생했습니다.");
      } finally {
        setLoading(false);
      }
    };

    loadTasks();
  }, []);

  // 할 일 추가
  const addTask = async (text: string): Promise<void> => {
    try {
      const newTask = await createTodo(text);
      setTasks([...tasks, newTask]);
    } catch (err) {
      console.error("할 일을 추가하는 중 오류 발생:", err);
      setError("할 일을 추가하는 중 오류가 발생했습니다.");
    }
  };

  // 할 일 토글
  const toggleTask = async (id: number): Promise<void> => {
    try {
      const task = tasks.find((t) => t.id === id);
      if (!task) return;

      const updatedTask = await updateTodo(String(id), {
        completed: !task.completed,
      });
      setTasks(
        tasks.map((task) =>
          task.id === id ? { ...task, completed: updatedTask.completed } : task
        )
      );
    } catch (err) {
      console.error("할 일 상태를 변경하는 중 오류 발생:", err);
      setError("할 일 상태를 변경하는 중 오류가 발생했습니다.");
    }
  };

  // 할 일 삭제
  const deleteTask = async (id: number): Promise<void> => {
    try {
      await deleteTodo(String(id));
      setTasks(tasks.filter((task) => task.id !== id));
    } catch (err) {
      console.error("할 일을 삭제하는 중 오류 발생:", err);
      setError("할 일을 삭제하는 중 오류가 발생했습니다.");
    }
  };

  return (
    <div className="task-page">
      <Header title="스케줄러" />
      {error && <div className="error-message">{error}</div>}
      <TaskInput onAddTask={addTask} />
      {loading ? (
        <div className="loading">로딩 중...</div>
      ) : (
        <TaskList
          tasks={tasks}
          onToggleTask={toggleTask}
          onDeleteTask={deleteTask}
        />
      )}
    </div>
  );
};

export default TaskPage;
