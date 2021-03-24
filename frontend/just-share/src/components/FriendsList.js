import React, {useState} from 'react'
import FriendsListItem from './FriendsListItem';

const FriendsList = ({friends, setPreviewedFriend}) =>{
    
    return (
        <div className="friends-side">
            <h2>Friends</h2>
            <h4>Friend requests</h4>
            <ul className="requested-friends-list">
                {friends.map((friend) => 
                    <FriendsListItem friend={friend} setPreviewedFriend={setPreviewedFriend} isRequested={true}/>)}
            </ul>
            <h4>People you may know</h4>
            <ul className="friends-list">
                {friends.map((friend) => 
                    <FriendsListItem friend={friend} setPreviewedFriend={setPreviewedFriend}/>)}
            </ul>
                    
        </div>
    )
}

export default FriendsList;