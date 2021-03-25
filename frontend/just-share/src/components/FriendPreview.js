import React, { Component } from 'react'

const FriendPreview = ({previewedFriend}) =>{
    return (
        <div className="friend-preview">
            {previewedFriend ? <h1>You have selected {previewedFriend.profile.first_name}</h1>
            :
            <h1>No friend selected</h1>
            }
        </div>
    )
}
export default FriendPreview;