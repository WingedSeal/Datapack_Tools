import os
import tkinter as tk
from typing import Dict
from . import utils

def generate_paths(datapack) -> None:
    namespace_path = datapack.namespace_path
    subfolder = datapack.subfolder
    os.makedirs(os.path.join(namespace_path, 'tags', 'items', subfolder))
    os.makedirs(os.path.join(namespace_path, 'tags', 'functions', subfolder))
    os.makedirs(os.path.join(namespace_path, 'tags', 'fluids', subfolder))
    os.makedirs(os.path.join(namespace_path, 'tags', 'entity_types', subfolder))
    os.makedirs(os.path.join(namespace_path, 'tags', 'blocks', subfolder))
    os.makedirs(os.path.join(namespace_path, 'worldgen', 'template_pool', subfolder))
    os.makedirs(os.path.join(namespace_path, 'worldgen', 'processor_list', subfolder))
    os.makedirs(os.path.join(namespace_path, 'worldgen', 'noise_settings', subfolder))
    os.makedirs(os.path.join(namespace_path, 'worldgen', 'configured_surface_builder', subfolder))
    os.makedirs(os.path.join(namespace_path, 'worldgen', 'configured_structure_feature', subfolder))
    os.makedirs(os.path.join(namespace_path, 'worldgen', 'configured_feature', subfolder))
    os.makedirs(os.path.join(namespace_path, 'worldgen', 'configured_carver', subfolder))
    os.makedirs(os.path.join(namespace_path, 'worldgen', 'biome', subfolder))
    os.makedirs(os.path.join(namespace_path, 'structures', subfolder))
    os.makedirs(os.path.join(namespace_path, 'recipes', subfolder))
    os.makedirs(os.path.join(namespace_path, 'predicates', subfolder))
    os.makedirs(os.path.join(namespace_path, 'loot_tables', subfolder))
    os.makedirs(os.path.join(namespace_path, 'dimension_type', subfolder))
    os.makedirs(os.path.join(namespace_path, 'dimension', subfolder))
    os.makedirs(os.path.join(namespace_path, 'advancements', subfolder))

def generate_pack_mcmeta(datapack) -> None:
    with open(os.path.join(datapack.directory, 'pack.mcmeta'), 'w') as pack_mcmeta:
        pack_mcmeta.write(f"""
{{
    "pack": {{
        "pack_format": {datapack.pack_format},
        "description": "{datapack.description}"
        }}
}}
    """.strip()
        )

def generate_tick_load(datapack) -> None:
    minecraft_function_tags_path = os.path.join(datapack.directory, 'data', 'minecraft', 'tags', 'functions')
    os.makedirs(minecraft_function_tags_path)
    with open(os.path.join(minecraft_function_tags_path, 'load.json'), 'w') as load_json:
        load_json.write(f"""
{{
  "values":[
    "{datapack.namespace}:{datapack.subfolder}/load"
    ]
}}
        """.strip())
    with open(os.path.join(minecraft_function_tags_path, 'tick.json'), 'w') as tick_json:
        tick_json.write(f"""
{{
  "values":[
    "{datapack.namespace}:{datapack.subfolder}/tick"
    ]
}}
        """.strip())

    functions_path = os.path.join(datapack.namespace_path, 'functions', datapack.subfolder)
    os.makedirs(functions_path)
    with open(os.path.join(functions_path, 'load.mcfunction'), 'w') as load_mcfunction:
        load_mcfunction.write(
            f'tellraw @a [{{"text":"{datapack.datapack_name}","color":"gold"}},{{"text":" datapack has been successfully installed.","color":"green"}}]'
        )
    open(os.path.join(functions_path, 'tick.mcfunction'), 'w').close()

def generate_optional_files(datapack, options: Dict[str, tk.Checkbutton]) -> None:
    options_path = {
        'shulkerbox_manip_loot_table': os.path.join(datapack.directory, 'data', 'minecraft', 'loot_tables', 'blocks', 'shulker_box.json'),
        'undead_entity_tag': os.path.join(datapack.namespace_path, 'tags', 'entity_types', datapack.subfolder, 'undeads.json'),
        'baby_form_entity_tag': os.path.join(datapack.namespace_path, 'tags', 'entity_types', datapack.subfolder, 'have_baby_form.json'),
        'transparent_block_tag': os.path.join(datapack.namespace_path, 'tags', 'blocks', datapack.subfolder, 'transparent_blocks.json'),
        'plants_block_tag': os.path.join(datapack.namespace_path, 'tags', 'blocks', datapack.subfolder, 'plants.json')
    }
    for option, file_path in options_path.items():
        if options[option].get():
            if not os.path.exists(os.path.dirname(file_path)):
                os.makedirs(os.path.dirname(file_path))
            with open(utils.resource_path('optional_files', f'{option}.txt'), 'r') as optional_file:
                file_data = optional_file.read()
            with open(file_path, 'w') as json_file:
                json_file.write(file_data)