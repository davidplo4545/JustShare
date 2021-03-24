import React, { useState} from 'react'
import FriendsList from '../components/FriendsList'
import FriendPreview from '../components/FriendPreview'
import './friends.css'
const FriendsPage = () =>{

    const [previewedFriend, setPreviewedFriend] = useState(null)
    const [friendsRequested, setFriendsRequested] = useState([
        {email : 'test1@gmail.com',
        id: 1,
        firstName: 'david',
        lastName: 'plotkin',
        friends: [],
    },
        {email : 'test1@gmail.com',
        id: 2,
        firstName: 'shit',
        lastName: 'head',
            friends: [],
    },
        {email : 'test1@gmail.com',
        id: 3,
        firstName: 'dick',
        lastName: 'head',
        friends: [],
    },
        {email : 'test1@gmail.com',
        id: 4,
        firstName: 'yosi',
        lastName: 'bublil',
        friends: [],
    }
    ]) 
    const [friends, setFriends] = useState([
        {email : 'test1@gmail.com',
        id: 1,
        firstName: 'david',
        lastName: 'plotkin',
        friends: [],
    },
        {email : 'test1@gmail.com',
        id: 2,
        firstName: 'shit',
        lastName: 'head',
            friends: [],
    },
        {email : 'test1@gmail.com',
        id: 3,
        firstName: 'dick',
        lastName: 'head',
        friends: [],
    },
        {email : 'test1@gmail.com',
        id: 4,
        firstName: 'yosi',
        lastName: 'bublil',
        friends: [],
    }
    ]) 
    return (
        <div className="friends-main">
            <FriendsList friends={friends} setPreviewedFriend={setPreviewedFriend}/>
            <FriendPreview previewedFriend={previewedFriend}/>
        </div>
    )
}

export default FriendsPage;