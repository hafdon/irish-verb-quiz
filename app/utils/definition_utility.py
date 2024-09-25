import json
import tkinter as tk
from tkinter import messagebox, ttk

from app.utils.file_utility import get_data_file_path


def update_definition_in_json(updated_verb_data):
    data_file = get_data_file_path()
    # Load the entire verbs data
    with open(data_file, 'r', encoding='utf-8') as file:
        verbs = json.load(file)

    # Find the verb in the list and update its definition
    for verb in verbs:
        if verb['verb'] == updated_verb_data['verb']:
            verb['definition'] = updated_verb_data['definition']
            break

    # Write the updated data back to the file
    with open(data_file, 'w', encoding='utf-8') as file:
        json.dump(verbs, file, ensure_ascii=False, indent=4)


def edit_definition(current_verb_data, root):
    if current_verb_data is None:
        messagebox.showinfo("No Verb Selected", "Please generate a verb form first.")
        return

    # Create a new window for editing the definition
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Definition")

    # Current definition
    current_def = current_verb_data.get('definition', '')

    # Label and Entry for new definition
    label = ttk.Label(edit_window, text=f"Edit definition for '{current_verb_data['verb']}':")
    label.pack(pady=5)
    definition_var = tk.StringVar(value=current_def)
    entry = ttk.Entry(edit_window, textvariable=definition_var, width=50)
    entry.pack(pady=5)

    # Save button
    def save_definition():
        new_def = definition_var.get().strip()
        current_verb_data['definition'] = new_def
        update_definition_in_json(current_verb_data)
        edit_window.destroy()
        messagebox.showinfo("Success", f"Definition updated for '{current_verb_data['verb']}'.")

    save_button = ttk.Button(edit_window, text="Save", command=save_definition)
    save_button.pack(pady=10)
