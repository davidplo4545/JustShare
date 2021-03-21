import React, {useState} from 'react'
import { Link } from "react-router-dom";
import {userLogin} from '../api/AuthenticationAPI.js'

const LoginForm = () =>{

    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")


    const handleSubmit = (event) => {
        event.preventDefault();
        
        const userData = {
            'email': email,
            'password': password,
        }

        userLogin(userData);

    }

    return(
        <form onSubmit={handleSubmit}>
        
            <h3>Login</h3>

            <div className="form-group">
                <label>Email address</label>
                <input required type="email" className="form-control" value={email} onChange={(e) => setEmail(e.target.value)} name="email" placeholder="Enter email" />
            </div>

            <div className="form-group">
                <label>Password</label>
                <input required type="password" className="form-control" name="password" value={password} onChange={(e) => setPassword(e.target.value)}  placeholder="Enter password" />
            </div>

            <button type="submit" className="btn btn-primary btn-block">Login</button>
            <p className="forgot-password text-right">
                Not registered? <Link to="register">Register Here</Link>
            </p>
        </form>
    );
}

export default LoginForm;