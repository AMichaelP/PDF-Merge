import sys
import tkinter as tk
import tkinter.messagebox as tkm
from ctypes import windll
from dataclasses import dataclass
from tkinter import StringVar, Variable, ttk
from tkinter import filedialog as fd

from PyPDF2 import PdfFileMerger


def input_file_selection_button_callback():
    files = fd.askopenfilenames(filetypes=(("pdf", "*.pdf"), ("txt", "*.txt"), ("*", "*")))
    n = len(files)
    GUI.num_files_selected_text.set(f"{len(files)} file{'s' if n != 1 else ''} Selected")
    GUI.input_files.set(files)
    if n:
        GUI.save_as_button.configure(state="normal")
    else:
        GUI.save_as_button.configure(state="disabled")


def output_file_callback():
    of = fd.asksaveasfile(initialfile="combined.pdf", filetypes=(("pdf", "*.pdf"),), mode="wb")
    files = GUI.input_files.get()
    try:
        if of and files:
            pdf_merger = PdfFileMerger()
            for f in files:
                if f.endswith(".pdf"):
                    pdf_merger.append(f)
            pdf_merger.write(of)
            tkm.showinfo("", message="Done!")
    except Exception as e:
        tkm.showerror(e)
        sys.exit(1)
    finally:
        sys.exit(0)


@dataclass
class GUI:
    PADDING = {
        "padx": 10,
        "pady": 10,
    }

    WINDOW_SIZE = {
        "width": 300,
        "height": 50,
    }

    window = tk.Tk()
    window.wm_minsize(**WINDOW_SIZE)
    window.resizable(False, False)
    window.title("PDF Merge")

    input_files = Variable(master=window, value=None, name="INPUT_FILES")
    num_files_selected_text = StringVar(master=window, value="0 files selected")

    file_input_frame = ttk.Frame(master=window)
    ttk.Label(text="Select Input Files:", master=file_input_frame).grid(row=0, column=0,
                                                                        **PADDING)
    num_files_selected_label = ttk.Label(textvariable=num_files_selected_text, master=file_input_frame)

    save_as_button = ttk.Button(text="Save As...".center(25), master=file_input_frame, state="disabled",
                                command=output_file_callback)

    def __post_init__(self):
        ttk.Button(text="Browse...".center(25), master=self.file_input_frame,
                   command=input_file_selection_button_callback).grid(
            row=0, column=1,
            **self.PADDING
        )

        self.num_files_selected_label.grid(row=1, column=0, **self.PADDING)

        self.save_as_button.grid(
            row=1, column=1,
            **self.PADDING
        )

        self.file_input_frame.pack()
        self.window.mainloop()


def get_gui() -> GUI:
    windll.shcore.SetProcessDpiAwareness(1)
    return GUI()
