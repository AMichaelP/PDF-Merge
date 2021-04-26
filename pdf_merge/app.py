from dataclasses import dataclass

from .gui import get_gui


@dataclass
class App:
    gui = get_gui()


def run():
    return App()
