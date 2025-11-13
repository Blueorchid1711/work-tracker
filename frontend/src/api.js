import axios from "axios";
const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000/api";

const getToken = () => localStorage.getItem("token");

const api = axios.create({
  baseURL: API_BASE,
});

api.interceptors.request.use((c) => {
  const t = getToken();
  if (t) c.headers.Authorization = `Bearer ${t}`;
  return c;
});

export default api;
