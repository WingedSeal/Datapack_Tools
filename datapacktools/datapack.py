import tkinter as tk
import os
from typing import Dict

from . import utils
from . import _init
from . import tools
from .window import Window

class Datapack:
    def __init__(self, directory: str, datapack_name: str, window: Window) -> None:
        self.directory = directory
        self.window = window
        self.datapack_name = datapack_name

    def init(self) -> None:
        self.window.label("Generate empty datapack",22)
        entries = self.window.input_frame(
            frame_text=self.datapack_name,
            pad = (50,30),
            entries_list=[
                'pack_format',
                'description',
                'Namespace',
                'Subfolder'
            ]
        )
        options = self.window.checkbutton_frame(
            frame_text="Options",
            pad = (50,20),
            buttons_map={
                'Shulkerbox Manipulation loot_table': 'shulkerbox_manip_loot_table',
                'Undead entity_type tag': 'undead_entity_tag',
                'Transparent block entity_types': 'transparent_block_tag',
                'Entity that have baby form entity_type tag': 'baby_form_entity_tag',
                'Plants block tag': 'plants_block_tag'
            },
            rows=2
        )
        
        tk.Button(self.window.root, text="Generate",command=lambda: self._init_generate(entries, options)).pack(padx=20, pady=10)

    def _init_generate(self, entries: Dict[str, tk.Entry], options: Dict[str, tk.Checkbutton]) -> None:
        namespace = entries['Namespace'].get().lower().strip().replace(" ", "_")
        if namespace == "":
            namespace = "namespace"
        self.namespace = namespace
        self.namespace_path = os.path.join(self.directory, 'data', self.namespace)

        subfolder = entries['Subfolder'].get().lower().strip().replace(" ", "_")
        if subfolder == "":
            subfolder = "my_datapack"
        self.subfolder = subfolder

        pack_format = entries['pack_format'].get()
        if pack_format == "":
            pack_format = "7"
        self.pack_format = pack_format

        self.description = entries['description'].get()

        _init.generate_paths(self)
        _init.generate_pack_mcmeta(self)
        _init.generate_tick_load(self)
        _init.generate_optional_files(self, options)

        self.main()

    def main(self) -> None:
        self.window.clear()
        self.window.label(self.datapack_name, 22)

        namespaces = [namespace for namespace in os.listdir(os.path.join(self.directory, 'data')) if namespace != 'minecraft']
        if len(namespaces) == 1:
            self.namespace_tk = tk.StringVar(value=namespaces[0])
        else:
            namespace_frame = tk.LabelFrame(self.window.root, padx=30, pady=20, text=" Choose namespace ")
            namespace_frame.pack(padx=10, pady=10)
            self.namespace_tk = tk.StringVar(value=namespaces[0])
            for index, name in enumerate(namespaces):
                tk.Radiobutton(namespace_frame, text=name, variable=self.namespace_tk, value=name, tristatevalue=0).grid(row=index//2, column=index%2, sticky=tk.W)

        frame = tk.LabelFrame(self.window.root, padx=50, pady=30, text=" Tools ")
        frame.pack(padx=10, pady=10)

        tk.Button(frame, text="Custom Floor Crafting", height=2, width=20, font=("", 12), 
            command=lambda: tools.custom_floor_crafting.main(self)
            ).grid(row=0, column=0, padx=20, pady=10)
        tk.Button(frame, text="Custom Crafting Recipe", height=2, width=20, font=("", 12), 
            command=lambda: tools.custom_crafting_recipe.main(self)
            ).grid(row=0, column=1, padx=20, pady=10)
        tk.Button(frame, text="Melee look_at", height=2, width=20, font=("", 12), 
            command=lambda: tools.melee_look_at.main(self)
            ).grid(row=1, column=0, padx=20, pady=10)
        tk.Button(frame, text="Melee Raycast", height=2, width=20, font=("", 12), 
            command=lambda: tools.melee_raycast.main(self)
            ).grid(row=1, column=1, padx=20, pady=10)

    def pack_main_menu(self) -> None:
        tk.Button(self.window.root, text="Main menu",command=self.main , font=("", 10)).pack(padx=20, pady=10)