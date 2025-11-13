import React from "react";
import {
  LineChart, Line,
  BarChart, Bar,
  PieChart, Pie, Cell,
  XAxis, YAxis, Tooltip, Legend,
  ResponsiveContainer
} from "recharts";

export function TasksLineChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={260}>
      <LineChart data={data}>
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="tasks_completed" stroke="#82ca9d" />
      </LineChart>
    </ResponsiveContainer>
  );
}

export function EmployeeBarChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={260}>
      <BarChart data={data}>
        <XAxis dataKey="employee_id" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="tasks_completed" fill="#8884d8" />
        <Bar dataKey="on_time" fill="#82ca9d" />
      </BarChart>
    </ResponsiveContainer>
  );
}

export function StatusPieChart({ data }) {
  const COLORS = ["#0088FE", "#FF8042", "#00C49F"];

  return (
    <ResponsiveContainer width="100%" height={260}>
      <PieChart>
        <Pie
          data={data}
          dataKey="value"
          nameKey="name"
          outerRadius={100}
          label
        >
          {data.map((_, i) => (
            <Cell key={i} fill={COLORS[i % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
      </PieChart>
    </ResponsiveContainer>
  );
}
