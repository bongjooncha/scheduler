import React from "react";
import "./TaskList.css";
import { Task } from "../../types/Task";
import TaskItem from "../TaskItem/TaskItem";

interface TaskListProps {
  tasks: Task[];
  onToggleTask: (id: number) => void;
  onDeleteTask: (id: number) => void;
}

const TaskList: React.FC<TaskListProps> = ({
  tasks,
  onToggleTask,
  onDeleteTask,
}) => {
  return (
    <div className="task-list">
      {tasks.length === 0 ? (
        <p className="no-tasks">
          할 일이 없습니다. 새로운 할 일을 추가해보세요!
        </p>
      ) : (
        tasks.map((task) => (
          <TaskItem
            key={task.id}
            task={task}
            onToggle={onToggleTask}
            onDelete={onDeleteTask}
          />
        ))
      )}
    </div>
  );
};

export default TaskList;
