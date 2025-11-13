import React from "react";
import {Link} from "react-router-dom";
export default function Header(){
  return (
    <div style={{padding:10, borderBottom:"1px solid #ddd"}}>
      <Link to="/">Dashboard</Link> | <Link to="/tasks">Tasks</Link> | <Link to="/employees">Employees</Link> | <Link to="/uploads">Uploads</Link> | <Link to="/meetings">Meetings</Link> | <Link to="/profile">Profile</Link>
    </div>
  )
}
