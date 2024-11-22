import React, { Component } from 'react'
import './timesUp.css'
import clock_icon from '../../icons/times_up_clock_icon.png'

export default class TimesUp extends Component {
  render() {
    let {on_logout} = this.props;
    return (
      <div className='timesup_main_body'>
        <div className='timesup_layout'>
            <img src={clock_icon} alt="clock icon" className='clock_icon' />
            <div className='titles'>
                <h1 className='title_timesup'>Time❜s Up</h1>
                <p className='sub_title'>Your exam time is up<br />This session has been ended by the administrator. Please contact them if you have any concerns.</p>
                <button className='btn logout' onClick={on_logout}>Logout</button>
            </div>
        </div>
      </div>
    )
  }
}
