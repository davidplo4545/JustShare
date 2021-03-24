import React, { Component } from 'react'
import unknownImg from '../images/unknown.jpg';
import Button from 'react-bootstrap/Button'
const FriendsListItem = ({friend, isRequested, setPreviewedFriend}) =>{
    const onFriendClicked = () =>{
        setPreviewedFriend(friend)
        console.log('here')
    }
    if (isRequested)
    return (
        <li onClick={onFriendClicked} className="friend-item">
        <img src={unknownImg} width="50" height="50"/>
            <div className="friend-data">
                <p>{`${friend.firstName} ${friend.lastName} ` }</p>

                <div className="request-buttons">
                    <Button className="btn-accept" variant="primary">Accept</Button>
                    <Button className="btn-decline" variant="danger">Decline</Button>
                </div>
            </div>
        </li>
    )
    return (
            <li onClick={onFriendClicked} className="friend-item">
                <img src={unknownImg} width="50" height="50"/>
                <div className="friend-data">
                    <p>{`${friend.firstName} ${friend.lastName} ` }</p>

                    <div className="status-buttons">
                        <Button className="" variant="primary">Add Friend</Button>
                        {/* <Button variant="danger">Danger</Button> */}
                    </div>
                </div>
            </li>
    

    
    )
}

export default FriendsListItem  ;