import React, { useState } from "react";
import "./TaskInput.css";

interface TaskInputProps {
  onAddTask: (text: string) => void;
}

const TaskInput: React.FC<TaskInputProps> = ({ onAddTask }) => {
  const [newTask, setNewTask] = useState<string>("");

  const handleAddTask = (): void => {
    if (newTask.trim() !== "") {
      onAddTask(newTask);
      setNewTask("");
    }
  };

  return (
    <div className="task-input">
      <input
        type="text"
        value={newTask}
        onChange={(e) => setNewTask(e.target.value)}
        placeholder="할 일을 입력하세요"
        onKeyPress={(e) => e.key === "Enter" && handleAddTask()}
      />
      <button onClick={handleAddTask}>추가</button>
    </div>
  );
};

export default TaskInput;
