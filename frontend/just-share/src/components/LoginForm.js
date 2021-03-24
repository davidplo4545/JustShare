import React, {useState, useContext} from 'react'
import { Link, useHistory, Redirect } from "react-router-dom";
import {userLogin} from '../api/AuthenticationAPI.js'
import {TokenContext} from '../hooks/TokenContext'

const LoginForm = () =>{
    const {token, setToken} = useContext(TokenContext)
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("")

    const handleSubmit = (event) => {
        event.preventDefault();

        userLogin({
            'email': email,
            'password': password
        }, setToken, setError);

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
            {error}
            <button type="submit" className="btn btn-primary btn-block">Login</button>
            <p className="forgot-password text-right">
                Not registered? <Link to="register">Register Here</Link>
            </p>
        </form>
    );
}

export default LoginForm;