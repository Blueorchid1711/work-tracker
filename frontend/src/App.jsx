import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import PrivateRoute from "./components/PrivateRoute";
import Header from "./components/Header";

import Dashboard from "./pages/Dashboard";
import Tasks from "./pages/Tasks";
import Employees from "./pages/Employees";
import Uploads from "./pages/Uploads";
import Meetings from "./pages/Meetings";
import Profile from "./pages/Profile";
import Login from "./pages/Login";

export default function App() {
  return (
    <BrowserRouter>
      <Header />

      <Routes>
        <Route path="/login" element={<Login />} />

        <Route
          path="/"
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          }
        />

        <Route
          path="/tasks"
          element={
            <PrivateRoute>
              <Tasks />
            </PrivateRoute>
          }
        />

        <Route
          path="/employees"
          element={
            <PrivateRoute>
              <Employees />
            </PrivateRoute>
          }
        />

        <Route
          path="/uploads"
          element={
            <PrivateRoute>
              <Uploads />
            </PrivateRoute>
          }
        />

        <Route
          path="/meetings"
          element={
            <PrivateRoute>
              <Meetings />
            </PrivateRoute>
          }
        />

        <Route
          path="/profile"
          element={
            <PrivateRoute>
              <Profile />
            </PrivateRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
