import os
import sys
from pathlib import Path
from tkinter.messagebox import showerror, showinfo
from typing import Iterable

from PyPDF4 import PdfFileMerger
from PyPDF4.utils import PdfReadError, PdfReadWarning

from pdf_merge.gui import get_gui, GUI


def run():
    gui = get_gui()
    merger = _prompt_and_get_merged_input_files(gui)
    output_path = _prompt_get_output_path(gui)
    _write_merged_pdf(merger, output_path)
    os.startfile(output_path.as_posix())
    sys.exit(0)


def _get_merger_from_paths(paths=Iterable[Path]) -> PdfFileMerger:
    merger = PdfFileMerger()
    for p in paths:
        with p.open(mode="rb") as fo:
            try:
                merger.append(fo)
            except PdfReadError:
                showerror("Error Reading PDF File", f"Unable to read PDF file:\n{fo.name}")
    if not merger.pages:
        showerror("No Files Selected", "No files were selected.")
        sys.exit(0)
    return merger


def _prompt_get_output_path(gui: GUI) -> Path:
    if not (p := gui.ask_get_output_file_text_buffer()):
        showinfo("No Output Path Selected", "No output path was selected.\nCanceling merge.")
        sys.exit(0)
    return Path(p.name)


def _write_merged_pdf(merger: PdfFileMerger, path: Path) -> None:
    with path.open("wb") as fo:
        merger.write(fo)


def _prompt_get_input_files(gui: GUI) -> Iterable[Path]:
    return (Path(p) for p in gui.ask_get_input_file_paths())


def _prompt_and_get_merged_input_files(gui: GUI) -> PdfFileMerger:
    return _get_merger_from_paths(_prompt_get_input_files(gui))
