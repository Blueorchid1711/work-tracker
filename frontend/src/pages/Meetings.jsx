import React, { useEffect, useState } from "react";
import api from "../api";

export default function Meetings() {
  const [meetings, setMeetings] = useState([]);

  useEffect(() => {
    api
      .get("/meetings")
      .then((res) => setMeetings(res.data))
      .catch((err) => console.log(err));
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h2>Meetings</h2>

      <table border="1" cellPadding="8" style={{ marginTop: 15 }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Start</th>
            <th>End</th>
            <th>Participants</th>
          </tr>
        </thead>

        <tbody>
          {meetings.map((m) => (
            <tr key={m.id}>
              <td>{m.id}</td>
              <td>{m.title}</td>
              <td>{m.start_datetime}</td>
              <td>{m.end_datetime}</td>
              <td>{(m.participants_employee_ids || []).join(", ")}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
