import os
import json
import tkinter as tk
from .subdatapack import SubDatapack
from . import path as _path


def generate(subdatapack: SubDatapack, entries: dict):
    pass



class MeleeLookAt:

    def melee_look_at(self):
        self.window.clear()
        self.window.label("Melee look_at", font_size=18, pad=(10,10))
        self.pack_main_menu()
        
        subdatapack = SubDatapack(self)
        if subdatapack.get_pack_format() < 7:
            self.window.label("look_at predicate only works on 1.17 or higher!", font_size=16, pad=(10,5))
            return

        subdatapack.choose_subfolder()

        output_item_frame = tk.LabelFrame(subdatapack.window.root, padx=20, pady=10, text="Output Item")
        output_item_frame.pack(padx=20, pady=10)

        label = tk.Label(output_item_frame, text="Item's name: ")
        label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        item_id_field = tk.Entry(output_item_frame, width=25)
        item_id_field.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)

        label = tk.Label(output_item_frame, text="NBT: {" )
        label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        item_nbt_field = tk.Entry(output_item_frame, width=30)
        item_nbt_field.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        label = tk.Label(output_item_frame, text="}")
        label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.E)

        entries = {
            'item_id': item_id_field,
            'item_nbt': item_nbt_field
        }

        tk.Button(subdatapack.window.root, text="Generate", width=30, font=("", 16), command=lambda: generate(subdatapack, entries)).pack(padx=20, pady=10)