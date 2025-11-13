import React from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Tasks from "./pages/Tasks";
import Employees from "./pages/Employees";
import Uploads from "./pages/Uploads";
import Meetings from "./pages/Meetings";
import Profile from "./pages/Profile";
import Header from "./components/Header";
import "./index.css";

function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/login" element={<Login />} />
        <Route path="/tasks" element={<Tasks />} />
        <Route path="/employees" element={<Employees />} />
        <Route path="/uploads" element={<Uploads />} />
        <Route path="/meetings" element={<Meetings />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
    </BrowserRouter>
  );
}

createRoot(document.getElementById("root")).render(<App />);
