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
import {UserContext} from './hooks/UserContext'
import useToken from './hooks/useToken.js'

function getToken(){
  return {'token':localStorage.getItem('token')}
}
function App() {
  const {token,setToken} = useToken();
  const {user, setUser} = useState({})

  return (
    <div className="App">
      <UserContext.Provider value={{token, user, setToken, setUser}}>
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
        {/* <footer className="footer">Footer</footer> */}
      </UserContext.Provider>
    </div>
  );
}

export default App;
