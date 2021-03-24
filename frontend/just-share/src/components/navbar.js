import React, {useContext} from 'react';
import { Navbar, Nav, NavDropdown } from 'react-bootstrap';
import { Link, Redirect } from "react-router-dom";
import {TokenContext} from '../hooks/TokenContext'
import {userLogout} from '../api/AuthenticationAPI.js'
const NavbarMenu = () => {
    const {token, setToken} = useContext(TokenContext)

    const onLogout = () => {
        userLogout(token, setToken)
        return <Redirect to="/home" />;
    }
    return (
        <Navbar bg="dark"  variant="dark" expand="lg">
            <div className="navbar-center">
                <div className="collapsed-center">
                    <Navbar.Brand href="#home">JustShare</Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                </div>
                
                    {token == null ?
                        <Navbar.Collapse id="basic-navbar-nav"> 
                            <Nav className="mr-auto">
                                <Nav.Link as={Link} to='/'>Home</Nav.Link>
                                <Nav.Link as={Link} to='register'>Register</Nav.Link>
                                <Nav.Link as={Link} to='login'>Login</Nav.Link>
                                <NavDropdown title="Dropdown" id="basic-nav-dropdown">
                                    <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
                                    <NavDropdown.Item href="#action/3.2">Another action</NavDropdown.Item>
                                    <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
                                    <NavDropdown.Divider />
                                    <NavDropdown.Item href="#action/3.4">Separated link</NavDropdown.Item>
                                </NavDropdown>
                            </Nav>
                        </Navbar.Collapse>
                    :
                        <Navbar.Collapse id="basic-navbar-nav"> 
                            <Nav className="mr-auto">
                                <Nav.Link as={Link} to='/'>Home</Nav.Link>
                                <Nav.Link as={Link} to='profile'>Profile</Nav.Link>
                                <NavDropdown title="My Profile" id="basic-nav-dropdown">
                                    <NavDropdown.Item href="#action/3.1">Photos</NavDropdown.Item>
                                    <NavDropdown.Item href="friends">Friends</NavDropdown.Item>
                                    <NavDropdown.Item href="#action/3.3">Collections</NavDropdown.Item>
                                    <NavDropdown.Divider />
                                    <NavDropdown.Item href="#action/3.4">Separated link</NavDropdown.Item>
                                </NavDropdown>
                                
                            </Nav>
                            <Nav>
                                <Nav.Link onClick={onLogout}>Logout</Nav.Link>
                            </Nav>
                        </Navbar.Collapse>
                    }
                
            </div>
        </Navbar>
    )
}

export default NavbarMenu;