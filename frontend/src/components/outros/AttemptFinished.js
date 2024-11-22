import React, { Component } from 'react'
import './attemptFinished.css'
import mail_icon from '../../icons/mail_later_icon.png'

export default class AttemptFinished extends Component {
    render() {
        let {onLogOut} = this.props;

        return (
            <div className='finish_main_body'>
                <div className='popup_'>
                    <img src={mail_icon} alt="mail icon" className='mail_icon' draggable={false} />
                    <p className='tanku'>Thank you</p>
                    <span className='msg1'>Your submission has been saved.</span>
                    <button className='btn back_to_site' onClick={onLogOut}>Logout</button>
                </div>
            </div>
        )
    }
}
