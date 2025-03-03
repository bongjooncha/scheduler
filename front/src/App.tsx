import React from "react";
import "./App.css";
import TaskPage from "./pages/TaskPage/TaskPage";

const App: React.FC = () => {
  return (
    <div className="App">
      <header className="App-header">
        <TaskPage />
      </header>
    </div>
  );
};

export default App;
