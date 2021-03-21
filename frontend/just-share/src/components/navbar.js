import React from 'react';
import { Navbar, Nav, NavDropdown } from 'react-bootstrap';
import { Link } from "react-router-dom";
const NavbarMenu = (props) => {
    return (
        <Navbar bg="dark" variant="dark" expand="lg">
            <div className="navbar-center">
                <div className="collapsed-center">
                    <Navbar.Brand href="#home">JustShare</Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                </div>
                <Navbar.Collapse id="basic-navbar-nav"> 
                    {props.isLoggedIn ?
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
                    :
                        <Nav className="mr-auto">
                            <Nav.Link href="#">Home</Nav.Link>
                            <Nav.Link href="#">Profile</Nav.Link>
                            <Nav.Link href="#">My Items</Nav.Link>
                            <NavDropdown title="Dropdown" id="basic-nav-dropdown">
                                <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
                                <NavDropdown.Item href="#action/3.2">Another action</NavDropdown.Item>
                                <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
                                <NavDropdown.Divider />
                                <NavDropdown.Item href="#action/3.4">Separated link</NavDropdown.Item>
                            </NavDropdown>
                        </Nav>
                    }
                </Navbar.Collapse>
            </div>
        </Navbar>
    )
}

export default NavbarMenu;