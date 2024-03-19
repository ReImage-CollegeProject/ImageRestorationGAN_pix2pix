import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { Link } from 'react-router-dom'; 
import './nav.css'
import { useState, useEffect } from 'react';

function NavBar() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [auth, setAuth] = useState(null);

  useEffect(() => {
    if (!token) {
      setAuth(
        <div>
        <Button variant="outline-success" as={Link} to="/login" className='btns'>
            Login
          </Button>
          <Button variant="outline-success"
            as={Link} to="/signup" className='btns'>SignUp
          </Button>
        </div>
      );
    } else {
      setAuth(
        <Button variant="outline-success"
            as={Link} to="/logout">Logout
          </Button>
      );
    }
  }, [token]);
  return (
    <Navbar expand="lg" className="nav">
      <Container className='justify-content-center'>
        <Navbar.Brand href="/" style={{color:"white", marginRight:150}}>ReImage</Navbar.Brand>
        <Navbar.Toggle aria-controls="navbarScroll" />
        <Navbar.Collapse id="navbarScroll">
          <Nav
            className="me-auto my-2 my-lg-0"
            style={{ maxHeight: '100px' }}
            navbarScroll
          >
            <Nav.Link as={Link} to="/uploads" className='navs'>Upload</Nav.Link>
            <Nav.Link as={Link} to="/images" className='navs'>Images</Nav.Link>
          </Nav>
          {auth}
        </Navbar.Collapse>
        <div className='pseudoElementStyle' ></div>
      </Container>
    </Navbar>
  );
}

export default NavBar;