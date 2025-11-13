import React, {useState} from "react";
import api from "../api";
import {useNavigate} from "react-router-dom";

export default function Login(){
  const [username, setUsername] = useState("");
  const [password, setPassword]= useState("");
  const nav = useNavigate();
  const submit = async (e) => {
    e.preventDefault();
    try{
      const res = await api.post("/auth/login", {username, password});
      localStorage.setItem("token", res.data.access_token);
      nav("/");
    }catch(err){
      alert("Login failed");
    }
  }
  return (
    <div style={{padding:20}}>
      <h2>Login</h2>
      <form onSubmit={submit}>
        <input placeholder="username or email" value={username} onChange={e=>setUsername(e.target.value)} /><br/>
        <input type="password" placeholder="password" value={password} onChange={e=>setPassword(e.target.value)} /><br/>
        <button>Login</button>
      </form>
    </div>
  )
}
