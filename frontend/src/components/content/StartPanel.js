import React, { Component } from 'react'
import './startPanel.css'

export default class StartPanel extends Component {
    render() {
        let {onStartPaper, qp_meta_data} = this.props;
        return (
            <div className='start_panel_main_body'>
                <h1 className='qp_title'>{qp_meta_data["title"]} </h1>
                <div className='inline_info'>
                    <h3 style={{ textAlign: "left", width: "100%" }}>Questions : {qp_meta_data["no_of_questions"]}</h3>
                    <h3 style={{ textAlign: "right", width: "100%" }}>Max Marks : {qp_meta_data["max_marks"]}</h3>
                </div>
                <h3 style={{ textAlign: "center", margin: "0" }}>Subject : {qp_meta_data["subject"]}</h3>
                <div className='start_btn' onClick={onStartPaper}>
                    <div className='clickable'>
                        <span>START</span>
                    </div>
                </div>
            </div>
        )
    }
}
