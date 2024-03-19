import "./login.css";
import { useState } from "react";
import axios from 'axios';

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const isUserLoggedIn = !!localStorage.getItem('token');

  if (isUserLoggedIn) {
    window.location.href = "/"    
    return null;
  }
  async function handleLogin() {
    const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];
    try {
      const response = await axios.post("/api/login", {
        'username': username,
        'password': password
      }, {
        headers: {
          'X-CSRFToken': csrfToken,
        }
      });
      localStorage.setItem('token', response.data.token);
      console.log(response.data.token);
      window.location.href = "/"
      } catch (error) {
      setError("user"+error.response.data.detail+"Please enter valid details")
      
    }
  }
  return (
    <div id="login-main">
      <h2>Login</h2>
      <div className="login-div">
          <input
            type="username"
            placeholder="username"
            name="username"
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            placeholder="password"
            name="password"
            onChange={(e) => setPassword(e.target.value)}
          />
          <button onClick={handleLogin}>Login</button>
          {error && <p style={{ color: "red" }}>{error}</p>}
      </div>
    </div>
  );
  }
export default Login;
