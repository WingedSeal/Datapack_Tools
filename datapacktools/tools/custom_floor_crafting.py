import os
import json
import tkinter as tk
from .subdatapack import SubDatapack
from . import path as _path

def entity_selector(item: dict, limit: bool):
    tag = f'tag:{{{item["nbt"]}}}' if item["nbt"]!="" else ""
    if limit:
        return f'@e[type=item,nbt={{Item:{{id:"minecraft:{item["id"]}",Count:{item["count"]}b,{tag}}}}},limit=1,distance=..1]'
    else: 
        return f'@e[type=item,nbt={{Item:{{id:"minecraft:{item["id"]}",Count:{item["count"]}b,{tag}}}}}]'

def is_tick_valid(values: list, namespace: str, subfolder: str):
    for value in values:
        if len(value.split(':')[1].split('/')) == 2 and (value.split(':')[0], value.split(':')[1].split('/')[0], value.split(':')[1].split('/')[1]) == (namespace, subfolder, 'tick'):
            return True
    return False


def generate(subdatapack: SubDatapack, entries: dict) -> None:
    subfolder = subdatapack.subfolder_tk.get()
    namespace = subdatapack.namespace
    namespace_path = subdatapack.namespace_path 
    output_item_name = entries['item_name'].get()
    
    recipes = []
    for item in subdatapack.items_data:
        id = item['id'].get().lower().replace(' ','_')
        nbt = item['nbt'].get().lower().replace(' ','_')
        if ':' not in nbt and nbt!="":
            nbt+=':1b'
        count = item['count'].get()
        recipes.append({
            'id': id,
            'nbt': nbt,
            'count': count
        })
    # Make tick.mcfunction valid
    tick_json_path = (os.path.join(subdatapack.directory, 'data', 'minecraft', 'tags', 'functions'))

    _path.makedirs(tick_json_path)
    with open(os.path.join(tick_json_path, 'tick.json'), 'r+') as tick_json_file:
        tick_json = json.loads(tick_json_file.read())
        if not is_tick_valid(tick_json['values'], namespace, subfolder):
            tick_json['values'].append(f'{namespace}:{subfolder}/tick')
            print(tick_json)
            tick_json_file.write(json.dumps(tick_json, indent=2))

    # Add floor_recipe to tick.mcfunction
    _path.makedirs(namespace_path, 'functions', subfolder, 'floor_recipe')
    with open(os.path.join(namespace_path, 'functions', subfolder, 'tick.mcfunction'), 'r') as tick_file:
        tick_function = tick_file.read()
    with open(os.path.join(namespace_path, 'functions', subfolder, 'tick.mcfunction'), 'a') as tick_file:
        tick_command = f'function {namespace}:{subfolder}/floor_recipe/tick'
        if not tick_command in tick_function:
            if tick_function == '':
                tick_file.write('\n'+tick_command)
            else:
                tick_file.write(tick_command)  

    # Add recipe to floor_recipe/tick.mcfunction
    with open(os.path.join(namespace_path, 'functions', subfolder, 'floor_recipe', 'tick.mcfunction'), 'a') as recipe_tick_file:
        tick_command = f'execute as {entity_selector(recipes[0], False)} at @s'
        for item in recipes[1:]:
            tick_command += f' if entity {entity_selector(item, True)}'
        tick_command += f" run function {namespace}:{subfolder}/floor_recipe/{output_item_name}"
        recipe_tick_file.write('\n'+tick_command)

    # item_name.mcfunction
    with open(os.path.join(namespace_path, 'functions', subfolder, 'floor_recipe', f'{output_item_name}.mcfunction'), 'w') as item_mcfunction:
        item_mcfunction.write('kill @s'+'\n')
        for item in recipes[1:]:
            item_mcfunction.write(f'kill {entity_selector(item, True)}'+'\n')
        item_mcfunction.write('say [PLACEHOLDER]')

    # Add floor_recipe to tick.mcfunction
    _path.makedirs(namespace_path, 'functions', subfolder, 'floor_recipe')
    with open(os.path.join(namespace_path, 'functions', subfolder, 'tick.mcfunction'), 'r') as tick_file:
        tick_function = tick_file.read()
    with open(os.path.join(namespace_path, 'functions', subfolder, 'tick.mcfunction'), 'a') as tick_file:
        tick_command = f'function {namespace}:{subfolder}/floor_recipe/tick'
        if not tick_command in tick_function:
            if tick_function == '':
                tick_file.write('\n'+tick_command)
            else:
                tick_file.write(tick_command)

    subdatapack.window.clear()
    subdatapack.window.label("Custom floor crafting is successfully generated.", 16, (20,10))
    subdatapack.pack_main_menu()
    

def input_recipes(subdatapack: SubDatapack, entries: dict) -> None:
    subdatapack.recipes_frame.pack_forget()
    subdatapack.recipes_frame = tk.LabelFrame(subdatapack.window.root, padx=20, pady=10, text="Recipes")
    subdatapack.recipes_frame.pack(padx=10, pady=10)

    try:
        amount_of_type = int(entries['amount_of_type'].get())
    except:
        amount_of_type = 2

    items_data = []
    
    for n in range(amount_of_type):
        row = n//3
        column = n%3
        recipe_frame = tk.LabelFrame(subdatapack.recipes_frame, padx=10, pady=5, text=f"Item {n+1}")
        recipe_frame.grid(row=row, column=column, padx=10, pady=10)

        label = tk.Label(recipe_frame, text="Item's id: ")
        label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        item_id_field = tk.Entry(recipe_frame, width=25)
        item_id_field.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)

        label = tk.Label(recipe_frame, text="NBT: {" )
        label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        item_nbt_field = tk.Entry(recipe_frame, width=30)
        item_nbt_field.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        label = tk.Label(recipe_frame, text="}")
        label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.E)

        label = tk.Label(recipe_frame, text="Count: ")
        label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        item_count_field = tk.Entry(recipe_frame, width=15)
        item_count_field.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        items_data.append({
            'id': item_id_field,
            'nbt': item_nbt_field,
            'count': item_count_field
        })

    subdatapack.items_data = items_data

    tk.Button(subdatapack.recipes_frame, text="Generate", width=30, font=("", 16), command=lambda: generate(subdatapack, entries)).grid(row=amount_of_type*3, column=0, columnspan=3, padx=10, pady=10)



class CustomFloorCrafting:

    def custom_floor_crafting(self) -> None:
        self.window.clear()
        self.window.label("Custom Floor Crafting", font_size=18, pad=(10,10))
        self.pack_main_menu()

        subdatapack = SubDatapack(self)
        subdatapack.choose_subfolder()

        output_item_frame = tk.LabelFrame(subdatapack.window.root, padx=50, pady=20, text=f" Output item ")
        output_item_frame.pack(padx=10, pady=10)

        tk.Label(output_item_frame, text="Item's name: ").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        item_name_entry = tk.Entry(output_item_frame, width=30)
        item_name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(output_item_frame, text="Amount of type of item in the recipe: ").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        type_entry = tk.Entry(output_item_frame, width=30)
        type_entry.grid(row=2, column=1, padx=5, pady=5)

        subdatapack.recipes_frame = tk.LabelFrame(subdatapack.window.root, padx=20, pady=10, text="Recipes")
        entries = {
            'amount_of_type': type_entry,
            'item_name': item_name_entry
        }

        tk.Button(subdatapack.window.root, text="Input recipes", command=lambda: input_recipes(subdatapack, entries)).pack(padx=20, pady=10)