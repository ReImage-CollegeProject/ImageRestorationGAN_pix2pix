import './login.css'
import { useState } from "react";
import axios from 'axios';

function SignUp(){
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [email, setEmail] = useState("");
    const [registrationStatus, setRegistrationStatus] = useState('');
    const [error, setError] = useState([]);

  const isUserLoggedIn = !!localStorage.getItem('token');

  if (isUserLoggedIn) {
    window.location.href = "/"
    return null;
  }

    async function handleRegister() {
       const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];
    try {
      const response = await axios.post("/api/register", {
        'email':email,
        'username': username,
        'password': password
      }, {
        headers: {
          'X-CSRFToken': csrfToken,
        }
      });
      setRegistrationStatus("registered")
      window.location.href = "/login"
    } catch (error) {
      console.log(error)
      if(error.response){
        if (error.response.data.email || error.response.data.password){
          setError([error.response.data.email,error.response.data.password])
        }
      }
    }
      }
    return(
        <div id='login-main'>
            <h2>SignUp</h2>
        <div className='login-div'>
                <input type="email" placeholder='email' name='email'
                onChange={(e) => setEmail(e.target.value)}/>
                <input type="username"  placeholder='username' name='username'
                onChange={(e) => setUsername(e.target.value)}/>
                <input type="password" placeholder='password' name='password'
                onChange={(e) => setPassword(e.target.value)}/>
                <button onClick={handleRegister}>SignUp</button>
            {registrationStatus && <p style={{ color: 'green' }}>{registrationStatus}</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
        </div>
        

    );

}
export default SignUp