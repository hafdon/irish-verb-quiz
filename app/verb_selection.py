import tkinter as tk
from tkinter import ttk
import textwrap

def select_verbs(root, verbs, verb_selection_vars, select_all_verbs, deselect_all_verbs):
    """
    Open a dialog window where the user can select/deselect verbs to include in the quiz.
    """
    # Create a new Toplevel window
    verb_selection_window = tk.Toplevel(root)
    verb_selection_window.title("Select Verbs to Include in Quiz")
    verb_selection_window.geometry("1000x600")  # Adjust width and height as needed

    # Add search bar at the top
    search_frame = ttk.Frame(verb_selection_window)
    search_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

    search_label = ttk.Label(search_frame, text="Search:")
    search_label.pack(side=tk.LEFT)

    search_var = tk.StringVar()
    search_entry = ttk.Entry(search_frame, textvariable=search_var)
    search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    # Add the "Select All", "Deselect All", and "Save Selection" buttons in a new frame below the search bar
    button_frame = ttk.Frame(verb_selection_window)
    button_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

    select_all_button = ttk.Button(button_frame, text="Select All", command=select_all_verbs)
    select_all_button.pack(side=tk.LEFT, padx=5)

    deselect_all_button = ttk.Button(button_frame, text="Deselect All", command=deselect_all_verbs)
    deselect_all_button.pack(side=tk.LEFT, padx=5)

    show_definitions_var = tk.BooleanVar(value=True)  # Default is True (definitions are shown)

    # Function to update displayed verbs
    def update_displayed_verbs(*args):
        search_term = search_var.get().lower()
        for child in frame.winfo_children():
            child.destroy()

        # Increase the number of columns if the definitions are hidden
        if show_definitions_var.get():
            num_columns = 3
        else:
            num_columns = 9

        filtered_verbs = sorted(
            [verb_data for verb_data in verbs if search_term in verb_data['verb'].lower()],
            key=lambda vd: vd['verb'].lower()
        )

        verbs_per_column = len(filtered_verbs) // num_columns + 1

        for idx, verb_data in enumerate(filtered_verbs):
            verb = verb_data['verb']
            if show_definitions_var.get():
                # Shorten the definition
                definition = verb_data.get('definition', '')
                definition = textwrap.shorten(definition, width=35, placeholder='...')
                display_text = f"{verb} - {definition}"
            else:
                display_text = verb
            var = verb_selection_vars.get(verb, tk.BooleanVar(value=True))
            verb_selection_vars[verb] = var

            # Use tk.Checkbutton to enable text wrapping
            cb = tk.Checkbutton(
                frame,
                text=display_text,
                variable=var,
                wraplength=300,
                justify='left',
                anchor='w'  # Align text to the left within the checkbutton
            )
            row = idx % verbs_per_column
            column = idx // verbs_per_column
            cb.grid(row=row, column=column, sticky='w', padx=5, pady=2)

    show_definitions_checkbutton = ttk.Checkbutton(
        button_frame,
        text="Show Definitions",
        variable=show_definitions_var,
        command=update_displayed_verbs  # Update display when toggled
    )
    show_definitions_checkbutton.pack(side=tk.LEFT, padx=5)

    save_button = ttk.Button(button_frame, text="Save Selection", command=verb_selection_window.destroy)
    save_button.pack(side=tk.RIGHT, padx=5)

    # Create a canvas with scrollbar for the list of verbs
    canvas = tk.Canvas(verb_selection_window)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(verb_selection_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor='nw')

    frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

    search_var.trace_add('write', update_displayed_verbs)
    show_definitions_var.trace_add('write', update_displayed_verbs)

    # Initially display all verbs
    update_displayed_verbs()