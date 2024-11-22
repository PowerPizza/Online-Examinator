import React, { Component } from 'react'
import './promptYesNo.css'

export default class PromptYesNo extends Component {
  render() {
    let {msg, yes_command, no_command} = this.props;
    return (
      <div className='promptysno_main_body'>
        <div className='content_prompt_ysno'>
            <span className='msg_'>{msg}</span>
            <button className='btn yes' onClick={yes_command}>Yes</button>
            <button className='btn no' onClick={no_command}>No</button>
        </div>
      </div>
    )
  }
}
