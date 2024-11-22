from tkinter import *
from tkinter import messagebox
from application_resources import *
from tkinter.ttk import PanedWindow as ttkPanedWindow
from tkhelper import *
import json
from pandas import DataFrame
from tkinter import filedialog
from bs4 import BeautifulSoup

class ResultViewTab(Canvas):
    results_ = None
    user_list = None
    user_id_lbl = None
    marks_lbl = None
    user_name_lbl = None
    subject_lbl = None
    selected_user = None
    scrollable_fr = None
    fr_question_list = None
    export_result_btn = None
    
    def __init__(self, master, result_file_path):
        super().__init__(master, bg="#dbffd1")
        self.results_ = json.load(open(os.path.join(ApplicationPaths.RESULT_DIR, result_file_path), 'r'))

        main_panedwin = ttkPanedWindow(self, orient=HORIZONTAL)

        fr_user_list = Frame(main_panedwin, bg="#d1ffb3", highlightthickness=1, highlightbackground="blue")
        Label(fr_user_list, text="Users", bg="#d1ffb3", font=("Bahnschrift", 16)).pack()
        self.user_list = Listbox(fr_user_list, bg="#ebffde", highlightthickness=1, highlightbackground="green", font=("Helvetica", 16))
        self.user_list.pack(fill=BOTH, expand=True, padx=1, pady=1)
        self.user_list.bind("<<ListboxSelect>>", self.onSelectUser)
        for item in self.results_["users"]:
            self.user_list.insert(END, item)
        main_panedwin.add(fr_user_list)
        
        fr_answer_sheet = Frame(main_panedwin, bg="#ffffff", highlightthickness=1, highlightbackground="blue")
        Label(fr_answer_sheet, text="Result Answer Sheet", bg="#ffbfa6", font=("Calibri", 18)).pack(fill=X)
        self.scrollable_fr = ScrollableFrame(fr_answer_sheet, bg="white")
        self.scrollable_fr.config(bg="#ffffff")
        Label(self.scrollable_fr, text=result_file_path[:-5], bg="#FFFFFF", font=("Russo One", 18)).pack()
        
        fr_primary_info = Frame(self.scrollable_fr, bg="#faf9f5", highlightthickness=1, highlightbackground="#bababa")
        fr_pinfo_row_1 = Frame(fr_primary_info, bg="#faf9f5")
        self.user_id_lbl = Label(fr_pinfo_row_1, text="User ID : ", bg="#faf9f5", font=("Russo One", 14), fg="#363636")
        self.user_id_lbl.pack(side=LEFT)
        self.marks_lbl = Label(fr_pinfo_row_1, text="Marks : ", bg="#faf9f5", font=("Russo One", 14), fg="#363636")
        self.marks_lbl.pack(side=RIGHT)
        fr_pinfo_row_1.pack(fill=X)

        fr_pinfo_row_2 = Frame(fr_primary_info, bg="#faf9f5")
        self.user_name_lbl = Label(fr_primary_info, text="User Name : ", bg="#faf9f5", font=("Russo One", 14), fg="#363636")
        self.user_name_lbl.pack(side=LEFT)
        self.subject_lbl = Label(fr_primary_info, text="Subject : ", bg="#faf9f5", font=("Russo One", 14), fg="#363636")
        self.subject_lbl.pack(side=RIGHT)
        fr_pinfo_row_2.pack(fill=X)
        fr_primary_info.pack(fill=X, padx=2, pady=2)

        self.fr_question_list = Frame(self.scrollable_fr, bg='#FFFFFF')
        self.fr_question_list.pack(fill=BOTH, expand=True)
        
        self.scrollable_fr.pack(fill=BOTH, expand=True)
        main_panedwin.add(fr_answer_sheet, weight=1)

        fr_side_options = Frame(main_panedwin, bg="#bae5ff", highlightthickness=1, highlightbackground="blue")
        self.export_result_btn = Button(fr_side_options, text="Export Result", font=("Helvetica", 16), relief=GROOVE, command=self.onExportResult)
        self.export_result_btn.pack(padx=20, pady=5, ipadx=20, fill=X)
        Button(fr_side_options, text="Save Answer Sheet", font=("Helvetica", 16), relief=GROOVE, command=self.onSaveAnswerSheet).pack(padx=20, pady=5, ipadx=20, fill=X)
        Button(fr_side_options, text="Close", font=("Helvetica", 16), relief=GROOVE, command=self.destroy).pack(padx=20, pady=5, ipadx=20, fill=X)
        main_panedwin.add(fr_side_options)

        main_panedwin.pack(fill=BOTH, expand=True)
        self.place(relx=0, rely=0, relwidth=1, relheight=1)

    def onSelectUser(self, eve):
        self.selected_user = self.user_list.get(ANCHOR)
        user_creds = self.results_["users"][self.selected_user]['creds']
        qp_metadata = self.results_["qp_metadata"]
        self.user_id_lbl.config(text=f"User ID : {user_creds['uid']}")
        self.user_name_lbl.config(text=f"User Name : {user_creds['u_name']}")
        self.subject_lbl.config(text=f"Subject : {qp_metadata['subject']}")
        self.marks_lbl.config(text=f"Marks : {self.getMoreResultInfo(user_creds['uid'])['scored_marks']}/{qp_metadata["max_marks"]}")
        self.loadResult()
    
    def getMoreResultInfo(self, user_id):
        """
        This function gives correct questions done by user and total marks they got.
        return : dict
        """
        to_ret = {"scored_marks": 0, "correct_ans": 0}
        answers_ = dict(self.results_["users"][user_id])
        del answers_["creds"]
        for qno in answers_:
            if answers_[qno]["value"] in self.results_["question_paper"]["questions"][int(qno)]["correct_opts"]:
                to_ret["scored_marks"] += self.results_["question_paper"]["questions"][int(qno)]["max_marks"]
                to_ret["correct_ans"] += 1
            else:
                pass # IF NEGATIVE MARKING FUNCTIONALITY ADDED SO CODE WILL COME HERE!!
        return to_ret

    def loadResult(self):
        [child.destroy() for child in self.fr_question_list.winfo_children()]
        for q_idx, question_item in enumerate(self.results_["question_paper"]["questions"]):
            corrospond_ans = self.results_["users"][self.selected_user].get(f"{q_idx}")
            if corrospond_ans:
                corrospond_ans = corrospond_ans["value"]
            
            layout_color = "#f5d3b8"  # RED
            layout_border = "#ff2f00"  # RED
            if corrospond_ans in question_item["correct_opts"]:
                layout_color = "#c1f5b8"  # GREEN
                layout_border = "#00a100"  # GREEN
            elif corrospond_ans is None:
                layout_color = "#f3f5b8"  # YELLOWISH 
                layout_border = "#ffbf00"  # YELLOWISH 
            
            fr_question_ele = Frame(self.fr_question_list, bg=layout_color, highlightthickness=2, highlightbackground=layout_border)
            Label(fr_question_ele, text=f"{q_idx+1}) {question_item['question']} ({question_item['max_marks']})", bg=layout_color, font=("Helvetica", 16)).pack(anchor=NW)
            for opt_ in question_item["options"]:
                if opt_ == corrospond_ans and corrospond_ans not in question_item["correct_opts"]:
                    Label(fr_question_ele, text=opt_, font=("Helvetica", 16), bg=layout_color, fg="red").pack(anchor=NW, padx=15)
                elif opt_ in question_item["correct_opts"] and corrospond_ans is not None:
                    Label(fr_question_ele, text=opt_, font=("Helvetica", 16), bg=layout_color, fg="green").pack(anchor=NW, padx=15)
                else:
                    Label(fr_question_ele, text=opt_, font=("Helvetica", 16), bg=layout_color, fg="black").pack(anchor=NW, padx=15)
            fr_question_ele.pack(fill=X, padx=1, pady=1)

    def onExportResult(self):
        users_ = json.load(open(ApplicationPaths.USER_CREDENTIALS_FILE, 'r'))
        result_df = DataFrame(columns=["User ID", "User Name", "Subject", "Scored Marks", "Max Marks", "Correct", "Incorrect", "Total Questions"])
        for user_id in self.results_["users"]:
            result_info = self.getMoreResultInfo(user_id)
            result_df.loc[len(result_df)] = [
                user_id, users_[user_id]["u_name"],
                self.results_["qp_metadata"]["subject"],
                result_info['scored_marks'],
                self.results_["qp_metadata"]["max_marks"],
                result_info['correct_ans'],
                self.results_["qp_metadata"]["no_of_questions"]-result_info['correct_ans'],
                self.results_["qp_metadata"]["no_of_questions"]
            ]
        file_ = filedialog.asksaveasfile(title="Exporting result", filetypes=[("CSV File", "*.csv"), ("Excel File", "*.xlsx"), ("Json File (unstable)", "*.json")], defaultextension="csv")
        self.export_result_btn.config(text="Exporting Result...", state="disabled")
        self.update()
        if file_:
            if file_.name.endswith(".csv"):
                result_df.to_csv(file_.name, index=False, lineterminator="\n")
            elif file_.name.endswith(".xlsx"):
                result_df.to_excel(file_.name, "Result", index=False)
            elif file_.name.endswith(".json"):
                result_df.to_json(file_.name)
            messagebox.showinfo("File Saved", f"Result saved successfully at `{file_.name}`")
        self.export_result_btn.config(text="Export Result", state="normal")

    def onSaveAnswerSheet(self):
        if not self.selected_user:
            messagebox.showwarning("No user selected", "Please select the user whose result you want to save.")
            return
        to_print = BeautifulSoup(open(PrintingLayoutPaths.RESULT_LAYOUT, "r"), 'html.parser')
        to_print.find("h2", {"class": "exam_h"}).string = self.results_["qp_metadata"]["title"]
        to_print.find("span", {"class": "uid"}).string += self.selected_user
        to_print.find("span", {"class": "marks"}).string += f"{self.getMoreResultInfo(self.selected_user)['scored_marks']}/{self.results_['qp_metadata']['max_marks']}"
        to_print.find("span", {"class": "uname"}).string += self.results_["users"][self.selected_user]['creds']["u_name"]
        to_print.find("span", {"class": "sub"}).string += self.results_["qp_metadata"]["subject"]
        for q_idx, question_item in enumerate(self.results_["question_paper"]["questions"]):
            corrospond_ans = self.results_["users"][self.selected_user].get(f"{q_idx}")
            if corrospond_ans:
                corrospond_ans = corrospond_ans["value"]
            
            layout_color = "#f5d3b8"  # RED
            layout_border = "#ff2f00"  # RED
            if corrospond_ans in question_item["correct_opts"]:
                layout_color = "#c1f5b8"  # GREEN
                layout_border = "#00a100"  # GREEN
            elif corrospond_ans is None:
                layout_color = "#f3f5b8"  # YELLOWISH 
                layout_border = "#ffbf00"  # YELLOWISH

            question_bx = to_print.new_tag("div", attrs={"class": "question_box", "style": f"background-color: {layout_color}; border-color: {layout_border};"})
            span_ele1 = to_print.new_tag("span", attrs={"class": "question"})
            span_ele1.string = f"{q_idx+1}) {question_item['question']} ({question_item['max_marks']})"
            question_bx.append(span_ele1)

            for opt_ in question_item["options"]:
                if opt_ == corrospond_ans and corrospond_ans not in question_item["correct_opts"]:
                    span_ele2 = to_print.new_tag("span", attrs={"class": "opt", "style": "color: red;"})
                    span_ele2.string = opt_
                elif opt_ in question_item["correct_opts"] and corrospond_ans is not None:
                    span_ele2 = to_print.new_tag("span", attrs={"class": "opt", "style": "color: green;"})
                    span_ele2.string = opt_
                else:
                    span_ele2 = to_print.new_tag("span", attrs={"class": "opt", "style": "color: black;"})
                    span_ele2.string = opt_
                question_bx.append(span_ele2)
            to_print.find("div", attrs={"class": "main_body"}).append(question_bx)
        
        file_ = filedialog.asksaveasfile(title="Saving result", filetypes=[("HTML files", "*.html")], defaultextension="html")
        if file_:
            with open(file_.name, "w") as fp:
                fp.write(to_print.prettify())
            messagebox.showinfo("Saved", f"Result has been saved at {file_.name}")


class ResultWindow(Toplevel):
    main_canvas = None
    close_win_btn = None
    table_view = None
    __eye_icon = None
    __delete_icon = None

    def __init__(self, master):
        super().__init__(master)
        self.__eye_icon = TkIcon(IconPaths.EYE_OPEN_ICON)
        self.__delete_icon = TkIcon(IconPaths.DELETE_ICON)

        self.title("Results")
        self.geometry("500x400")
        self.state("zoomed")
        self.main_canvas = Canvas(self, bg="#dbffd1")
        fr_top_header = Frame(self.main_canvas, bg="#c9ffba", highlightthickness=1, highlightbackground="green")
        self.close_win_btn = Button(fr_top_header, text="close", bg="#ff473c", activebackground="#ff473c", relief=GROOVE, fg="white", activeforeground="white", font=("Courier", 16, "bold"), command=self.destroy)
        self.close_win_btn.pack(side=LEFT, padx=2, pady=2)
        fr_top_header.pack(fill=X, padx=1, pady=1)

        self.table_view = ScrollableFrame(self.main_canvas, bg="#dbffd1")
        self.table_view.config(bg="#dbffd1")
        self.__load_results()
        self.table_view.pack(fill=BOTH, expand=True)
        self.main_canvas.pack(fill=BOTH, expand=True)

    def __load_results(self):
        [child.destroy() for child in self.table_view.winfo_children()]
        def make_row(title_):
            fr_row = Frame(self.table_view, bg="#b8ecff", highlightthickness=1, highlightbackground="blue")
            lb_title = Label(fr_row, text=title_[:-5], bg="#b8ecff", font=("Helvetica", 18))
            lb_title.pack(side=LEFT, ipadx=10)
            def on_delete():
                if messagebox.askyesno("Deleting result", "Result will be deleted permanently, Do you want to delete ?"):
                    os.remove(os.path.join(ApplicationPaths.RESULT_DIR, title_))
                    self.__load_results()
            Button(fr_row, image=self.__delete_icon, bg="#f26f90", relief=GROOVE, command=on_delete).pack(side=RIGHT, padx=1, pady=1)
            def on_show_result():
                ResultViewTab(self, result_file_path=title_)

            Button(fr_row, image=self.__eye_icon, bg="#fffcb3", relief=GROOVE, command=on_show_result).pack(side=RIGHT, padx=1, pady=1)
            def change_row_color(color):
                fr_row.config(bg=color)
                lb_title.config(bg=color)
            fr_row.bind("<Enter>", lambda eve: change_row_color("#6ea9f0"))
            fr_row.bind("<Leave>", lambda eve: change_row_color("#b8ecff"))
            fr_row.pack(fill=X, pady=1)

        for item in os.listdir(ApplicationPaths.RESULT_DIR):
            make_row(item)

if __name__ == "__main__":
    root = Tk()
    root.iconify()
    r_win = ResultWindow(root)
    root.mainloop()