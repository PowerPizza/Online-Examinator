from tkinter import *
from tkinter import messagebox
from application_resources import *
from tkinter.ttk import Button as ttkButton
from tkinter.ttk import Style, Combobox
from tkhelper import *
from uuid import uuid4
import json

class BasicQuestionForm(Frame):
    question_label = None
    question_entry = None
    option_listbox = None
    correct_opt_list = None
    mm_value = None
    def __init__(self, master):
        super().__init__(master=master)
        self.config(bg="#fff3de", highlightthickness=1, highlightbackground="#000000")

        fr_question_row = Frame(self, bg="#fff3de", highlightthickness=1, highlightbackground="#000000")
        lbl_question_ = Label(fr_question_row, text=f"Question", font=("Helvetica", 18), bg="#fff3de")
        lbl_question_.pack(padx=20, side=LEFT)
        self.question_label = lbl_question_
        self.question_entry = Text(fr_question_row, font=("Helvetica", 12), height=4, width=50, border=0, highlightthickness=1, highlightbackground="#000000")
        self.question_entry.pack(side=LEFT, fill=X, expand=True, padx=2, pady=2)
        fr_question_row.pack(fill=X)

        btn_style = Style(self)
        btn_style.configure("optAS.TButton", font=("Helvetica", 14), width=2)

        fr_option_box = Frame(self, bg="#fff3de")
        fr_options = Frame(fr_option_box, bg="#fff3de", highlightthickness=1, highlightbackground="#000000")
        scroll_bar_hr = Scrollbar(fr_options, orient=HORIZONTAL)
        scroll_bar_hr.grid(row=2, column=0, sticky=NSEW, columnspan=3)
        scroll_bar_vr = Scrollbar(fr_options, orient=VERTICAL)
        scroll_bar_vr.grid(row=1, column=3, sticky=NSEW, rowspan=3)
        
        Label(fr_options, text="Selectable Options", font=("Helvetica", 14), bg="#fff3de").grid(row=0, column=0)
        ttkButton(fr_options, text="+", style="optAS.TButton", command=self.__onAddOption).grid(row=0, column=1)
        ttkButton(fr_options, text="-", style="optAS.TButton", command=self.__onRemoveOption).grid(row=0, column=2)
        self.option_listbox = Listbox(fr_options, font=("Helvetica", 14), highlightthickness=1, highlightbackground="#525252", yscrollcommand=scroll_bar_vr.set, xscrollcommand=scroll_bar_hr.set)
        self.option_listbox.grid(row=1, column=0, columnspan=3, sticky=NSEW)
        scroll_bar_hr.config(command=self.option_listbox.xview)
        scroll_bar_vr.config(command=self.option_listbox.yview)
        fr_options.pack(side=LEFT, pady=2, anchor=NW, padx=2)

        fr_transverse_btns = Frame(fr_option_box, bg="#fff3de")
        ttkButton(fr_transverse_btns, text="⮝", style="optAS.TButton", command=self.__onMoveOptUp).pack()
        ttkButton(fr_transverse_btns, text="⮟", style="optAS.TButton", command=self.__onMoveOptDown).pack()

        Frame(fr_transverse_btns).pack(pady=10)  # JUST FOR GAPING

        ttkButton(fr_transverse_btns, text="⮞", style="optAS.TButton", command=self.__onMakeOptCorrect).pack()
        fr_transverse_btns.pack(side=LEFT, padx=2, pady=2)
        
        Frame(fr_option_box).pack(padx=30, side=LEFT)

        fr_options_correct = Frame(fr_option_box, bg="#fff3de", highlightthickness=1, highlightbackground="#000000")
        Label(fr_options_correct, text="Correct Options", font=("Helvetica", 14), bg="#fff3de").grid(row=0, column=0, padx=40)
        scroll_bar_hr = Scrollbar(fr_options_correct, orient=HORIZONTAL)
        scroll_bar_hr.grid(row=2, column=0, sticky=NSEW, columnspan=3)
        scroll_bar_vr = Scrollbar(fr_options_correct, orient=VERTICAL)
        scroll_bar_vr.grid(row=1, column=3, sticky=NSEW, rowspan=3)

        self.correct_opt_list = Listbox(fr_options_correct, font=("Helvetica", 14), highlightthickness=1, highlightbackground="#525252", yscrollcommand=scroll_bar_vr.set, xscrollcommand=scroll_bar_hr.set)
        self.correct_opt_list.grid(row=1, column=0, columnspan=3, sticky=NSEW)
        scroll_bar_hr.config(command=self.correct_opt_list.xview)
        scroll_bar_vr.config(command=self.correct_opt_list.yview)
        fr_options_correct.pack(side=LEFT, pady=2, anchor=NW, padx=2)

        fr_transverse_btns2 = Frame(fr_option_box, bg="#fff3de")
        ttkButton(fr_transverse_btns2, text="✖", style="optAS.TButton", command=self.__onMakeOptDiscorrect).pack()
        fr_transverse_btns2.pack(side=LEFT, padx=2, pady=2)
        
        fr_max_marks = Frame(fr_option_box, bg="#fff3de", highlightthickness=1, highlightbackground="blue")
        Label(fr_max_marks, text="Max Marks : ", font=("Helvetica", 14, "italic", "underline"), bg="#fff3de").pack(side=LEFT)
        self.mm_value  = IntVar(self, value=5)
        entry_max_marks = Entry(fr_max_marks, font=("Helveitca", 14), textvariable=self.mm_value , width=4, highlightthickness=1, highlightbackground="blue")
        entry_max_marks.pack(side=LEFT, ipady=5, ipadx=10, padx=1, pady=1)
        fr_max_marks.pack(side=RIGHT, anchor=NE, padx=4, pady=4)
        fr_option_box.pack(fill=X)

        self.pack(side=LEFT, fill=BOTH, expand=True, padx=2, pady=2)
    
    def __onAddOption(self):
        def add_option_(option_):
            if option_ not in self.option_listbox.get(0, END) and len(option_):
                self.option_listbox.insert(END, option_)
        StringDialog(self, window_title="Add Option", prompt_label="Option", btn_text="add +", submit_command=add_option_)

    def __onRemoveOption(self):
        if len(self.option_listbox.curselection()):
            cur_selected_idx = self.option_listbox.curselection()[0]

            if self.option_listbox.get(cur_selected_idx) in self.correct_opt_list.get(0, END):
                to_del = list(self.correct_opt_list.get(0, END)).index(self.option_listbox.get(cur_selected_idx))
                self.correct_opt_list.delete(to_del)

            self.option_listbox.delete(cur_selected_idx)
            self.option_listbox.select_set(0)

    def __onMoveOptUp(self):
        cur_selection_idx = self.option_listbox.curselection()[0]
        if cur_selection_idx <= 0:
            return
        prev_selection_val = self.option_listbox.get(cur_selection_idx-1)
        cur_selection_val = self.option_listbox.get(cur_selection_idx)
        self.option_listbox.delete(cur_selection_idx-1, cur_selection_idx)
        self.option_listbox.insert(cur_selection_idx-1, cur_selection_val, prev_selection_val)
        self.option_listbox.select_set(cur_selection_idx-1)

    def __onMoveOptDown(self):
        cur_selection_idx = self.option_listbox.curselection()[0]
        if not len(self.option_listbox.get(cur_selection_idx+1)):
            return
        cur_selection_val = self.option_listbox.get(cur_selection_idx)  # get(ANCHOR) can't be used due to it causes BUG in up down
        next_selection_val = self.option_listbox.get(cur_selection_idx+1)
        self.option_listbox.delete(cur_selection_idx, cur_selection_idx+1)
        self.option_listbox.insert(cur_selection_idx, next_selection_val, cur_selection_val)
        self.option_listbox.select_set(cur_selection_idx+1)
    
    def __onMakeOptCorrect(self):
        if len(self.option_listbox.curselection()) and self.option_listbox.get(self.option_listbox.curselection()[0]) not in self.correct_opt_list.get(0, END):
            self.correct_opt_list.insert(END, self.option_listbox.get(self.option_listbox.curselection()[0]))
    
    def __onMakeOptDiscorrect(self):
        if len(self.correct_opt_list.curselection()):
            self.correct_opt_list.delete(self.correct_opt_list.curselection()[0])
            self.correct_opt_list.select_set(0)

    def clear_form(self):
        self.question_entry.delete("1.0", END)
        self.option_listbox.delete(0, END)
        self.correct_opt_list.delete(0, END)
        self.mm_value.set(5)

    def get_form_data(self):
        return {
            "question": self.question_entry.get("1.0", END)[:-1],
            "options": list(self.option_listbox.get(0, END)),
            "correct_opts": list(self.correct_opt_list.get(0, END)),
            "max_marks": self.mm_value.get()
        }
    
    def set_form_data(self, question, options, correct_opts, max_marks):
        self.clear_form()
        self.question_entry.insert(END, question)
        self.option_listbox.insert(END, *options)
        self.correct_opt_list.insert(END, *correct_opts)
        self.mm_value.set(max_marks)

class QuestionListItem(Frame):
    update_btn = None
    delete_btn = None
    __pencil_icon = None
    def __init__(self, master, question_, options, correct_options, **kwargs):
        super().__init__(master=master, **kwargs)
        fr_curd = Frame(self, bg="#ffffff")
        self.__pencil_icon = TkIcon(IconPaths.PENCIL_ICON, (16, 16))
        self.update_btn = Button(fr_curd, image=self.__pencil_icon, relief=RIDGE, bg="#c9c7ff")
        self.update_btn.pack(side=LEFT, padx=2, pady=2, fill=Y, ipadx=4)
        self.delete_btn = Button(fr_curd, text="X", relief=RIDGE, bg="#c9c7ff", font=("Helvetica", 12))
        self.delete_btn.pack(side=LEFT, padx=2, pady=2, fill=Y, ipadx=4)
        fr_curd.pack(anchor=NW)
        Label(self, text=question_, font=("Calibri", 16), anchor=NW, bg=self['bg'], justify=LEFT, wraplength=500).pack(fill=X, padx=20)
        for idx, opt in enumerate(options):
            if opt in correct_options:
                Label(self, text=f"{idx+1}) {opt}", font=("Bahnschrift", 14), anchor=NW, bg=self['bg'], fg="green").pack(fill=X, padx=40)
            else:
                Label(self, text=f"{idx+1}) {opt}", font=("Bahnschrift", 14), anchor=NW, bg=self['bg']).pack(fill=X, padx=40)

class QuestionList(Frame):
    questions_index = 0
    def __init__(self, master, q_list, on_update, on_delete):
        super().__init__(master=master, bg="#fffede")
        self.q_list = q_list
        self.on_update = on_update
        self.on_delete = on_delete
        self.reload()
        self.pack(padx=2, pady=2, fill=X, expand=True)
    
    def reload(self):
        self.questions_index = 0
        [child.destroy() for child in self.winfo_children()]
        for idx, question in enumerate(self.q_list):
            qd1 = QuestionListItem(self, f"{idx+1}) {question['question']} ━ [{question['max_marks']}]", question["options"], question["correct_opts"], bg="#fffede", highlightthickness=1, highlightbackground="black")
            qd1.pack(fill=X, padx=2, pady=2)
            def set_update_command():
                q_copy = question
                q_idx_cpy = idx
                qd1.update_btn.config(command=lambda : self.on_update(q_idx_cpy, q_copy))
            set_update_command()
            def set_delete_command():
                idx_cpy = idx
                qd1.delete_btn.config(command=lambda : self.on_delete(idx_cpy))
            set_delete_command()
            self.questions_index += 1  # BINDALL NOT WORKING PROPERLY...

    def refresh(self):
        """
        Call only if new question element is added to question_paper["questions"]
        """
        question = self.q_list[self.questions_index]
        qd1 = QuestionListItem(self, f"{self.questions_index+1}) {question['question']} ━ [{question['max_marks']}]", question["options"], question["correct_opts"], bg="#fffede", highlightthickness=1, highlightbackground="black")
        qd1.pack(fill=X, padx=2, pady=2)
        def set_ctrl_command():
            idx_cpy = self.questions_index
            qd1.delete_btn.config(command=lambda : self.on_delete(idx_cpy))
            qd1.update_btn.config(command=lambda : self.on_update(idx_cpy, question))
        set_ctrl_command()
        self.questions_index += 1

class QP_Window(Toplevel):
    question_paper = None
    questions_list_area = None
    qp_id = None
    updation_win = None
    max_marks_lbl = None
    no_of_questions_lbl = None
    qp_title = None
    qp_subject = None
    basic_qp_form = None

    btn_save_qp = None
    app_instance = None

    def __init__(self, master):
        super().__init__(master)
        master.withdraw()
        self.qp_id = str(uuid4()).replace("-", "")
        self.qp_title = StringVar(self)
        self.qp_subject = StringVar(self, value="Select Subject")
        self.question_paper = {"title": self.qp_title.get(), "subject": self.qp_subject.get(), "max_marks": 0, "questions": []}
        
        self.title("Create Question Paper")
        self.geometry("700x500")
        self.state("zoomed")
        self.app_instance = master

        def on_close_win():
            master.deiconify()
            master.state("zoomed")
            self.destroy()
        self.protocol("WM_DELETE_WINDOW", on_close_win)
    def create_window(self):
        main_qp_canvas = PanedWindow(self, bg="#ffffff", orient=HORIZONTAL)
        self.basic_qp_form = BasicQuestionForm(main_qp_canvas)
        self.basic_qp_form.question_label.config(text=f"Question {len(self.question_paper['questions'])+1}")

        self.basic_qp_form_btns = Frame(self.basic_qp_form, bg="#fffede")
        btn_add_question = Button(self.basic_qp_form_btns, text="ADD +", bg="#05b41c", fg="white", activebackground="#05b41c", activeforeground="white", relief=RIDGE, font=("Russo One", 18), width=10, command=self.onAddQuestion)
        btn_add_question.pack(side=RIGHT, pady=5, padx=5)
        btn_clear_form = Button(self.basic_qp_form_btns, text="CLEAR", bg="#ff4136", fg="white", activebackground="#ff4136", activeforeground="white", relief=RIDGE, font=("Russo One", 18), width=10, command=self.basic_qp_form.clear_form)
        btn_clear_form.pack(side=RIGHT, pady=5, padx=5)
        self.basic_qp_form_btns.pack(anchor=NE, pady=5, padx=5)

        main_qp_canvas.add(self.basic_qp_form)

        fr_qp_configs = Frame(main_qp_canvas, bg="#fffede", highlightthickness=1, highlightbackground="#000000")
        fr_title_config = Frame(fr_qp_configs, bg="#fffede", highlightthickness=1, highlightbackground='black')
        Label(fr_title_config, text="Title", bg="#fffede", font=("Helvetica", 18)).pack(side=LEFT, padx=3)
        paper_title_entry = Entry(fr_title_config, textvariable=self.qp_title, font=('Helvetica', 14), highlightthickness=1, highlightbackground="black")
        paper_title_entry.pack(side=LEFT, fill=X, expand=True, padx=2)
        fr_title_config.pack(padx=2, pady=2, fill=X)

        fr_mm = Frame(fr_qp_configs, bg="#fffede", highlightthickness=1, highlightbackground="black")
        self.max_marks_lbl = Label(fr_mm, font=("Calibri", 18, "bold"), bg="#fffede")
        self.max_marks_lbl.pack(side=LEFT)
        fr_mm.pack(padx=2, pady=2, fill=X)

        fr_subject_config = Frame(fr_qp_configs, bg="#fffede", highlightthickness=1, highlightbackground="black")
        lbl_subject = Label(fr_subject_config, text=f"Subject", font=("Helvetica", 18), anchor=NW, bg="#fffede")
        lbl_subject.pack(side=LEFT, padx=3)
        subject_list = json.load(open(JsonFiles.SUBJECT_CODE_REFERENCE, "r"))
        subject_select = Combobox(fr_subject_config, values=list(map(lambda code: subject_list[code]["Name"], subject_list)), textvariable=self.qp_subject, font=("Calibri", 16))
        subject_select.pack(side=LEFT, padx=2, pady=2)
        fr_subject_config.pack(padx=2, pady=2, fill=X)

        fr_no_of_questions = Frame(fr_qp_configs, bg="#fffede", highlightthickness=1, highlightbackground="black")
        self.no_of_questions_lbl = Label(fr_no_of_questions, font=("Calibri", 18, "bold"), bg="#fffede")
        self.no_of_questions_lbl.pack(side=LEFT)
        fr_no_of_questions.pack(padx=2, pady=2, fill=X)

        fr_question_display = Frame(fr_qp_configs, bg="#fffede", highlightthickness=1, highlightbackground="#000000")
        fr_scrollable = ScrollableFrame(fr_question_display, bg="#fffede")
        fr_scrollable.config(bg="#fffede")
        fr_scrollable.pack(fill=BOTH, expand=True)
        fr_question_display.pack(padx=2, pady=2, fill=BOTH, expand=True)

        self.questions_list_area = QuestionList(fr_scrollable, self.question_paper["questions"], self.__onUpdate, self.__onDeleteQuestion)
        """
        DIRECTLY PASSING REFERENCE OF LIST INTO FUNCTION CAUSES REFRESH METHOD OF CLASS QUESTIONLIST WORK PROPERLY
        """
        
        self.btn_save_qp = Button(fr_qp_configs, text="SAVE", bg="#269f42", fg="white", activebackground="#269f42", activeforeground="white", relief=RIDGE, font=("Russo One", 18), width=8, command=self.on_save_qp)
        self.btn_save_qp.pack(side=BOTTOM, anchor=SE, pady=5, padx=5, ipadx=10)
        
        fr_qp_configs.pack(side=LEFT)
        self.__update_information()
        main_qp_canvas.add(fr_qp_configs)

        main_qp_canvas.pack(fill=BOTH, expand=True)
    
    def onAddQuestion(self):
        to_save = self.basic_qp_form.get_form_data()
        self.question_paper["questions"].append(to_save)
        self.questions_list_area.refresh()
        self.__update_information()

    def on_save_qp(self):
        self.question_paper["title"] = self.qp_title.get()
        self.question_paper["subject"] = self.qp_subject.get()
        if not len(self.question_paper["title"]):
            messagebox.showwarning("Saving failed", "Title is invalid please enter a valid title.")
            return
        if not len(self.question_paper["subject"]):
            messagebox.showwarning("Saving failed", "Subject is invalid please enter a valid subject.")
            return
        try:
            json.dump(self.question_paper, open(f"{ApplicationPaths.QUESTION_PAPER_DIR}\\{self.qp_id}.qp", "w"))
            self.app_instance.question_paper_list.loadPapers()
            messagebox.showinfo("Saved", "Question paper saved")
        except BaseException as e:
            messagebox.showerror("Saving failed", f"Saving failed due to error.\n{e}")

    def __onUpdate(self, q_no, to_update):
        if self.updation_win:
            self.updation_win.destroy()
            self.updation_win = None

        updation_win = Toplevel(self)
        self.updation_win = updation_win
        updation_win.title("Update")
        updation_win.transient(self)
        updation_win.attributes("-topmost", True)
        updation_win.resizable(False, False)
        updation_win.geometry(f"900x450+{updation_win.winfo_screenwidth()//2 - 900//2}+{updation_win.winfo_screenheight()//2 - 300}")

        fr_update_form = BasicQuestionForm(updation_win)
        fr_update_form.question_label.config(text=f"Question {q_no+1}")
        fr_update_form.set_form_data(*to_update.values())

        fr_update_form_btns = Frame(fr_update_form, bg="#fffede")
        def on_commit_update():
            new_form_data = fr_update_form.get_form_data()
            for key_ in to_update:
                to_update[key_] = new_form_data[key_]
            self.questions_list_area.reload()
            self.__update_information()
            on_close()
        btn_update_question = Button(fr_update_form, text="UPDATE ⬆", bg="#05b41c", fg="white", activebackground="#05b41c", activeforeground="white", relief=RIDGE, font=("Russo One", 18), width=10, command=on_commit_update)
        btn_update_question.pack(side=RIGHT, pady=5, padx=5)
        def on_close():
            updation_win.destroy()
        updation_win.protocol("WM_DELETE_WINDOW", on_close)
        btn_cancle_update = Button(fr_update_form, text="CANCLE", bg="#ff4136", fg="white", activebackground="#ff4136", activeforeground="white", relief=RIDGE, font=("Russo One", 18), width=10, command=on_close)
        btn_cancle_update.pack(side=RIGHT, pady=5, padx=5)
        
        fr_update_form_btns.pack(anchor=NE, pady=5, padx=5)
        updation_win.mainloop()

    def __onDeleteQuestion(self, index):
        if messagebox.askyesno("Deleting Question", "Do you really want to delete this question?"):
            self.question_paper["questions"].pop(index)
            self.questions_list_area.reload()
            self.__update_information()
    
    def __calculate_qp_maxMarks(self):
        self.question_paper["max_marks"] = sum([question["max_marks"] for question in self.question_paper["questions"]])
        return self.question_paper["max_marks"]
    
    def __update_information(self):
        self.max_marks_lbl.config(text=f"Max Marks : {self.__calculate_qp_maxMarks()}")
        self.no_of_questions_lbl.config(text=f"Questions : {len(self.question_paper['questions'])}")
        self.basic_qp_form.question_label.config(text=f"Question {len(self.question_paper['questions'])+1}")