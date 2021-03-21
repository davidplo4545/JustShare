import axios from 'axios'

const domain = "http://127.0.0.1:8000/api"
export const userLogin = (userCredentials) => {
    axios.post(domain + '/login/',{
        'email':userCredentials['email'],
        'password':userCredentials['password'],
    })
    .then((res) => console.log(res))
}
export const userRegister = (userCredentials) => {
    axios.post(domain + '/register/',{
        'email':userCredentials['email'],
        'password':userCredentials['password'],
        'profile':{
            'first_name':userCredentials['profile.first_name'],
            'last_name':userCredentials['profile.last_name'],
        }
    })
    .then((res) => console.log(res))
}