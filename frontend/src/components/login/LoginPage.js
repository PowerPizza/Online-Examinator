import React, { Component } from 'react'
import './loginPage.css'
import { Eye, EyeClosed } from 'iconoir-react'

export default class LoginPage extends Component {
  constructor() {
    super();
    this.state = { showPassword: false, user_id: "", password: "" }
  }

  toggleShowPassword = () => {
    this.setState({ showPassword: !this.state.showPassword });
  }

  on_change_uid = (ele) => {
    this.setState({ user_id: ele.target.value });
  }

  on_change_password = (ele) => {
    this.setState({ password: ele.target.value });
  }

  on_submit_login = async () => {
    const resp = await fetch("/login", { method: "POST", body: JSON.stringify({ "uid": this.state.user_id, "password": this.state.password }), headers: {"SameSite": "None"} });
    let resp_text = await resp.text();
    if (resp_text === "INVALID_CREDENTIALS"){
      this.props.createMessageBox("Failed to login : INVALID_CREDENTIALS");
    }
    else if(resp_text === "LOGIN_SUCCESS"){
      // WHILE USING WEBSOCKET TO GET CREDENTIALS, I DON'T KNOW WHY BUT EVEN AFTER ASSIGNING SESSION FIRST IT WAS GIVING EMPTY CREDENTIALS...
      // SO USED RELOAD METHOD INSTEAD.
      window.location.reload();
    }
  }
  
  render() {
    return (
      <div className='login_main_body'>
        <h1 className='heading_login'>LOGIN</h1>

        <label htmlFor="user_id">User ID</label>
        <input type="text" name='user_id' onChange={this.on_change_uid} />

        <span style={{ marginBottom: "20px" }}></span>

        <label htmlFor="password">Password</label>
        <div className='password_holder'>
          <input type={this.state.showPassword ? "text" : "password"} name='password' onChange={this.on_change_password} />
          {this.state.showPassword ? <EyeClosed width={35} height={35} fill='blue' onClick={this.toggleShowPassword} /> : <Eye width={35} height={35} fill='blue' onClick={this.toggleShowPassword} />}
        </div>

        <button className='submit_btn' onClick={this.on_submit_login}>submit</button>
      </div>
    )
  }
}
