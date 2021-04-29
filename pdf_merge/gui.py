import io
import tkinter as tk
from dataclasses import dataclass, asdict
from tkinter import filedialog as fd
from typing import Iterable, Union, NewType

DialogAllowedFileTypes = NewType("DialogAllowedFileTypes", Iterable[tuple[str, Union[str, Iterable[str]]]])

ALLOWED_INPUT_TYPES: DialogAllowedFileTypes = ("pdf", (".pdf",)), (
    "pdf", ".pdf"), ("txt", ".txt"), ("", "*")
INPUT_FILES_DIALOG_TITLE: str = "Select the Files to Merge"

SAVE_AS_ALLOWED_TYPES: DialogAllowedFileTypes = ("pdf", ".pdf"),
SAVE_AS_DIALOG_TITLE: str = "Save As..."
SAVE_AS_DEFAULT_FILE_NAME: str = "combined.pdf"


@dataclass
class DialogParams:
    filetypes: Iterable[tuple[str, str]] = None
    title: str = None
    initialfile: str = None

    def as_dict(self):
        return asdict(self)


@dataclass
class GUI:
    input_params: DialogParams
    save_as_params: DialogParams

    def ask_get_input_file_paths(self) -> tuple[str]:
        return fd.askopenfilenames(multiple=True, **self.input_params.as_dict())

    def ask_get_output_file_text_buffer(self) -> io.TextIOWrapper:
        return fd.asksaveasfile(**self.save_as_params.as_dict())

    @classmethod
    def _hide_root_window(cls):
        tk.Tk().withdraw()

    def __post_init__(self):
        self._hide_root_window()


def get_gui() -> GUI:
    input_params = DialogParams(ALLOWED_INPUT_TYPES, INPUT_FILES_DIALOG_TITLE)
    output_params = DialogParams(SAVE_AS_ALLOWED_TYPES, SAVE_AS_DIALOG_TITLE, SAVE_AS_DEFAULT_FILE_NAME)
    return GUI(input_params, output_params)
