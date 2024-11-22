import os, json, sys
if getattr(sys, 'frozen', False):
    import engineio
    from engineio.async_drivers import gevent

from tkinter import *
from tkinter import messagebox

from tkhelper import *
from hosting_server import *
from application_resources import *
from registerStudentWindow import *
from resultWindow import *
from qp_window import *

def fileSystemSetup():
    if not os.path.exists(ApplicationPaths.DATABASE_PATH):
        os.mkdir(ApplicationPaths.DATABASE_PATH)    
    if not os.path.exists(ApplicationPaths.QUESTION_PAPER_DIR):
        os.mkdir(ApplicationPaths.QUESTION_PAPER_DIR)
    if not os.path.exists(ApplicationPaths.RESULT_DIR):
        os.mkdir(ApplicationPaths.RESULT_DIR)
    if not os.path.exists(ApplicationPaths.USER_CREDENTIALS_FILE):
        json.dump({}, open(ApplicationPaths.USER_CREDENTIALS_FILE, "w"))

    
fileSystemSetup()
print(ApplicationPaths.DATABASE_PATH, os.listdir(ApplicationPaths.DATABASE_PATH))

class QuestionPaperList(ScrollableFrame):
    qp_list = None
    def __init__(self, master):
        super().__init__(master)
        self.config(bg="#e0ffcc")
        self.loadPapers()
    
    def loadPapers(self):
        [child.destroy() for child in self.winfo_children()]
        for item in os.listdir(ApplicationPaths.QUESTION_PAPER_DIR):
            paper_data = json.load(open(os.path.join(ApplicationPaths.QUESTION_PAPER_DIR, item), "r"))
            fr_list_row = Frame(self, highlightthickness=1, highlightbackground="green", bg="#f3ffd4")
            fr_lable_holder = Frame(fr_list_row, bg="#f3ffd4")
            Label(fr_lable_holder, text=f'TITLE : {paper_data["title"]}', font=("Lucida Console", 14), bg="#f3ffd4", anchor=NW, justify=LEFT).grid(row=0, column=0, sticky=NSEW, ipadx=60)
            Label(fr_lable_holder, text=f'MAX MARKS : {paper_data["max_marks"]}', font=("Lucida Console", 14), bg="#f3ffd4").grid(row=0, column=1, sticky=NSEW)
            Label(fr_lable_holder, text=f'SUBJECT : {paper_data["subject"]}', font=("Lucida Console", 14), bg="#f3ffd4", anchor=NW, justify=LEFT).grid(row=1, column=0, sticky=NSEW)
            Label(fr_lable_holder, text=f'TOTAL QUESTIONS : {len(paper_data["questions"])}', font=("Lucida Console", 14), bg="#f3ffd4").grid(row=1, column=1, sticky=NSEW)
            fr_lable_holder.pack(side=LEFT)

            fr_btn_holder = Frame(fr_list_row, bg="#f3ffd4")
            def create_control_btns():
                qp_id = item
                qp_data = paper_data

                def on_start_qp_server():
                    qp_svr = QPWebServer(app_instance=gui_app, qp_data=qp_data)
                    qp_svr.on_server_started = lambda : btn_start_stop_.config(command=qp_svr.stop_server, image=Icons.pause_icon)
                    qp_svr.on_server_stoped = lambda : btn_start_stop_.config(command=on_start_qp_server, image=Icons.play_icon)
                    qp_svr.start_server()
                btn_start_stop_ = Button(fr_btn_holder, image=Icons.play_icon, relief="ridge", bg="#2bffe6", activebackground="#2bffe6", command=on_start_qp_server)
                btn_start_stop_.grid(row=0, column=0, padx=1)

                def on_edit_qp():
                    edit_win = QP_Window(gui_app)
                    edit_win.title("Edit Question Paper")
                    edit_win.qp_id = qp_id.replace(".qp", "")
                    edit_win.question_paper = qp_data
                    edit_win.qp_title.set(qp_data["title"])
                    edit_win.qp_subject.set(qp_data["subject"])
                    edit_win.create_window()
                btn_edit_qp_ = Button(fr_btn_holder, image=Icons.pencil_icon_40x40, relief="ridge", bg="#fcbf44", activebackground="#fcbf44", command=on_edit_qp)
                btn_edit_qp_.grid(row=0, column=1, padx=1)

                def on_delete_qp():
                    if messagebox.askyesno("Delete Question Paper", "Do you really want to delete the question paper ?"):
                        os.remove(os.path.join(ApplicationPaths.QUESTION_PAPER_DIR, qp_id))
                        self.loadPapers()
                btn_delete_qp_ = Button(fr_btn_holder, image=Icons.delete_icon_40x40, relief="ridge", bg="#f5040b", activebackground="#f5040b", command=on_delete_qp)
                btn_delete_qp_.grid(row=0, column=2, padx=1)
            create_control_btns()
            fr_btn_holder.pack(side=RIGHT, padx=2)

            fr_list_row.pack(fill=X, padx=2, pady=2)


class Icons:
    pencil_icon_40x40 = None
    play_icon = None
    pause_icon = None
    delete_icon_40x40 = None

class Application(Tk):
    question_paper_list = None
    def __init__(self):
        super().__init__()
        Icons.pencil_icon_40x40 = TkIcon(IconPaths.PENCIL_ICON, (40, 40))
        Icons.play_icon = TkIcon(IconPaths.PLAY_ICON, (40, 40))
        Icons.pause_icon = TkIcon(IconPaths.PAUSE_ICON, (40, 40))
        Icons.delete_icon_40x40 = TkIcon(IconPaths.DELETE_ICON, (40, 40))

        self.title("Online Examination (OE v1.0)")
        self.geometry("600x500")
        self.state("zoomed")
        self.iconbitmap("software_icon.ico")
    
        self.panedWindow = PanedWindow(orient=HORIZONTAL)
        self.sidePanelLeft()
        self.panedWindow.pack(fill=BOTH, expand=True)
        self.panedWindow.configure(sashrelief=RIDGE)

    def rmEmptyListItem(self, lst):
        lst = list(lst)
        while '' in lst:
            lst.remove('')
        return lst

    def onCreateQPWindow(self):
        qp_win = QP_Window(self)
        qp_win.create_window()

    def onRegisterStudent(self):
        self.withdraw()
        reg_student_win = RegisterStudentWin(self)
        def on_delete_rsw():
            self.deiconify()
            self.state("zoomed")
            reg_student_win.destroy()
        reg_student_win.protocol("WM_DELETE_WINDOW", on_delete_rsw)
    
    def onResult(self):
        self.withdraw()
        result_win = ResultWindow(self)
        def close_result_win():
            self.deiconify()
            self.state("zoomed")
            result_win.destroy()
        result_win.protocol("WM_DELETE_WINDOW", close_result_win)
        result_win.close_win_btn.config(command=close_result_win)

    def onImportQuestionPaper(self):
        file_ = filedialog.askopenfilename(title="Select a text file", filetypes=[("All Files", "*.txt"), ])
        if file_:
            with open(file_, "r") as fp:
                file_data = self.rmEmptyListItem(fp.read().split("\n\n"))
                question_eles = []
                def on_save_marks(value_):
                    if not value_.isnumeric():
                        value_ = 1
                    for quest_itm in file_data:
                        q_ele = {"question": None, "options": [], "correct_opts": [], "max_marks": int(value_)}
                        for ele in self.rmEmptyListItem(quest_itm.split("\n")):
                            ele = ele.strip()
                            if ele.startswith("??"):
                                q_ele["question"] = ele[2:]
                            elif ele.startswith("*") and ele.endswith("||"):
                                q_ele["options"].append(ele[1:-2])
                                q_ele["correct_opts"].append(ele[1:-2])
                            elif ele.startswith("*"):
                                q_ele["options"].append(ele[1:])
                        question_eles.append(q_ele)
                    nw = QP_Window(self)
                    nw.question_paper = {"title": "", "subject": "", "max_marks": 0, "questions": question_eles}
                    nw.create_window()
                StringDialog(self, "Question Marks", "Do you want to assign marks to each question? If yes, please enter the marks for each question below. The same marks will be applied to all questions. By default, 1 mark will be assigned.", on_save_marks)

    def sidePanelLeft(self):
        fr_left_content = Frame(self.panedWindow, bg="#d9e7ff", highlightthickness=1, highlightbackground="#000000")
        Button(fr_left_content, text="CREATE QUESTION PAPER", bg="#e8fcd4", fg="green", font=("Helvetica", 14), relief="ridge", command=self.onCreateQPWindow).pack(padx=2, pady=2, fill=X)
        Button(fr_left_content, text="IMPORT QUESTION PAPER", bg="#e8fcd4", fg="green", font=("Helvetica", 14), relief="ridge", command=self.onImportQuestionPaper).pack(padx=2, pady=2, fill=X)
        Button(fr_left_content, text="REGISTER STUDENT", bg="#e8fcd4", fg="green", font=("Helvetica", 14), relief="ridge", command=self.onRegisterStudent).pack(padx=2, pady=2, fill=X)
        Button(fr_left_content, text="RESULTS", bg="#e8fcd4", fg="green", font=("Helvetica", 14), relief="ridge", command=self.onResult).pack(padx=2, pady=2, fill=X)
        fr_left_content.pack(side=LEFT, fill=BOTH, expand=True)
        self.panedWindow.add(fr_left_content)

        fr_right_content = Frame(self.panedWindow, bg="#e0ffcc", highlightthickness=1, highlightbackground="#000000")
        Label(fr_right_content, bg="#87e876", text="Available Question Papers", font=("Bahnschrift", 18)).pack(fill=X)
        self.question_paper_list = QuestionPaperList(fr_right_content)
        self.question_paper_list.pack(fill=BOTH, expand=True)
        fr_right_content.pack(side=LEFT, fill=BOTH, expand=True)
        self.panedWindow.add(fr_right_content)

    def beginGUI(self):
        self.mainloop()


if __name__ == '__main__':
    gui_app = Application()
    #  = PhotoImage(file="assets/pencil_icon_16x16.png")
    gui_app.beginGUI()