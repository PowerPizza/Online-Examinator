import React, { Component } from 'react'
import './attemptingArea.css'
import { Truck } from 'iconoir-react';

export default class AttemptingArea extends Component {
  answers = {}
  constructor() {
    super();
    this.state = { current_question: null, cur_q_no: 0, selected_answer: null}
    this.loadQuestion(0);
  }

  loadQuestion = async (question_num) => {
    const resp = await fetch("/get_question", { method: "POST", body: JSON.stringify({ "q_no": question_num }) });
    let question_data = await resp.text();
    this.setState({ current_question: JSON.parse(question_data) });
  }

  on_change_option = (ele)=>{
    this.setState({selected_answer: ele.target.value});
    this.answers[this.state.cur_q_no] = {"value": ele.target.value, "index": Number(ele.target.getAttribute("index"))};
  }

  onPrevQuestion = () => {
    if (this.state.cur_q_no === 0) {
      return
    }
    this.loadQuestion(this.state.cur_q_no - 1).then(() => {
      this.setState({ cur_q_no: this.state.cur_q_no - 1 });
    })
  }

  onNextQuestion = () => {
    try{
      document.getElementById("card_select_"+(this.state.cur_q_no+1)).scrollIntoView();
    }catch (e){};
    if (this.state.cur_q_no === this.props.qp_metadata["no_of_questions"] - 1) {
      return
    }
    this.loadQuestion(this.state.cur_q_no + 1).then(() => {
      this.setState({ cur_q_no: this.state.cur_q_no + 1});
    })
  }

  onFinishAttempt = async()=>{
    let resp = await fetch("/finish_attempt", {method: "POST", body: JSON.stringify(this.answers)});
    let status_ = await resp.text();
    if (status_ === "OK"){
      this.props.finishExam();
      this.props.sendLogs(`Finished Attempt || ${this.props.loginCreds['uid']} | ${this.props.loginCreds['u_name']}`);
    }
    else if (status_ === "ALREADY_SUBMITTED"){
      this.props.createMessageBox("You have already submitted and resubmittion is not allowed in this exam.");
    }
    else if (status_ === "OVER_WRITE"){
      const on_yes = async ()=>{
        this.answers["OVER_WRITE"] = true;  // here creating new key in a dict but not deleting it when response comes back, since this dict belongs to the class so may cause bug << ALERT WITH THIS LINE
        let resp2 = await fetch("/finish_attempt", {method: "POST", body: JSON.stringify(this.answers)});
        let status_2 = await resp2.text();
        if (status_2 === "OVER_WRITTEN"){
          this.props.finishExam();
          this.props.sendLogs(`Re-Submitted || ${this.props.loginCreds['uid']} | ${this.props.loginCreds['u_name']}`);
        }
      };
      this.props.createYesNoPrompt("Seems like you have already submitted once from this account, would you like to overwrite the last submittion ?", on_yes, ()=>{});
    }
  }

  render() {
    let { qp_metadata, remaining_time } = this.props;
    if (!this.state.current_question) {
      return (<>LOADING...</>)
    }

    return (
      <div className='attempt_area_main_body'>
        <div className="subheader">
          <h1 className='paper_title'>
            {qp_metadata["subject"]} - {qp_metadata["title"]}
          </h1>
          <span className='remaining_time'>Time Left : {remaining_time}</span>
        </div>
        <span className='sub_heading'>MM : {qp_metadata["max_marks"]}</span>

        <div className='two_split'>
          <div className='question_view'>
            <p>{this.state.cur_q_no + 1}&#41; {this.state.current_question["question"]} ({this.state.current_question["max_marks"]})</p>
            {this.state.current_question["options"].map((opt_, idx) => {
              return (
                <div key={(this.state.cur_q_no + 1) + "_opt_" + idx} className='option_'>
                  <input type="radio" name="N" value={opt_} index={idx} onChange={this.on_change_option} defaultChecked={this.answers[this.state.cur_q_no] ? this.answers[this.state.cur_q_no]["index"] === idx : false}/>
                  <span>{opt_}</span><br />
                </div>)
            })}
            <div style={{ display: "flex", width: "100%", marginTop: "30px" }}>
              <button className='btn previous' onClick={this.onPrevQuestion}>Previous</button>
              <button className='btn next' onClick={this.onNextQuestion}>Next</button>
            </div>
          </div>

          <div className='exam_navigation_list'>
            <p className='tab_name'>Exam navigation</p>
            <div className='holder_'>
              {[...Array(qp_metadata["no_of_questions"])].map((ele, idx) => {
                return <span className={`q_no_card ${this.state.cur_q_no === idx ? "selected" : this.answers[idx] ? "checked" : ""}`} key={"card_" + idx} id={"card_select_" + idx}>{idx + 1}</span>
              })}
            </div>
            <button className='btn finish_' onClick={this.onFinishAttempt}>Finish attempt...</button>
          </div>
        </div>
      </div>
    )
  }
}
