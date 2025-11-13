import React, { useEffect, useState } from "react";
import api from "../api";

export default function Profile() {
  const [me, setMe] = useState(null);

  useEffect(() => {
    api
      .get("/users/me")
      .then((res) => setMe(res.data))
      .catch((err) => console.log(err));
  }, []);

  if (!me) return <div style={{ padding: 20 }}>Loading...</div>;

  return (
    <div style={{ padding: 20 }}>
      <h2>My Profile</h2>

      <p><strong>Username:</strong> {me.username}</p>
      <p><strong>Email:</strong> {me.email}</p>
      <p><strong>Full Name:</strong> {me.full_name}</p>
      <p><strong>Role:</strong> {me.role}</p>
    </div>
  );
}
