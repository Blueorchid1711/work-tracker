import React, {useEffect, useState} from "react";
import api from "../api";

export default function Tasks(){
  const [tasks, setTasks] = useState([]);
  useEffect(()=>{ api.get("/tasks").then(r=>setTasks(r.data)); },[]);
  return (
    <div style={{padding:20}}>
      <h2>Tasks</h2>
      <table border="1"><thead><tr><th>ID</th><th>Title</th><th>Status</th><th>Due (UTC)</th></tr></thead>
      <tbody>
        {tasks.map(t=>(
          <tr key={t.id}><td>{t.id}</td><td>{t.title}</td><td>{t.status}</td><td>{t.due_date}</td></tr>
        ))}
      </tbody></table>
    </div>
  )
}
