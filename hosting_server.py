from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit
import socketio
import threading, ctypes, webbrowser
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Style
from tkinter.ttk import LabelFrame as ttkLabelFrame
from tkinter.ttk import Spinbox as ttkSpinBox
from tkinter.ttk import Checkbutton as ttkCheckButton
import socket
import json
from application_resources import *
from datetime import datetime, timedelta
import time

class TimerEntry(Frame):
    hh_val, mm_val, ss_val = [None]*3
    entry_hh, entry_mm, entry_ss = [None]*3
    isRunning = False

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.hh_val = StringVar(value="00")
        self.mm_val = StringVar(value="00")
        self.ss_val = StringVar(value="00")
        Label(self, text="HH", font=("Russo One", 16), bg="red").grid(row=0, column=0, ipadx=15)
        Label(self, text="MM", font=("Russo One", 16), bg="orange").grid(row=0, column=1, ipadx=15)
        Label(self, text="SS", font=("Russo One", 16), bg="gold").grid(row=0, column=2, ipadx=15)
        style_arrow = Style()
        style_arrow.theme_use("alt")
        style_arrow.configure("TSpinbox", arrowsize=20, arrowcolor="green")
        
                
        self.entry_hh = ttkSpinBox(self, from_=0, to=60, style="TSpinbox", textvariable=self.hh_val, font=("Russo One", 16), width=2, justify=CENTER)
        self.entry_hh.grid(row=1, column=0, sticky=NSEW)
        self.entry_hh.bind("<KeyRelease>", lambda eve: self.__preventInvalidValue(eve, self.hh_val))

        self.entry_mm = ttkSpinBox(self, from_=0, to=60, style="TSpinbox", textvariable=self.mm_val, font=("Russo One", 16), width=2, justify=CENTER)
        self.entry_mm.grid(row=1, column=1, sticky=NSEW)
        self.entry_mm.bind("<KeyRelease>", lambda eve: self.__preventInvalidValue(eve, self.mm_val))

        self.entry_ss = ttkSpinBox(self, from_=0, to=60, style="TSpinbox", textvariable=self.ss_val, font=("Russo One", 16), width=2, justify=CENTER)
        self.entry_ss.grid(row=1, column=2, sticky=NSEW)
        self.entry_ss.bind("<KeyRelease>", lambda eve: self.__preventInvalidValue(eve, self.ss_val))

    def __preventInvalidValue(self, eve, text_var):
        if len(text_var.get()) > 2:
            text_var.set(text_var.get()[0:2])
        try:
            int(eve.char)
            if int(text_var.get()) > 60:
                text_var.set("60")
        except BaseException:
            text_var.set(text_var.get().replace(eve.char, ""))
        if len(text_var.get()) == 0:
            text_var.set("00")

    def getDurationInSec(self):
        try:
            total_duration = int(self.hh_val.get()) * 3600
            total_duration += int(self.mm_val.get()) * 60
            total_duration += int(self.ss_val.get())
            return total_duration
        except BaseException:
            return 0
        
    def startTimer(self, callback_onstop=None, runtime_callback=None):
        def run_reverse():
            cur_time = datetime.strptime(f"{self.hh_val.get()}:{self.mm_val.get()}:{self.ss_val.get()}", "%H:%M:%S")
            if cur_time.time() == datetime.strptime("00:00:00", "%H:%M:%S").time() or not self.isRunning:
                self.isRunning = False
                if callable(callback_onstop): callback_onstop()
                return
            new_time = cur_time - timedelta(seconds=1)
            self.hh_val.set(new_time.hour)
            self.mm_val.set(new_time.minute)
            self.ss_val.set(new_time.second)
            if callable(runtime_callback): runtime_callback(new_time.hour, new_time.minute, new_time.second)
            self.after(1000, run_reverse)
        self.isRunning = True
        run_reverse()

    def stopTimer(self):
        self.isRunning = False
    
    def disableAllEntries(self):
        self.entry_hh.config(state="disabled", foreground="black")
        self.entry_mm.config(state="disabled", foreground="black")
        self.entry_ss.config(state="disabled", foreground="black")

    def enableAllEntries(self):
        self.entry_hh.config(state="normal")
        self.entry_mm.config(state="normal")
        self.entry_ss.config(state="normal")


class ActualWebSocketClient(socketio.Client):
    def __init__(self, host, port):
        super().__init__()
        self.connect(f"http://{host}:{port}")
        @self.on("connect")
        def on_client_ctc():
            print("WS SELF CLIENT CONNECTED.")


class WebServerConfigForm(Toplevel):
    ip_addr = None
    port = None
    result_file_name = None
    btn_start_server = None
    btn_stop_server = None
    starting_in_lbl = None
    logs_view = None
    time_duration = None
    auto_stop = None
    resubmittion = None

    def __init__(self, master, ip_addr="0.0.0.0", port="5000"):
        super().__init__(master=master)
        self.ip_addr = StringVar(value=ip_addr)
        self.port = StringVar(value=port)
        self.result_file_name = StringVar(value="")
        self.auto_stop = IntVar(value=0)
        self.resubmittion = IntVar(value=0)
        self.grab_set()
        self.transient(master)
        self.title("Web-Server Configs")
        self.resizable(False, False)
        self.geometry(f"900x550+{master.winfo_screenwidth()//2 - 900//2}+{master.winfo_screenheight()//2 - 300}")
        self.update()

        fr_content = Frame(self, bg="#FFFFFF")

        fr_ip_addr_ = Frame(fr_content, bg="#FFFFFF")
        Label(fr_ip_addr_, text="IP ADDRESS", font=("Russo One", 16), fg="blue", bg="#FFFFFF").pack(side=LEFT)
        ip_entry = Combobox(fr_ip_addr_, font=("Russo One", 16), values=list(set(["127.0.0.1", "0.0.0.0", QPWebServer.getPrivateIP()])), textvariable=self.ip_addr)
        ip_entry.pack(fill=X, padx=20)
        fr_ip_addr_.pack(fill=X, padx=20, pady=5)
        

        fr_port_ = Frame(fr_content, bg="#FFFFFF")
        Label(fr_port_, text="PORT", font=("Russo One", 16), fg="blue", bg="#FFFFFF").pack(side=LEFT)
        port_entry = Entry(fr_port_, font=("Russo One", 16), highlightthickness=1, highlightbackground="blue", width=6, textvariable=self.port)
        port_entry.pack(padx=20, side=LEFT)
        fr_port_.pack(fill=X, padx=20, pady=10)

        fr_result_fname = Frame(fr_content, bg="#FFFFFF")
        Label(fr_result_fname, text="Result File Name", font=("Russo One", 16), fg="blue", bg="#FFFFFF", anchor=NW, justify=LEFT).pack(side=LEFT, ipadx=10)
        result_file_name = Entry(fr_result_fname, font=("Russo One", 16), highlightthickness=1, highlightbackground="blue", textvariable=self.result_file_name)
        result_file_name.pack(side=LEFT, fill=X, expand=True)
        def check_file_exists(*eve):
            if os.path.exists(os.path.join(ApplicationPaths.RESULT_DIR, self.result_file_name.get()+".json")):
                result_file_name.config(highlightcolor="red")
            else:
                result_file_name.config(highlightcolor="green")
        result_file_name.bind("<KeyRelease>", check_file_exists)
        result_file_name.bind("<Button-1>", check_file_exists)
        Label(fr_result_fname, text=".json", font=("Russo One", 16), fg="#525252", bg="#FFFFFF").pack(side=LEFT)
        fr_result_fname.pack(fill=X, padx=20)

        fr_duration = Frame(fr_content, bg="#FFFFFF")
        Label(fr_duration, text="Duration", font=("Russo One", 16), fg="blue", bg="#FFFFFF", anchor=NW, justify=LEFT).pack(side=LEFT, ipadx=10)
        self.time_duration = TimerEntry(fr_duration, bg="#FFFFFF")
        self.time_duration.pack(side=LEFT)
        fr_duration.pack(fill=X, padx=20, pady=10)

        fr_auto_stop = Frame(fr_content, bg="#FFFFFF")
        s2 = Style()
        s2.configure("MY.TCheckbutton", background="#FFFFFF", font=("Bahnschrift", 16), foreground="blue")
        check_btn = ttkCheckButton(fr_auto_stop, takefocus=0, text="Automatically stop when time finishes ?", style="MY.TCheckbutton", variable=self.auto_stop)
        check_btn.pack()
        fr_auto_stop.pack(fill=X, padx=20)

        fr_resubmittion = Frame(fr_content, bg="#FFFFFF")
        check_resubmit_btn = ttkCheckButton(fr_resubmittion, takefocus=0, text="Allow Resubmittion ?", style="MY.TCheckbutton", variable=self.resubmittion)
        check_resubmit_btn.pack()
        fr_resubmittion.pack(fill=X, padx=20)

        self.starting_in_lbl = Label(fr_content, text="", bg="#FFFFFF", font=("Russo One", 16), fg="red")
        self.starting_in_lbl.pack(pady=4)
        
        fr_btn_holder = Frame(fr_content, bg="#FFFFFF")
        self.btn_start_server = Button(fr_btn_holder, text="Start", bg="#35ce75", fg="white", activebackground="#35ce75", activeforeground="white", font=("Calibri", 14, "bold"), relief="ridge")
        self.btn_start_server.pack(ipadx=20, padx=5, pady=5, side=RIGHT)
        self.btn_stop_server = Button(fr_btn_holder, text="Stop", bg="#e85242", fg="white", activebackground="#e85242", activeforeground="white", font=("Calibri", 14, "bold"), relief="ridge")
        fr_btn_holder.pack(anchor=SE)
        
        logs_style = Style(self)
        logs_style.theme_use("alt")
        logs_style.configure("clam.TLabelframe", relief="solid", bordercolor="blue", background="white")
        logs_style.configure("clam.TLabelframe.Label", font=("Bahnschrift", 18), foreground="blue", background="white")
        fr_logs = ttkLabelFrame(fr_content, text="Logs", style="clam.TLabelframe")
        self.logs_view = Text(fr_logs, bg="#FFFFFF", font=("Bahnschrift", 16), border=0, highlightthickness=1, highlightbackground="#c7c7c7", state="disabled")
        self.logs_view.pack(fill=BOTH, padx=2, pady=2)
        fr_logs.pack(fill=BOTH, padx=2, pady=2)
        # ADD AUTO STOP IN FEATURE ALSO

        fr_content.pack(fill=BOTH, expand=True)

    

class QPWebServer(Flask):
    thread_id = None
    application_instance = None
    host = None
    port = None
    on_server_started = None
    on_server_stoped = None
    web_svr = None
    config_win = None
    result_file_path = None
    ws_client = None

    def __init__(self, app_instance, qp_data):
        super().__init__(__name__, template_folder=os.getcwd(), static_folder=os.getcwd(), static_url_path="/")
        self.qp_data = qp_data
        self.application_instance = app_instance
        self.secret_key = "IDJ883934NDAS89DHAS923NS"
        self.web_svr = SocketIO(self, cors_allowed_origins="*")
        self.setup_routes()
        
    def generate_qp_metadata(self):
        qp_data = dict(self.qp_data)
        del qp_data["questions"]
        qp_data["no_of_questions"] = len(self.qp_data["questions"])
        return qp_data
    
    def setup_routes(self):
        @self.route("/")
        def home_page():
            return render_template("index.html")
        
        @self.route("/login", methods=["POST"])
        def onLogin():
            cred_arrived = json.loads(request.data.decode())
            with open(ApplicationPaths.USER_CREDENTIALS_FILE, "r") as fp:
                users = json.load(fp)
                if cred_arrived["uid"] in users and cred_arrived["password"] == users[cred_arrived["uid"]]["password"]:
                    session["creds"] = users[cred_arrived["uid"]] | {"uid": cred_arrived["uid"]}
                    return "LOGIN_SUCCESS"
                else:
                    return "INVALID_CREDENTIALS"
                
        @self.route("/logout", methods=["POST"])
        def on_logout():
            if "creds" in session:
                del session["creds"]
                return "LOGOUT_SUCCESS"
            else:
                return "LOGOUT_FAILED"
            
        @self.route("/get_question", methods=["POST"])
        def on_get_question():
            data_ = json.loads(request.data.decode())
            q_no = data_["q_no"]
            return json.dumps(self.qp_data["questions"][q_no])

        @self.route("/finish_attempt", methods=["POST"])
        def on_finish_attempt():
            data_ = json.loads(request.data.decode())
            result_ = json.load(open(self.result_file_path, 'r'))
            data_["creds"] = session["creds"]
            if session["creds"]['uid'] not in result_["users"]:
                result_["users"][session["creds"]['uid']] = data_
                json.dump(result_, open(self.result_file_path, 'w'))
                return "OK"
            
            if "OVER_WRITE" in data_:
                del data_["OVER_WRITE"]
                result_["users"][session["creds"]['uid']] = data_
                json.dump(result_, open(self.result_file_path, 'w'))
                return "OVER_WRITTEN"
            
            if self.config_win.resubmittion.get():
                return "OVER_WRITE"
            
            else:
                return "ALREADY_SUBMITTED"
        
        # ------------------------- WEBSOCKET END POINTS ---------------------------
        @self.web_svr.on("get_login_cred")
        def send_login_creds():
            if "creds" in session:
                self.web_svr.emit("login_credentials", session["creds"], to=request.sid)
            else:
                self.web_svr.emit("login_credentials", None, to=request.sid)

        @self.web_svr.on("qp_metadata")
        def send_qp_metadata():
            self.web_svr.emit("qp_metadata", self.generate_qp_metadata(), to=request.sid)

        @self.web_svr.on("add_log")
        def add_log(msg_):
            self.config_win.logs_view.config(state="normal")
            self.config_win.logs_view.insert(END, msg_+"\n")
            self.config_win.logs_view.config(state="disabled")

        @self.web_svr.on("timer_broadcast")
        def on_timer_broadcast(data_):
            emit("timer_broadcast", data_, include_self=False, broadcast=True)

        @self.web_svr.on("times_up")
        def on_times_up():
            emit("times_up", include_self=False, broadcast=True)


    def start_server(self):
        self.config_win = WebServerConfigForm(self.application_instance, ip_addr=self.getPrivateIP())
        self.config_win.result_file_name.set(self.qp_data["title"])
        running_error = None
        def __run():
            try:
                self.config_win.btn_start_server.config(state="disabled", text="Starting...")
                self.web_svr.run(self, host=self.host, port=int(self.port), allow_unsafe_werkzeug=True)
            except BaseException as e:
                nonlocal running_error
                running_error = e

        def on_run_server():
            if not self.config_win.time_duration.getDurationInSec():
                if not messagebox.askyesno("Infinite Run", "No time duration is provided, you have to manually stop the server\nDo you want to start the exam ?"):
                    return

            assumed_path_ = os.path.join(ApplicationPaths.RESULT_DIR, self.config_win.result_file_name.get()+".json")
            if not os.path.exists(assumed_path_):
                json.dump({"qp_metadata": self.generate_qp_metadata(), "question_paper": self.qp_data, "users": {}}, open(assumed_path_, "w"))
                self.result_file_path = assumed_path_
            else:
                messagebox.showerror("Existing Result File", "Startup Failed: The result file name you provided already exists. Please enter a unique name.")
                return
            
            self.host = self.config_win.ip_addr.get()
            self.port = self.config_win.port.get()
            hosting_ip = self.host
            if self.host == "0.0.0.0":
                hosting_ip = self.getPrivateIP()
            td = threading.Thread(target=__run)
            td.start()
            alive_since = 10
            def check_server_startup():
                nonlocal alive_since
                if td.is_alive() and alive_since > 0:
                    self.config_win.starting_in_lbl.config(text=f"Starting in ({alive_since})", fg="blue")
                    alive_since -= 1
                    self.application_instance.after(1000, check_server_startup)
                else:
                    if not td.is_alive():  # SERVER STARTUP FAILED
                        os.remove(assumed_path_)
                        self.config_win.starting_in_lbl.config(text=f"Failed", fg="red")
                        self.config_win.btn_start_server.config(state="normal", text="Start")
                        self.config_win.btn_stop_server.pack_forget()
                        self.config_win.btn_start_server.pack(ipadx=20, padx=5, pady=5, side=RIGHT)
                        messagebox.showerror("Starting failed", f"Server not started or crashed due to invalid host or port provided\nError : {running_error}")
                    else:  # SERVER STARTED
                        self.ws_client = ActualWebSocketClient(hosting_ip, self.port)
                        self.config_win.starting_in_lbl.config(text=f"Running\nhttp://{hosting_ip}:{self.port}", fg="green", cursor="")
                        self.config_win.btn_start_server.pack_forget()
                        self.config_win.btn_stop_server.pack(ipadx=20, padx=5, pady=5, side=RIGHT)
                        if self.config_win.time_duration.getDurationInSec() > 0:
                            def onTimerEnd():
                                self.config_win.time_duration.enableAllEntries()
                                if self.config_win.auto_stop.get():
                                    on_stop_server()
                            def on_timer_update(hh, mm, ss):
                                self.ws_client.emit("timer_broadcast", [hh, mm, ss])
                            self.config_win.time_duration.disableAllEntries()
                            self.config_win.time_duration.startTimer(callback_onstop=onTimerEnd, runtime_callback=on_timer_update)
                        if callable(self.on_server_started) : self.on_server_started()
                        if messagebox.askyesno("Started", f"Question paper is online now on http://{hosting_ip}:{self.port}\nWould you like to open it in browser?"):
                            webbrowser.open_new_tab(f"http://{hosting_ip}:{self.port}")
            check_server_startup()
            self.thread_id = td.native_id

        self.config_win.btn_start_server.config(command=on_run_server)

        def on_stop_server():
            self.ws_client.emit("times_up")
            time.sleep(3)
            self.stop_server()
            self.config_win.starting_in_lbl.config(text="")
            self.config_win.btn_start_server.config(state="normal", text="Start")
            self.config_win.btn_stop_server.pack_forget()
            self.config_win.btn_start_server.pack(ipadx=20, padx=5, pady=5, side=RIGHT)
        self.config_win.btn_stop_server.config(command=on_stop_server)

    def stop_server(self):
        if not self.thread_id:
            return
        for thread_ in threading.enumerate():
            if thread_.native_id == self.thread_id:
                self.config_win.time_duration.stopTimer()
                if self.ws_client:
                    self.ws_client.disconnect()
                    self.ws_client = None
                ctypes.pythonapi.PyThreadState_SetAsyncExc(self.thread_id, ctypes.py_object(SystemExit))
                print(f"SERVER STOPPED AT {self.host}:{self.port} | THREAD ID ({self.thread_id})")
                self.thread_id = None
                if callable(self.on_server_stoped) : self.on_server_stoped()
                break
    
    @staticmethod
    def getPrivateIP():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        except BaseException:
            return "127.0.0.1"
        
if __name__ == '__main__':
    w1 = Tk()
    qp_data_ = {"title": "Half Yearly Examinations (2024)", "subject": "ECONOMICS", "max_marks": 10, "questions": [{"question": "What is eco", "options": ["dsa", "sa"], "correct_opts": ["sa"], "max_marks": 5}, {"question": "dsada", "options": ["dsa", "sa"], "correct_opts": ["sa"], "max_marks": 5}]}

    s1 = QPWebServer(w1, qp_data_)
    s1.start_server()
    w1.mainloop()