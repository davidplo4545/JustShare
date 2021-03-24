import {useState, useEffect} from 'react';
import './App.css';
import NavbarMenu from './components/navbar.js';
import {Button} from 'react-bootstrap'
import { Route, Switch } from "react-router-dom";
import './components/navbar.css';
import LoginPage from './pages/Login.js'
import RegisterPage from './pages/Register.js'
import HomePage from './pages/Home'
import FriendsPage from './pages/Friends.js'
import ProfilePage from './pages/Profile.js'
import {TokenContext} from './hooks/TokenContext'
import useToken from './hooks/useToken.js'

function getToken(){
  return {'token':localStorage.getItem('token')}
}
function App() {
  const {token,setToken} = useToken();

  return (
    <div className="App">
      <TokenContext.Provider value={{token, setToken}}>
        <header className="App-header">
              <NavbarMenu token={token}/>
        </header>
        <main>
          <Switch>
            <Route exact path="/">
              <HomePage />
            </Route>
            <Route exact path="/register">
              <RegisterPage />
            </Route>
            <Route exact path="/login">
              <LoginPage/>
            </Route>
            <Route exact path="/profile">
              <ProfilePage/>
            </Route>
            <Route exact path="/friends">
              <FriendsPage/>
            </Route>
          </Switch> 
        </main>
        <footer className="footer">Footer</footer>
      </TokenContext.Provider>
    </div>
  );
}

export default App;
