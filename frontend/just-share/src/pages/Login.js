import React, {useState, useContext} from 'react'
import LoginForm from '../components/LoginForm'
import '../components/login.css'
import {UserContext} from '../hooks/UserContext'
import { Redirect } from 'react-router'

const LoginPage = (props) => {
  const {token, setToken} = useContext(UserContext)

  if(token) return <Redirect to="/home" />;

  return (
    <div className="login-form">
      <LoginForm/>
    </div>
  )
}

export default LoginPage
