import axios from 'axios';
import { useEffect, useState } from 'react';


async function performLogout(token) {
  try {
    if (token) {
      await axios.post(
        '/api/logout',
        {},
        {
          headers: {
            'Authorization': 'Token ' + token,
          },
        }
      );

      localStorage.removeItem('token');
    }
  } catch (error) {
    if (error.response) {
      console.error('Logout error:', error.response.data);
    } else {
      console.error('Logout error:', error.message);
    }
  }
}

function Logout() {
  const [loading, setLoading] = useState(true);
  const token = localStorage.getItem('token');

  useEffect(() => {
    const logout = async () => {
      if (token) {
        await performLogout(token);
        setLoading(false);
        window.location.href = "/"
      } else {
        setLoading(false);
        window.location.href = "/"      }
    };

    logout();
  }, [token]);

  return loading ? <p>Loading...</p> : null;
}

export default Logout;
