import React, {useContext} from 'react'
import RegistrationForm from '../components/RegistrationForm'
import '../components/register.css'
import {UserContext} from '../hooks/UserContext'
import useToken from '../hooks/useToken'
import { Redirect } from 'react-router'
const RegisterPage = (props) => {
  const {token, setToken} = useToken()
  const user = useContext(UserContext)

  if(token) return <Redirect to="/home" />;
  return (
    <div className="register-form">
      <RegistrationForm/>
    </div>
  )
}

export default RegisterPage
