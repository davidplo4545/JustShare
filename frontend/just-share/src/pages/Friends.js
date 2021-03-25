import React, { useState, useContext, useEffect} from 'react'
import FriendsList from '../components/FriendsList'
import FriendPreview from '../components/FriendPreview'
import './friends.css'
import { getFriendRecommendations } from '../api/AuthenticationAPI'
import {UserContext} from '../hooks/UserContext'
const FriendsPage = () =>{
    const user = useContext(UserContext)
    const [previewedFriend, setPreviewedFriend] = useState(null)
    const [friendsRequested, setFriendsRequested] = useState([]) 
    const [friends, setFriends] = useState([]) 

    useEffect(() => {
        getFriendRecommendations(user.token, setFriends)
      }, []);


    return (
        <div className="friends-main">
            <FriendsList friends={friends} requestedFriends={friendsRequested} setPreviewedFriend={setPreviewedFriend}/>
            <FriendPreview previewedFriend={previewedFriend}/>
        </div>
    )
}

export default FriendsPage;