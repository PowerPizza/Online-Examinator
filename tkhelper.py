from tkinter import *
from tkinter.constants import *
from PIL import Image as PIL_Image
from PIL import ImageTk

class ScrollableFrame(Frame):
    def __init__(self, master, v_scroll=True, h_scroll=True, **kwargs):
        main_frame = Frame(master, **kwargs)
        self.main_frame = main_frame

        fr_left_divison = Frame(main_frame)
        children_canvas = Canvas(fr_left_divison, bg=main_frame["bg"], bd=0)
        children_canvas.pack(fill=BOTH, expand=True)
        self.children_canvas = children_canvas
        super().__init__(master=children_canvas)

        hr_scroll = Scrollbar(fr_left_divison, orient=HORIZONTAL, command=children_canvas.xview)
        hr_scroll.pack(fill=X, side=BOTTOM)
        fr_left_divison.pack(fill=BOTH, expand=True, side=LEFT)

        vr_scroll = Scrollbar(main_frame, orient=VERTICAL, command=children_canvas.yview)
        vr_scroll.pack(side=RIGHT, fill=Y)
        
        children_canvas.configure(yscrollcommand=vr_scroll.set, xscrollcommand=hr_scroll.set)
        
        self.bind("<Configure>", lambda e: children_canvas.configure(scrollregion=children_canvas.bbox("all")))
        def on_load_canvas(e):
            children_canvas.configure(scrollregion=children_canvas.bbox("all"))
            self.children_canvas.itemconfig(drawn_frame, width=e.width-4)
        # children_canvas.bind("<Configure>", lambda e: children_canvas.configure(scrollregion=children_canvas.bbox("all")))
        children_canvas.bind("<Configure>", on_load_canvas)
        drawn_frame = children_canvas.create_window((0, 0), window=self, anchor=NW)

    def pack(self, **kwargs):
        self.main_frame.pack(**kwargs)

    def config(self, **kwargs):
        self.children_canvas.config(**kwargs)
        for item in kwargs:
            self[item] = kwargs[item]


class TkIcon(ImageTk.PhotoImage):
    # __photo = None
    def __init__(self, icon_path, size=(32, 32)):
        self.img = PIL_Image.open(icon_path)
        self.img = self.img.resize(size, PIL_Image.LANCZOS)
        super().__init__(self.img)
    
            # self.__photo = ImageTk.PhotoImage(self.img)

class StringDialog(Toplevel):
    string_val = None
    submit_command = lambda val: val
    close_at_submission = None
    label_prompt = None

    def __init__(self, master, window_title, prompt_label, submit_command, btn_text="submit", close_at_submission=True):
        super().__init__(master)
        self.string_val = StringVar(self, value="")
        self.submit_command = submit_command
        self.close_at_submission = close_at_submission

        self.title(window_title)
        self.geometry(f"350x250+{self.winfo_screenwidth()//2 - 350//2}+{self.winfo_screenheight()//2 - 180}")
        self.transient(master)
        self.config(bg="#fffff2")
        self.resizable(False, False)

        self.update()
        self.label_prompt = Label(self, text=prompt_label, font=("Helvetica", 14), bg="#fffff2", fg="blue", wraplength=self.winfo_width())
        self.label_prompt.pack(anchor=NW, padx=5, pady=5)
        input_ = Entry(self, textvariable=self.string_val, width=50, font=("Helvetica", 12), highlightthickness=2, highlightbackground="#292929")
        input_.pack(padx=15, pady=5, ipady=5)
        input_.focus_set()

        submit_btn = Button(self, text=btn_text, font=("Helvetica", 14), bg="#e4ffd9", fg="green", activebackground="#e4ffd9", activeforeground="green", command=self.__onSubmit)
        submit_btn.pack(ipadx=25)

        self.mainloop()

    def __onSubmit(self):
        self.submit_command(self.string_val.get())
        if self.close_at_submission:
            self.close()

    def getValue(self):
        return self.string_val.get()

    def close(self):
        self.destroy()

if __name__ == '__main__':
    from tkinter import *


    root = Tk()
    root.geometry("500x600")
    root.title("WINDOW")
    im = TkIcon("assets/play_icon.png", (40, 40))


    Button(root, text="PLAY", image=im).pack()
    Button(root, text="PLAY", image=im).pack()
    Button(root, text="PLAY", image=im).pack()

    fr2 = Frame(root)
    scf = ScrollableFrame(fr2, bg="green")
    scf.config(bg="yellow")

    for x in range(100):
        Label(scf, text=f"HELLO, THERE ITS PYTHON And its a very popular programming language {x+1}", font=("Helvetica", 18), bg="red", anchor=NW, justify=LEFT).pack(padx=13, pady=2, fill=X)
    scf.pack(fill=BOTH, expand=TRUE, padx=20)
    fr2.pack(pady=20, fill=X)

    def on_clc():
        Label(scf, text=f"New Label", font=("Helvetica", 18), bg="red", anchor=NW, justify=LEFT).pack(padx=13, pady=2, fill=X)
    Button(root, text="ADD", command=on_clc).pack()

    root.mainloop()