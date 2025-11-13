import React, {useEffect, useState} from "react";
import api from "../api";

export default function Dashboard(){
  const [data, setData] = useState(null);
  useEffect(()=>{
    api.get("/dashboard").then(r=>setData(r.data)).catch(()=>{});
  },[]);
  if(!data) return <div>Loading...</div>;
  return (
    <div style={{padding:20}}>
      <h2>Dashboard (IST)</h2>
      <div style={{display:"flex", gap:20}}>
        <div>Employees: {data.total_employees}</div>
        <div>Tasks: {data.total_tasks}</div>
        <div>Overdue: {data.overdue_tasks}</div>
        <div>Upcoming: {data.upcoming_deadlines}</div>
      </div>
      <p>Times are displayed in IST on the UI.</p>
    </div>
  )
}
