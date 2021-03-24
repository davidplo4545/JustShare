import {useState} from 'react';

export default function useToken(){
    
    const getToken = () =>{
        return localStorage.getItem('Token')
    };
    const [token, setToken] = useState(getToken());

    const saveToken = token => {
        if (token == null) localStorage.removeItem('Token')
        else {
            localStorage.setItem('Token', token);
        }
        setToken(token);
      };

    return {
        setToken: saveToken,
        token
      }
}