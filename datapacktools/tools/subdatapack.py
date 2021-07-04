import json
import os
import tkinter as tk

class SubDatapack:
    def __init__(self, datapack):
        self.pack_main_menu = datapack.pack_main_menu
        
        self.datapack = datapack
        self.directory = datapack.directory
        self.window = datapack.window
        self.datapack_name = datapack.datapack_name
        self.namespace = datapack.namespace_tk.get()
        self.namespace_path = os.path.join(self.directory, 'data', self.namespace)

    def choose_subfolder(self):
        functions_path = os.path.join(self.directory, 'data', self.namespace, 'functions')
        if not os.path.exists(functions_path):
            os.makedirs(functions_path)
        
        if len(os.listdir(functions_path)) == 0:
            os.makedirs(os.path.join(functions_path, 'my_datapack'))
            
        subfolders = os.listdir(functions_path)
        subfolder_frame = tk.LabelFrame(self.window.root, padx=30, pady=20, text=" Choose subfolder ")
        subfolder_frame.pack(padx=10, pady=10)
        self.subfolder_tk = tk.StringVar(value=subfolders[0])
        for index, folder in enumerate(subfolders):
            tk.Radiobutton(subfolder_frame, text=folder, variable=self.subfolder_tk, value=folder, tristatevalue=0).grid(row=index//2, column=index%2, sticky=tk.W)

    def get_pack_format(self):
        with open(os.path.join(self.directory, 'pack.mcmeta')) as pack_mcmeta:
            return json.load(pack_mcmeta)['pack']['pack_format']