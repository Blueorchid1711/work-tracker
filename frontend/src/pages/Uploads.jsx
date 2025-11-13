import React, { useEffect, useState } from "react";
import api from "../api";

export default function Uploads() {
  const [files, setFiles] = useState([]);

  useEffect(() => {
    api
      .get("/upload")
      .then((res) => setFiles(res.data))
      .catch((err) => console.log(err));
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h2>Uploads</h2>

      <table border="1" cellPadding="8" style={{ marginTop: 15 }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Filename</th>
            <th>Uploader</th>
            <th>Date</th>
          </tr>
        </thead>

        <tbody>
          {files.map((f) => (
            <tr key={f.id}>
              <td>{f.id}</td>
              <td>{f.filename}</td>
              <td>{f.uploader_user_id}</td>
              <td>{f.created_at}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
