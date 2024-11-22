import React, { Component } from 'react'
import './messageBoxFull.css'
import { CheckCircleSolid, InfoCircle, InfoCircleSolid, Xmark, XmarkCircleSolid } from 'iconoir-react'

export default class MessageBoxFull extends Component {
  render() {
    let {msg, on_close_msg, layout} = this.props;
    let text_color = "red";
    switch (layout) {
      case "error":
        text_color = "#ff0000"
        break;
      case "info":
        text_color = "#0080ff"
        break;
      case "success":
        text_color = "#0d9c00"
        break;
      default:
        break;
    }
    return (
      <div className='msgBoxFull_main_body' style={{backgroundColor: text_color+"1a", color: text_color, borderColor: text_color}}>
        {layout === "error" ?
          <XmarkCircleSolid width={40} height={40} className='icon_'/>
        : null}
        {layout === "info" ?
          <InfoCircleSolid width={40} height={40} className='icon_'/> 
        : null}
        {layout === "success" ? 
          <CheckCircleSolid width={40} height={40} className='icon_'/>
        : null}
        <span className='msg_'>{msg}</span>
        <button className='close_btn' style={{color: text_color, borderColor: text_color+"4d"}}>
            <Xmark width={40} height={40} onClick={on_close_msg}/>
        </button>
      </div>
    )
  }
}
