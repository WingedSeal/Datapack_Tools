import os
import json
import tkinter as tk
from .subdatapack import SubDatapack
from . import path as _path


def float_range(start, stop, step) -> float:
  while start < stop:
    yield round(float(start),5)
    start += step

def generate(subdatapack: SubDatapack, entries: dict):
    for entry in entries:
        if entry.get() == "":
            return
    namespace = subdatapack.namespace
    namespace_path = subdatapack.namespace_path
    subfolder = subdatapack.subfolder_tk.get()
    item_name = entries['item_name'].get().lower().replace(' ','_')
    item_nbt = entries['item_nbt'].get().lower().replace(' ','_')
    raycast_precision = entries['raycast_precision'].get()
    if ':' not in item_nbt and item_nbt!="":
        item_nbt+=':1b'

    try:
        raycast_precision = float(raycast_precision)
        if raycast_precision <= 0: raise ValueError
    except ValueError:
        raycast_precision = 0.5
    if raycast_precision < 6/(65_536-100):
        raycast_precision = 6/(65_536-100)

    #---- MAKE PATHS----
    _path.makedirs(namespace_path, 'predicates', subfolder, 'selecteditem')
    _path.makedirs(namespace_path, 'predicates', subfolder, 'utils')
    _path.makedirs(namespace_path, 'advancements', subfolder, 'utils', 'melee_raycast')
    _path.makedirs
    _path.makedirs
    _path.makedirs
    item_function_path = os.path.join(namespace_path, 'functions', subfolder, 'melee_raycast', item_name)
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
    with open(os.path.join(namespace_path, 'advancements', subfolder, 'utils', 'melee_raycast', 'player_hurt_entity.json'), 'w') as player_hurt_entity_json:
        player_hurt_entity_json.write(f"""
{{
    "criteria": {{
        "trigger": {{
            "trigger": "minecraft:player_hurt_entity"
        }}
    }},
    "rewards": {{
        "function": "{namespace}:{subfolder}/melee_raycast/player_hurt_entity"
    }}
}}
        """.strip())

    # Function
    if not os.path.exists(os.path.join(namespace_path, 'functions', subfolder, 'melee_raycast', 'player_hurt_entity.mcfunction')):
        with open(os.path.join(namespace_path, 'functions', subfolder, 'melee_raycast', 'player_hurt_entity.mcfunction'), 'w') as player_hurt_entity_file:
            player_hurt_entity_file.write(f"advancement revoke @s only {namespace}:{subfolder}/utils/melee_raycast/player_hurt_entity")
    with open(os.path.join(namespace_path, 'functions', subfolder, 'melee_raycast', 'player_hurt_entity.mcfunction'), 'a') as player_hurt_entity_file:
        player_hurt_entity_file.write('\n'+f"execute if entity @s[predicate={namespace}:{subfolder}/selecteditem/{item_name}] at @s anchored eyes run function {namespace}:{subfolder}/melee_raycast/{item_name}/init")  
    
    # Raycast function
    with open(os.path.join(item_function_path, 'init.mcfunction'), 'w') as init_file:
        init_file.write(f'tag @s add {namespace}.{item_name}.ray_caster'+'\n')
        for distance in float_range(0, 6, raycast_precision):
            init_file.write(f'execute positioned ^ ^ ^{distance:g} run function {namespace}:{subfolder}/melee_raycast/{item_name}/ray_cast'+'\n')
        init_file.write(f"""
tag @s remove {namespace}.{item_name}.ray_caster
execute as @e[distance=..6,tag={namespace}.{item_name}.ray_casted,predicate={namespace}:{subfolder}/utils/hurt_time,limit=1,sort=nearest] run function {namespace}:{subfolder}/melee_raycast/{item_name}/exe
        """.strip())

    with open(os.path.join(item_function_path, 'ray_cast.mcfunction'), 'w') as ray_cast_file:
        if raycast_precision >= 1:
            ray_cast_file.write(f"execute positioned ~-{raycast_precision/2:g} ~-{raycast_precision/2:g} ~-{raycast_precision/2:g} run tag @e[tag=!{namespace}.{item_name}.ray_caster,dx={raycast_precision-1:g},dy={raycast_precision-1:g},dz={raycast_precision-1:g}] add {namespace}.{item_name}.ray_casted"+'\n')
        if raycast_precision < 1:
            ray_cast_file.write(f"execute positioned ~-{1-raycast_precision/2:g} ~-{1-raycast_precision/2:g} ~-{1-raycast_precision/2:g} as @e[tag=!{namespace}.{item_name}.ray_caster,dx=0,dy=0,dz=0] positioned ~{1-raycast_precision:g} ~{1-raycast_precision:g} ~{1-raycast_precision:g} run tag @s[dx=0,dy=0,dz=0] add {namespace}.{item_name}.ray_casted"+'\n')
    

    with open(os.path.join(item_function_path, 'exe.mcfunction'), 'w') as exe_file:
        exe_file.write(f'tag @s remove {namespace}.{item_name}.ray_casted\nsay [PLACEHOLDER]')

    subdatapack.window.clear()
    subdatapack.window.label(f'Melee Raycast is successfully generated under {namespace}/{subfolder} with item nbt: "{{{item_nbt}}}."', 16, (20,10))
    subdatapack.pack_main_menu()

class MeleeRaycast:

    def melee_raycast(self):
        self.window.clear()
        self.window.label("Melee Raycast", font_size=18, pad=(10,10))
        self.pack_main_menu()

        subdatapack = SubDatapack(self)
        subdatapack.choose_subfolder()

        output_item_frame = tk.LabelFrame(subdatapack.window.root, padx=50, pady=20, text=f" Output item ")
        output_item_frame.pack(padx=10, pady=10)

        tk.Label(output_item_frame, text="Item's name: ").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        item_name_entry = tk.Entry(output_item_frame, width=30)
        item_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(output_item_frame, text="NBT: {" ).grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        item_nbt_entry = tk.Entry(output_item_frame, width=30)
        item_nbt_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        tk.Label(output_item_frame, text="}").grid(row=1, column=2, padx=5, pady=5, sticky=tk.E)

        raycast_precision = tk.LabelFrame(subdatapack.window.root, padx=50, pady=20, text=f" Raycast Precision ")
        raycast_precision.pack(padx=10, pady=10)

        tk.Label(raycast_precision, text="Distance between checks: ").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        raycast_precision_entry = tk.Entry(raycast_precision, width=10)
        raycast_precision_entry.grid(row=0, column=1, padx=5, pady=5)
        raycast_precision_entry.insert(0, "0.5")
        
        entries = {
            'item_name': item_name_entry,
            'item_nbt': item_nbt_entry,
            'raycast_precision': raycast_precision_entry
        }

        tk.Button(subdatapack.window.root, text="Generate", width=30, font=("", 16), command=lambda: generate(subdatapack, entries)).pack(padx=20, pady=10)