import React from 'react'
import RegistrationForm from '../components/RegistrationForm'
import '../components/register.css'
import {TokenContext} from '../hooks/TokenContext'
import useToken from '../hooks/useToken'
import { Redirect } from 'react-router'
const RegisterPage = (props) => {
  const {token, setToken} = useToken()

  if(token) return <Redirect to="/home" />;
  return (
    <div className="register-form">
      <RegistrationForm/>
    </div>
  )
}

export default RegisterPage
