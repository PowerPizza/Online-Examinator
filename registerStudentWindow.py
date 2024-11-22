from tkinter import *
from tkinter.ttk import Treeview, Style
import json
from application_resources import *
from tkinter import messagebox
from pandas import read_csv, read_excel, DataFrame
from tkinter import filedialog
from tkhelper import StringDialog

class AddStudentWindow(Toplevel):
    u_id_val = None
    u_name_val = None
    u_pass_val = None
    register_btn = None
    title_header = None
    reloadTableData = None  # FUNCTION HELPS IN RELOADING TABLE ALONG WITH NEW DATA -> OBJECT ASSIGNS IT
    entry_s_id = None
    entry_s_name = None
    entry_s_password = None
    def __init__(self, master):
        super().__init__(master)
        self.title("Add Students")
        self.transient(master)
        self.resizable(False, False)
        self.geometry(f"400x210+{master.winfo_screenwidth()//2 - 400//2}+{master.winfo_screenheight()//2 - 250}")
        self.update()
        
        fr_header = Frame(self)
        self.title_header = Label(fr_header, text="Add Student", font=("Bahnschrift", 18))
        self.title_header.pack(fill=X)
        fr_header.grid(row=0, column=0, columnspan=2, sticky=NSEW, ipady=7)
        Label(self, text="USER ID", font=('Calibri', 16), justify=LEFT, anchor=NW).grid(row=1, column=0, ipadx=5, sticky=NSEW)
        self.u_id_val = StringVar()
        self.entry_s_id = Entry(self, font=('Calibri', 16), textvariable=self.u_id_val)
        self.entry_s_id.grid(row=1, column=1)

        Label(self, text="USER NAME", font=('Calibri', 16), justify=LEFT, anchor=NW).grid(row=2, column=0, ipadx=5, sticky=NSEW)
        self.u_name_val = StringVar()
        self.entry_s_name = Entry(self, font=('Calibri', 16), textvariable=self.u_name_val)
        self.entry_s_name.grid(row=2, column=1)

        Label(self, text="USER PASSWORD", font=('Calibri', 16), justify=LEFT, anchor=NW).grid(row=3, column=0, ipadx=5, sticky=NSEW)
        self.u_pass_val = StringVar()
        self.entry_s_password = Entry(self, font=('Calibri', 16), textvariable=self.u_pass_val)
        self.entry_s_password.grid(row=3, column=1)

        self.register_btn = Button(self, text="Register", bg="#45a448", activebackground="#45a448", fg="white", activeforeground="white", relief="groove", font=("Russo One", 16), command=self.on_clc_register)
        self.register_btn.grid(row=4, column=0, columnspan=2, pady=7)

    def on_clc_register(self):
        with open(ApplicationPaths.USER_CREDENTIALS_FILE, 'r') as fp:
            old_data = json.load(fp)
            if self.u_id_val.get() in old_data:
                messagebox.showerror("Failed", f"Entry with `user id : {self.u_id_val.get()}` already exists!")
                return
            old_data[self.u_id_val.get()] = {"u_name": self.u_name_val.get(), "password": self.u_pass_val.get()}
        with open(ApplicationPaths.USER_CREDENTIALS_FILE, 'w') as fp:
            json.dump(old_data, fp)
        if callable(self.reloadTableData): self.reloadTableData()
        messagebox.showinfo("Entry Added", "New user entry added to database.")


class ModifyStudentWindow(AddStudentWindow):
    def __init__(self, master):
        super().__init__(master)
        self.title("Modify Student")
        self.title_header.config(text="Modify Student")
        self.register_btn.config(text="Commit", bg="#ffedde", activebackground="#ffedde", fg="#ff7700", activeforeground="#ff7700", command=self.on_commit_changes)
        self.entry_s_id.config(state="disabled")

    def on_commit_changes(self):
        with open(ApplicationPaths.USER_CREDENTIALS_FILE, 'r') as fp:
            old_data = json.load(fp)
            old_data[self.u_id_val.get()] = {"u_name": self.u_name_val.get(), "password": self.u_pass_val.get()}
        with open(ApplicationPaths.USER_CREDENTIALS_FILE, 'w') as fp:
            json.dump(old_data, fp)
        if callable(self.reloadTableData): self.reloadTableData()
        messagebox.showinfo("Updated", "Entry updated successfully")

class DuplicateEntryPrompt(Frame):
    new_uid_var = None
    message_label = None
    def __init__(self, master):
        super().__init__(master, bg="#FFFFFF")
        self.message_label = Label(self, text="", font=("Bahnschrift", 16), wraplength=480, bg="#ffffff")
        self.message_label.pack(pady=4)
        self.new_uid_var = StringVar()
        self.new_u_id_entry = Entry(self, textvariable=self.new_uid_var, font=("Bahnschrift", 16), highlightthickness=1, highlightbackground="#000000")
        self.new_u_id_entry.pack()
        self.skip_this_btn = Button(self, text="Skip this entry", font=("Bahnschrift", 14), relief=GROOVE, bg="#e8faff", activebackground="#e8faff", fg="blue")
        self.skip_this_btn.pack(fill=X, padx=20, pady=1, side=BOTTOM)
        self.overwrite_btn = Button(self, text="Overwrite existing user", font=("Bahnschrift", 14), relief=GROOVE, bg="#fde8ff", activebackground="#fde8ff", fg="magenta")
        self.overwrite_btn.pack(fill=X, padx=20, pady=1, side=BOTTOM)
        self.skip_all_btn = Button(self, text="Skip all duplicacies", font=("Bahnschrift", 14), relief=GROOVE, bg="#ffeae8", activebackground="#ffeae8", fg="red")
        self.skip_all_btn.pack(fill=X, padx=20, pady=1, side=BOTTOM)
        self.proceed_btn = Button(self, text="Proceed", font=("Bahnschrift", 14), relief=GROOVE, bg="#f0ffe8", activebackground="#f0ffe8", fg="green")
        self.proceed_btn.pack(fill=X, padx=20, pady=1, side=BOTTOM)
        

class RegisterStudentWin(Toplevel):
    main_canvas = None
    table_view = None

    def __init__(self, master):
        super().__init__(master)
        self.title("Register Student")
        self.geometry("500x400")
        self.state("zoomed")
        self.main_canvas = Canvas(self, bg="#FFFFFF")

        fr_table_ = Frame(self.main_canvas, bg="#FFFFFF", highlightthickness=1, highlightbackground="black")
        self.table_view = Treeview(fr_table_, columns=("u_id", "u_name", "password", ""))
        s1 = Style()
        s1.configure("Treeview.Heading", font=("Roboto", 16))
        s1.configure("Treeview", font=("Bahnschrift", 16), rowheight=35)
        self.table_view.column("#0", anchor=CENTER)
        self.table_view.column("u_id", anchor=CENTER)
        self.table_view.column("u_name", anchor=CENTER)
        self.table_view.column("password", anchor=CENTER)
        self.table_view.heading("#0", text="S. NO.")
        self.table_view.heading("u_id", text="User ID")
        self.table_view.heading("u_name", text="User Name")
        self.table_view.heading("password", text="Password")
        self.reloadTableData()
        self.table_view.pack(fill=BOTH, expand=True, side=LEFT)
        scroll_bar_y = Scrollbar(fr_table_, command=self.table_view.yview)
        scroll_bar_y.pack(side=RIGHT, fill=Y)
        self.table_view.config(yscrollcommand=scroll_bar_y.set)
        fr_table_.pack(fill=BOTH, expand=True, side=LEFT)

        fr_controls_ = Frame(self.main_canvas, bg="#FFFFFF", highlightthickness=1, highlightbackground="black")
        btn_add_student = Button(fr_controls_, text="ADD ➕", width=15, bg="#edffe0", activebackground="#edffe0", relief="ridge", fg="green", activeforeground="green", font=("Bahnschrift", 16), command=self.onAddStudent)
        btn_add_student.pack(ipadx=20, fill=X, padx=2, pady=2)

        btn_update_student = Button(fr_controls_, text="MODIFY ⚙️", bg="#fff2d6", activebackground="#fff2d6", relief="ridge", fg="#ff6d05", activeforeground="#ff6d05", font=("Bahnschrift", 16), command=self.onModifyStudent)
        btn_update_student.pack(ipadx=20, fill=X, padx=2, pady=2)

        btn_delete_student = Button(fr_controls_, text="DELETE ⛌", bg="#ffded6", activebackground="#ffded6", relief="ridge", fg="red", activeforeground="red", font=("Bahnschrift", 16), command=self.onDeleteStudent)
        btn_delete_student.pack(ipadx=20, fill=X, padx=2, pady=2)

        btn_import_student = Button(fr_controls_, text="IMPORT 📥", bg="#cffaff", activebackground="#cffaff", relief="ridge", fg="#00bcd1", activeforeground="#00bcd1", font=("Bahnschrift", 16), command=self.onImportStudents)
        btn_import_student.pack(ipadx=20, fill=X, padx=2, pady=2)
        fr_controls_.pack(fill=Y, side=RIGHT)

        self.main_canvas.pack(fill=BOTH, expand=True)
    
    def reloadTableData(self):
        with open(ApplicationPaths.USER_CREDENTIALS_FILE, 'r') as fp:
            users = json.load(fp)
        [self.table_view.delete(item) for item in self.table_view.get_children()]
        for idx, user_id in enumerate(users):
            self.table_view.insert("", END, text=f"{idx+1}", values=[user_id] + list(users[user_id].values()))
        
    def onAddStudent(self):
        add_std_win = AddStudentWindow(self)
        add_std_win.reloadTableData = self.reloadTableData

    def onModifyStudent(self):
        try:
            update_selection = self.table_view.item(self.table_view.selection()[0], "values")
        except IndexError:
            messagebox.showwarning("No selection", "Please select an entry to update from the table.")
            return
        modify_std_win = ModifyStudentWindow(self)
        modify_std_win.u_id_val.set(update_selection[0])
        modify_std_win.u_name_val.set(update_selection[1])
        modify_std_win.u_pass_val.set(update_selection[2])
        modify_std_win.reloadTableData = self.reloadTableData

    def onDeleteStudent(self):
        try:
            delete_selection = self.table_view.item(self.table_view.selection()[0], "values")
        except IndexError:
            messagebox.showwarning("No selection", "Please select an entry to delete from the table.")
            return
        if messagebox.askyesno("Delete", f"Are you sure you want to delete the entry with User ID {delete_selection[0]}?"):
            with open(ApplicationPaths.USER_CREDENTIALS_FILE, 'r') as fp:
                old_data = json.load(fp)
                del old_data[delete_selection[0]]
            with open(ApplicationPaths.USER_CREDENTIALS_FILE, 'w') as fp:
                json.dump(old_data, fp)
            self.reloadTableData()
    
    def onImportStudents(self):
        file_ = filedialog.askopenfilename(title="Import users from", filetypes=[("Excel Files", "*.xlsx"), ("CSV Files", "*.csv")], defaultextension=".csv")
        if file_:
            users_ = DataFrame()
            if file_.endswith(".csv"):
                users_ = read_csv(file_, dtype=str)
            elif file_.endswith(".xlsx"):
                users_ = read_excel(file_, dtype=str)
            if len(users_.columns) < 2:
                messagebox.showerror("Columns didn't match", "There should be 2 columns atleast in selected file, please provide a valid file.")
                return

            import_proc_win = Toplevel(self)
            import_proc_win.title("Column Mapping")
            import_proc_win.transient(self)
            import_proc_win.geometry(f"500x300+{self.winfo_screenwidth()//2 - 500//2}+{self.winfo_screenheight()//2 - 200}")
            Label(import_proc_win, text="File Column Mapping", bg="#fff1c7", fg="blue", font=("Russo One", 18), highlightthickness=1, highlightbackground="blue").pack(fill=X)
            fr_mapping = Frame(import_proc_win, bg="#fffbf0", highlightthickness=1, highlightbackground="blue")
            Label(fr_mapping, text="COLUMNS", font=("Calibri", 18), bg="#ffd8bf").grid(row=0, column=0, ipadx=20, sticky=NSEW)
            Label(fr_mapping, text="MAPPING WITH", font=("Calibri", 18), bg="#ffd8bf").grid(row=0, column=1, ipadx=20, sticky=NSEW)

            df_valid_col_vars = {
                "user_id": StringVar(value=users_.columns[0]),
                "u_name": StringVar(value=users_.columns[1]),
                "password": StringVar(value=users_.columns[2])
            }
            Label(fr_mapping, text="User ID", font=("Calibri", 16), bg="#ffd8bf").grid(row=1, column=0, sticky=NSEW)
            col_list_1 = OptionMenu(fr_mapping, df_valid_col_vars["user_id"], *users_.columns)
            col_list_1.config(font=("Calibri", 16), bg="#fffbf0")
            col_list_1.grid(row=1, column=1, sticky=NSEW)

            Label(fr_mapping, text="User Name", font=("Calibri", 16), bg="#ffd8bf").grid(row=2, column=0, sticky=NSEW)
            col_list_2 = OptionMenu(fr_mapping, df_valid_col_vars["u_name"], *users_.columns)
            col_list_2.config(font=("Calibri", 16), bg="#fffbf0")
            col_list_2.grid(row=2, column=1, sticky=NSEW)

            Label(fr_mapping, text="Password", font=("Calibri", 16), bg="#ffd8bf").grid(row=3, column=0, sticky=NSEW)
            col_list_3 = OptionMenu(fr_mapping, df_valid_col_vars["password"], *users_.columns)
            col_list_3.config(font=("Calibri", 16), bg="#fffbf0")
            col_list_3.grid(row=3, column=1, sticky=NSEW)
            fr_mapping.pack(fill=BOTH, expand=True)
            
            def on_import_now():
                with open(ApplicationPaths.USER_CREDENTIALS_FILE, 'r') as fp:
                    old_data = json.load(fp)
                
                skip_all = False
                def write_user(indexer):
                    if indexer < 0:
                        with open(ApplicationPaths.USER_CREDENTIALS_FILE, 'w') as fp:
                            json.dump(old_data, fp)
                        self.reloadTableData()
                        messagebox.showinfo("Import successful", "Users data has been imported successfully.")
                        return
                    row_ = users_.index[indexer]
                    u_id_ = str(users_.loc[row_, df_valid_col_vars["user_id"].get()])
                    u_name_ = str(users_.loc[row_, df_valid_col_vars["u_name"].get()])
                    password_ = str(users_.loc[row_, df_valid_col_vars["password"].get()])
                    if u_id_ in old_data and not skip_all:
                        dupe_tab = DuplicateEntryPrompt(import_proc_win)
                        dupe_tab.message_label.config(text=f"Duplicate user ID `{u_id_}` detected. Please provide a unique ID or choose to skip this user entry during the import process.")
                        dupe_tab.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)
                        def on_proceed():
                            new_uid_ = dupe_tab.new_uid_var.get()
                            if new_uid_ and new_uid_ not in old_data:
                                old_data[new_uid_] = {"u_name": u_name_, "password": password_}
                                dupe_tab.destroy()
                                write_user(indexer-1)
                            elif not len(new_uid_):
                                messagebox.showerror("Entry required", "New user ID is required to proceed, please provide it.")
                            else:
                                messagebox.showerror("Already exist", "can't proceed with this user ID, already exists.")
                        dupe_tab.proceed_btn.config(command=on_proceed)
                        def on_skip_this():
                            dupe_tab.destroy()
                            write_user(indexer-1)
                        dupe_tab.skip_this_btn.config(command=on_skip_this)
                        def on_skip_all():
                            nonlocal skip_all
                            skip_all = True
                            dupe_tab.destroy()
                            write_user(indexer-1)
                        dupe_tab.skip_all_btn.config(command=on_skip_all)
                        def on_overwrite():
                            old_data[u_id_] = {"u_name": u_name_, "password": password_}
                            dupe_tab.destroy()
                            write_user(indexer-1)
                        dupe_tab.overwrite_btn.config(command=on_overwrite)
                    elif u_id_ in old_data and skip_all:
                        write_user(indexer-1)
                    else:
                        old_data[u_id_] = {"u_name": u_name_, "password": password_}
                        write_user(indexer-1)
                write_user(len(users_.index)-1)

            btn_import = Button(import_proc_win, text="Import Now!", font=("Russo One", 16), bg="#b0ebff", relief=GROOVE, fg="#00a1d6", command=on_import_now)
            btn_import.pack(fill=X, padx=4, pady=2)

    def show(self):
        self.mainloop()

if __name__ == '__main__':
    root = Tk()
    s = RegisterStudentWin(root)
    root.mainloop()