import axios from 'axios'

const domain = "http://127.0.0.1:8000/api"
export const userLogin = (userCredentials, setToken, setError) => {
    axios.post(domain + '/login/',{
        'email':userCredentials['email'],
        'password':userCredentials['password'],
    })
    .then((res) => {
        setToken(res['data']['token']);
    })
    .catch((error) =>
    {
        setError("Username or password are incorrect.")
    })
    
}
export const userRegister = (userCredentials, setToken, setError) => {
    axios.post(domain + '/register/',{
        'email':userCredentials['email'],
        'password':userCredentials['password'],
        'profile':{
            'first_name':userCredentials['profile.first_name'],
            'last_name':userCredentials['profile.last_name'],
        }
    })
    .then((res) => 
    {
        setToken(res['data']['token']);
    })
    .catch((error) =>
    {
        setError("User with this email already exists.")
    })
}

export const userLogout = (userToken, setToken) => {
    axios.get(domain + '/logout/',{
        headers:{
            'Authorization': `token ${userToken}`
        }
    
    })
    .then((res) => 
    {
        setToken(null);
    })
}

export const getFriendInvites = (userToken) =>{
 axios.get(domain +``)
}

// Should replace /users endpoint with /people ?
export const getFriendRecommendations = async (userToken, setFriends) =>{
    await axios.get(domain + '/users',{
        headers:{
            'Authorization': `token ${userToken}`
        }
    })
    .then((res) =>{
        setFriends(res.data);
    })
}

export const sendFriendRequest = (userToken, friendId) =>{
    axios.post(domain + `/users/${friendId}/friends/`, {
        headers:{
            'Authorization': `token ${userToken}`
        }
    })
    .then((res) => console.log(res))
}

export const acceptFriendRequest = (userToken, friendId) =>{
    axios.post(domain + `/users/${friendId}/friends/`, {
        headers:{
            'Authorization': `token ${userToken}`
        }
    })
    .then((res) => console.log(res))
}

export const deleteFriendRequest = (userToken, friendId) =>{
    axios.delete(domain + `/users/${friendId}/friends/`, {
        headers:{
            'Authorization': `token ${userToken}`
        }
    })
    .then((res) => console.log(res))
}