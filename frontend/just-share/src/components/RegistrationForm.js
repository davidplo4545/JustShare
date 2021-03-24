import React, {useState, useContext} from 'react'
import { Link } from "react-router-dom";
import {userRegister} from '../api/AuthenticationAPI.js'
import {TokenContext} from '../hooks/TokenContext'

const RegistrationForm = () =>{

    const [email, setEmail] = useState("")
    const [firstName, setFirstName] = useState("")
    const [lastName, setLastName] = useState("")
    const [password, setPassword] = useState("")
    const {token, setToken} = useContext(TokenContext)
    const [error, setError] = useState("")


    const handleSubmit = (event) => {
        event.preventDefault();
        
        userRegister({
            'email': email,
            'password': password,
            'profile.first_name': firstName,
            'profile.last_name': lastName,
        }, setToken, setError);

    }


    return(
        <form onSubmit={handleSubmit}>
        
            <h3>Sign Up</h3>

            <div className="form-group">
                <label>Email address</label>
                <input required type="email" className="form-control" name="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="Enter email" />
            </div>

            <div className="form-group">
                <label>First Name</label>
                <input required type="text" className="form-control" name="password" value={firstName} onChange={e => setFirstName(e.target.value)} placeholder="Enter First Name" />
            </div>

            <div className="form-group">
                <label>Last Name</label>
                <input required type="text" className="form-control" name="password" placeholder="Enter Last Name" value={lastName} onChange={e => setLastName(e.target.value)}/>
            </div>


            <div className="form-group">
                <label>Password</label>
                <input required type="password" className="form-control" name="password" placeholder="Enter password" value={password} onChange={e => setPassword(e.target.value)}/>
            </div>
            {error}
            <button type="submit" className="btn btn-primary btn-block">Sign Up</button>
            <p className="forgot-password text-right">
                Already registered <Link to="login">sign in?</Link>
            </p>
        </form>
    );
}

export default RegistrationForm;