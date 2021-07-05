import os
import json
import tkinter as tk
from .subdatapack import SubDatapack
from . import path as _path


def generate(subdatapack: SubDatapack, entries: dict):
    for entry in entries.values():
        if entry.get() == "":
            return
    namespace = subdatapack.namespace
    namespace_path = subdatapack.namespace_path
    subfolder = subdatapack.subfolder_tk.get()
    item_name = entries['item_name'].get().lower().replace(' ','_')
    item_nbt = entries['item_nbt'].get().lower().replace(' ','_')
    if ':' not in item_nbt and item_nbt!="":
        item_nbt+=':1b'

    #---- MAKE PATHS----
    _path.makedirs(namespace_path, 'predicates', subfolder, 'selecteditem')
    _path.makedirs(namespace_path, 'predicates', subfolder, 'utils')
    _path.makedirs(namespace_path, 'advancements', subfolder, 'utils', 'melee_look_at')
    item_function_path = os.path.join(namespace_path, 'functions', subfolder, 'melee_look_at', item_name)
    _path.makedirs(item_function_path)

    # Predicate
    with open(os.path.join(namespace_path, 'predicates', subfolder, 'utils', 'hurt_time.json'), 'w') as hurt_time_json:
        hurt_time_json.write("""
{
    "condition": "minecraft:entity_properties",
    "entity": "this",
    "predicate": {
      "nbt": "{HurtTime:10s}"
    }
}
        """.strip())
    with open(os.path.join(namespace_path, 'predicates', subfolder, 'utils', 'melee_look_at.json'), 'w') as melee_look_at_json:
        melee_look_at_json.write(f"""
{{
    "condition": "minecraft:entity_properties",
    "entity": "this",
    "predicate": {{
        "player": {{
            "looking_at": {{
                "nbt": "{{Tags:['{namespace}.potential_looked']}}"
            }}
        }}
    }}
}}
        """.strip())

    with open(os.path.join(namespace_path, 'predicates', subfolder, 'selecteditem', f'{item_name}.json'), 'w') as selecteditem_file:
        selecteditem_file.write(f"""
{{
    "condition": "minecraft:entity_properties",
    "entity": "this",
    "predicate": {{
      "type": "minecraft:player",
      "equipment": {{
        "mainhand": {{
          "nbt": "{{{item_nbt}}}"
        }}
      }}
    }}
}}
        """.strip())

    # Advancements
    with open(os.path.join(namespace_path, 'advancements', subfolder, 'utils', 'melee_look_at', 'player_hurt_entity.json'), 'w') as player_hurt_entity_json:
        player_hurt_entity_json.write(f"""
{{
    "criteria": {{
        "trigger": {{
            "trigger": "minecraft:player_hurt_entity"
        }}
    }},
    "rewards": {{
        "function": "{namespace}:{subfolder}/melee_look_at/player_hurt_entity"
    }}
}}
        """.strip())

    # Function
    if not os.path.exists(os.path.join(namespace_path, 'functions', subfolder, 'melee_look_at', 'player_hurt_entity.mcfunction')):
        with open(os.path.join(namespace_path, 'functions', subfolder, 'melee_look_at', 'player_hurt_entity.mcfunction'), 'w') as player_hurt_entity_file:
            player_hurt_entity_file.write(f"advancement revoke @s only {namespace}:{subfolder}/utils/melee_look_at/player_hurt_entity")
    with open(os.path.join(namespace_path, 'functions', subfolder, 'melee_look_at', 'player_hurt_entity.mcfunction'), 'a') as player_hurt_entity_file:
        player_hurt_entity_file.write('\n'+f"execute if entity @s[predicate={namespace}:{subfolder}/selecteditem/{item_name}] at @s anchored eyes run function {namespace}:{subfolder}/melee_look_at/{item_name}/init")  
    
    # Look At function
    with open(os.path.join(item_function_path, 'init.mcfunction'), 'w') as init_file:
        init_file.write(f"""
tag @s add {namespace}.looker
execute as @e[distance=..6,tag=!{namespace}.looker] at @s run function {namespace}:{subfolder}/melee_look_at/{item_name}/look
tag @s remove {namespace}.looker
execute as @e[distance=..6,tag={namespace}.looked,limit=1,sort=nearest] at @s run function {namespace}:{subfolder}/melee_look_at/{item_name}/exe
""".strip())

    with open(os.path.join(item_function_path, 'look.mcfunction'), 'w') as look_file:
        look_file.write(f"""
tag @s add {namespace}.potential_looked
execute as @p[tag={namespace}.looker] if predicate {namespace}:{subfolder}/utils/melee_look_at run tag @e[limit=1,sort=nearest,tag={namespace}.potential_looked] add {namespace}.looked
tag @s remove {namespace}.potential_looked
""".strip()) 

    with open(os.path.join(item_function_path, 'exe.mcfunction'), 'w') as exe_file:
        exe_file.write('say [PLACE HOLDER]')

    subdatapack.window.clear()
    subdatapack.window.label(f'Melee look_at is successfully generated under {namespace}/{subfolder} with item nbt: "{{{item_nbt}}}."', 16, (20,10))
    subdatapack.pack_main_menu()

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
        item_name_entry = tk.Entry(output_item_frame, width=25)
        item_name_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)

        label = tk.Label(output_item_frame, text="NBT: {" )
        label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        item_nbt_entry = tk.Entry(output_item_frame, width=30)
        item_nbt_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        label = tk.Label(output_item_frame, text="}")
        label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.E)

        entries = {
            'item_name': item_name_entry,
            'item_nbt': item_nbt_entry
        }

        tk.Button(subdatapack.window.root, text="Generate", width=30, font=("", 16), command=lambda: generate(subdatapack, entries)).pack(padx=20, pady=10)
