import tkinter as tk
from . import SubDatapack

def input_recipes(subdatapack, entries: dict) -> None:
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

    tk.Button(subdatapack.recipes_frame, text="Generate", width=30, font=("", 16)).grid(row=amount_of_type*3, column=0, columnspan=3, padx=10, pady=10)


def main(datapack) -> None:
    datapack.window.clear()
    datapack.window.label("Custom Floor Crafting", font_size=18, pad=(10,10))
    datapack.pack_main_menu()

    subdatapack = SubDatapack(datapack)
    subdatapack.choose_subfolder()

    output_item_frame = tk.LabelFrame(subdatapack.window.root, padx=50, pady=20, text=f" Output item ")
    output_item_frame.pack(padx=10, pady=10)

    tk.Label(output_item_frame, text="Item's name: ").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
    item_name_entry = tk.Entry(output_item_frame, width=30)
    item_name_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(output_item_frame, text="Amount of type of item in the recipe: ").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
    type_entry = tk.Entry(output_item_frame, width=30)
    type_entry.grid(row=2, column=1, padx=5, pady=5)

    recipes_frame = tk.LabelFrame(subdatapack.window.root, padx=20, pady=10, text="Recipes")
    subdatapack.recipes_frame = recipes_frame
    entries = {
        'amount_of_type': type_entry,
        'item_name': item_name_entry
    }

    tk.Button(subdatapack.window.root, text="Input recipes", command=lambda: input_recipes(subdatapack, entries)).pack(padx=20, pady=10)