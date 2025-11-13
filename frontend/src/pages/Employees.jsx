import React, { useEffect, useState } from "react";
import api from "../api";

export default function Employees() {
  const [employees, setEmployees] = useState([]);

  useEffect(() => {
    api
      .get("/employees")
      .then((res) => setEmployees(res.data))
      .catch(() => {});
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h2>Employees</h2>
      <table border="1" cellPadding="8" style={{ marginTop: 15 }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>User ID</th>
            <th>Role</th>
            <th>Bio</th>
          </tr>
        </thead>

        <tbody>
          {employees.map((e) => (
            <tr key={e.id}>
              <td>{e.id}</td>
              <td>{e.user_id}</td>
              <td>{e.role}</td>
              <td>{e.bio}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
