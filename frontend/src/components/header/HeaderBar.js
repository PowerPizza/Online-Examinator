import React, { Component } from 'react'
import './headerBar.css'
import software_icon from '../../icons/software_icon.png'
import { LogOut, User } from 'iconoir-react'

export default class HeaderBar extends Component {
  constructor(){
    super();
    this.state = {loginDetailsOpen: false}
  }

  onToggleLoginDetails = ()=>{
    this.setState({loginDetailsOpen: !this.state.loginDetailsOpen});
  }

  render() {
    let {login_creds, onLogOut} = this.props;
    return (
      <div className='header_main_body'>
        <img src={software_icon} alt="software icon" className='app_icon' draggable={false} />
        <h2>Online Examinator</h2>
        {login_creds ? 
        <div className='account_btn' onClick={this.onToggleLoginDetails}>
          <div style={{display: "flex", justifyContent: "center", alignItems: "center", marginTop: '3px'}}><User width={40} height={40}/></div>
          { this.state.loginDetailsOpen ? 
          <div className='user_info' onClick={eve => eve.stopPropagation()}>
            <span>User ID : {login_creds["uid"]}</span>
            <span>User Name : {login_creds["u_name"]}</span>
            <button className='logout_btn' onClick={onLogOut}><LogOut width={26} height={26} color='white' /> Logout</button>
          </div> : null }
        </div> : null }
      </div>
    )
  }
}
