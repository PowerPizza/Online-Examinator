import React, { Component } from 'react'
import "./App.css"
import HeaderBar from './components/header/HeaderBar'
import { io } from 'socket.io-client'
import LoginPage from './components/login/LoginPage'
import MessageBoxFull from './components/messages/MessageBoxFull'
import AttemptingArea from './components/content/AttemptingArea'
import StartPanel from './components/content/StartPanel'
import AttemptFinished from './components/outros/AttemptFinished'
import TimesUp from './components/outros/TimesUp'
import PromptYesNo from './components/messages/PromptYesNo'

export default class App extends Component {
  constructor(){
    super()
    this.state = {
      loginCreds: null,
      msg_box: null,
      qp_meta_data: null,
      isStarted: null,
      finished: false,
      times_up_win: null,
      remainingTime: "00 : 00 : 00",
      yesNoPrompt: null
    }
    this.setup_ws();
  }

  setup_ws = ()=>{
    this.ws = io();
    this.ws.on("connect", ()=>{
      console.log("CONNECTED");
      this.requestPrimaryInfo();
    });

    this.ws.on("disconnect", ()=>{
      console.log("DISCONNECTED");
    });

    this.ws.on("times_up", ()=>{
      if (this.state.isStarted){
        const on_logout_func = ()=>{
          this.setState({loginCreds: null, qp_meta_data: null, isStarted: null, times_up_win: null});
        }
        this.setState({times_up_win: <TimesUp on_logout={on_logout_func} />});
        this.ws.disconnect();
      }
    });

    this.ws.on("login_credentials", (data_)=>{
      this.setState({loginCreds: data_});
      // console.log(data_);
    });

    this.ws.on("qp_metadata", (data_)=>{
      this.setState({qp_meta_data: data_});
      // console.log(data_);
    });

    this.ws.on("timer_broadcast", (data_)=>{
      // data_ (format) = [hh, mm, ss]
      this.setState({remainingTime: `${String(data_[0]).padStart(2, "0")} : ${String(data_[1]).padStart(2, "0")} : ${String(data_[2]).padStart(2, "0")}`});
    })
  }

  createMessageBox = (msg_, layout_="error")=>{
    this.setState({msg_box: <MessageBoxFull msg={msg_} on_close_msg={this.closeMsgBox} layout={layout_}/>});
    setTimeout(this.closeMsgBox, 5000);
  }
  closeMsgBox = ()=>{
    this.setState({msg_box: null});
  }

  createYesNoPrompt = (msg_, on_yes, on_no)=>{
    this.setState({yesNoPrompt: <PromptYesNo msg={msg_} yes_command={()=>{
      on_yes();
      this.setState({yesNoPrompt: null});
    }} no_command={()=>{
      on_no();
      this.setState({yesNoPrompt: null});
    }} />});
  }

  requestPrimaryInfo = ()=>{
    this.ws.emit("get_login_cred");
    this.ws.emit("qp_metadata");
  }

  sendLogs = (msg)=>{
    this.ws.emit("add_log", msg);
  }

  onStartPaper = ()=>{
    this.setState({isStarted: true});
  }

  finishExam = ()=>{
    this.setState({finished: true});
  }

  onLogOut = async () => {
    let resp = await fetch("/logout", { method: "POST" });
    let status_ = await resp.text();
    if (status_ === "LOGOUT_SUCCESS"){
      this.setState({loginCreds: null, isStarted: null, finished: null})
    }
  }

  render() {
    return (
      <div className='main_body'>
        <HeaderBar login_creds={this.state.loginCreds} onLogOut={this.onLogOut} />
        {this.state.msg_box}
        {this.state.finished ? <AttemptFinished onLogOut={this.onLogOut} /> : null}
        {this.state.times_up_win}
        {this.state.yesNoPrompt}
        {/* <TimesUp /> */}

        {this.state.loginCreds && this.state.qp_meta_data ?
          this.state.isStarted ? 
          <AttemptingArea qp_metadata={this.state.qp_meta_data} sendLogs={this.sendLogs} loginCreds={this.state.loginCreds} finishExam={this.finishExam} remaining_time={this.state.remainingTime} createMessageBox={this.createMessageBox} createYesNoPrompt={this.createYesNoPrompt} /> 
          : 
          <StartPanel qp_meta_data={this.state.qp_meta_data} onStartPaper={this.onStartPaper} /> 
        : <LoginPage createMessageBox={this.createMessageBox} />}
      </div>
    )
  }
}
