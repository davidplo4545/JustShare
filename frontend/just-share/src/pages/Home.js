import React, {useContext} from 'react'
import {UserContext} from '../hooks/UserContext'
const HomePage = () => {
  const user = useContext(UserContext)
  return (
    <div>
      <h1>Home</h1>
      <div>{user.token}</div>
    </div>
  )
}

export default HomePage
