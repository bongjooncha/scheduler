import React from "react";
import "./TaskItem.css";
import { Task } from "../../types/Task";

interface TaskItemProps {
  task: Task;
  onToggle: (id: number) => void;
  onDelete: (id: number) => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onToggle, onDelete }) => {
  return (
    <div className={`task-item ${task.completed ? "completed" : ""}`}>
      <input
        type="checkbox"
        checked={task.completed}
        onChange={() => onToggle(task.id)}
      />
      <span className="task-text">{task.text}</span>
      <button onClick={() => onDelete(task.id)} className="delete-btn">
        삭제
      </button>
    </div>
  );
};

export default TaskItem;
