import os
import tkinter as tk

class SubDatapack:
    def __init__(self, datapack):
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
        if len(subfolders) == 1:
            subfolder = tk.StringVar(value=subfolders[0])
            subfolder_frame = tk.LabelFrame()
        else:
            subfolder_frame = tk.LabelFrame(self.window.root, padx=30, pady=20, text=" Choose subfolder ")
            subfolder_frame.pack(padx=10, pady=10)
            subfolder = tk.StringVar(value=subfolders[0])
            for index, folder in enumerate(subfolders):
                tk.Radiobutton(subfolder_frame, text=folder, variable=subfolder, value=folder, tristatevalue=0).grid(row=index//2, column=index%2, sticky=tk.W)
        self.subfolder = subfolder