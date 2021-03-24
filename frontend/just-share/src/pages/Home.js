import React, {useContext} from 'react'
import {TokenContext} from '../hooks/TokenContext'
const HomePage = () => {
  const {token, setToken} = useContext(TokenContext)
  return (
    <div>
      <h1>Home</h1>
      <div>{token}</div>
    </div>
  )
}

export default HomePage
