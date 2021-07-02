import tkinter as tk
from typing import Tuple, List, Dict
from . import utils

class Window():
    def __init__(self, title: str, ico_path: str) -> None:
        self.root = tk.Tk()
        self.root.title(title)
        self.root.iconbitmap(ico_path)

    def clear(self) -> None:
        for item in self.root.winfo_children():
            item.pack_forget()
            item.grid_forget()

    def label(self, text: str, font_size: int = 8, pad: Tuple[int]=(15,10)) -> None:
        tk.Label(self.root, text=text, font=("", font_size)).pack(padx=pad[0], pady=pad[1])

    def input_frame(self, frame_text: str, pad: Tuple[int], entries_list: List[str], rows: int=1, entry_width: int=30) -> Dict[str,tk.Entry]:
        frame = tk.LabelFrame(self.root, padx=pad[0], pady=pad[0], text=f" {frame_text} ")
        frame.pack(padx=10, pady=10)

        entries = dict()

        for index, entry in enumerate(entries_list):
            row = index//rows
            column = 2*index%rows

            label = tk.Label(frame, text=f"{entry}: ")
            label.grid(row=row, column=column, padx=5, pady=5, sticky=tk.E)
            tk_entry = tk.Entry(frame, width=entry_width)
            tk_entry.grid(row=row, column=column+1, padx=5, pady=5)

            entries[entry] = tk_entry

        return entries

    def checkbutton_frame(self, frame_text: str, pad: Tuple[int], buttons_map: Dict[str, str], rows: int=1) -> Dict[str,tk.Checkbutton]:
        frame = tk.LabelFrame(self.root, padx=pad[0], pady=pad[0], text=f" {frame_text} ")
        frame.pack(padx=10, pady=10)

        buttons = dict()

        for index, (button_display, button) in enumerate(buttons_map.items()):
            row = index//rows
            column = index%rows

            label = tk.Label(frame, text=f"{button}: ")
            label.grid(row=row, column=column, padx=5, pady=5)
            checkbutton_bool = tk.BooleanVar()
            tk.Checkbutton(frame, text=button_display, variable=checkbutton_bool).grid(row=row, column=column, padx=7, pady=5, sticky=tk.W)


            buttons[button] = checkbutton_bool

        return buttons



    