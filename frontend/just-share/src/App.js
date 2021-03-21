import {useState} from 'react';
import './App.css';
import NavbarMenu from './components/navbar.js';
import {Button} from 'react-bootstrap'
import { Route, Switch } from "react-router-dom";
import './components/navbar.css';
import LoginPage from './pages/Login.js'
import RegisterPage from './pages/Register.js'
import HomePage from './pages/Home'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(true)

  const setLogin = () => {
    setIsLoggedIn(!isLoggedIn)
    console.log(isLoggedIn);
  };

  return (
    <div className="App">
      <header className="App-header">
            <NavbarMenu isLoggedIn={isLoggedIn}/>
      </header>
      {/* <Button onClick={setLogin} variant="primary">Login</Button>{' '} */}
      <main>
        <Switch>
          <Route exact path="/">
            <HomePage />
          </Route>
          <Route exact path="/register">
            <RegisterPage />
          </Route>
          <Route exact path="/login">
            <LoginPage />
          </Route>
        </Switch> 
      </main>
      <footer className="footer">Footer</footer>
    </div>
  );
}

export default App;
