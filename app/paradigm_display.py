import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, Any
import logging



def display_paradigm(root:tk.Tk, verb_data: Dict[str, Any], paradigm_data: Dict[str, Any]) -> None:
    """
    Create and open a notebook widget to display the verb paradigm.

    Args:
        verb_data (dict): The data of the current verb.
        paradigm_data (dict): The full verb paradigm data.
        :param root:
    """
    try:
        # Create a new window
        forms_window = tk.Toplevel(root)
        forms_window.title("All Forms")
        # Removed fixed geometry to allow dynamic sizing
        forms_window.geometry("800x600")  # Removed to allow auto-sizing

        # Create a main frame to hold all content with some padding
        main_frame = ttk.Frame(forms_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Verb Information Section ---
        verb_frame = ttk.LabelFrame(main_frame, text="Verb Information", padding="10")
        verb_frame.pack(fill=tk.X, pady=5)

        verb = verb_data.get('verb', 'N/A')
        definition = verb_data.get('definition', 'No definition provided.')

        verb_label = ttk.Label(verb_frame, text=f"Verb: {verb}", font=("Arial", 14, "bold"))
        verb_label.pack(anchor=tk.W, pady=2)

        definition_label = ttk.Label(verb_frame, text=f"Definition: {definition}", font=("Arial", 12))
        definition_label.pack(anchor=tk.W, pady=2)

        # --- Nouns and Adjectives Frame ---
        nouns_adjectives_frame = ttk.Frame(main_frame)
        nouns_adjectives_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # --- Verbal Nouns Section ---
        verbal_nouns = verb_data.get('verbal_nouns', [])
        if verbal_nouns:
            nouns_frame = ttk.LabelFrame(nouns_adjectives_frame, text="Verbal Nouns", padding="10")
            nouns_frame.grid(row=0, column=0, padx=5, sticky='nsew')  # Use grid for side-by-side

            listbox_height = min(len(verbal_nouns), 10)  # Show up to 10 items without scrolling
            nouns_listbox = tk.Listbox(nouns_frame, font=("Arial", 12), height=listbox_height)
            # nouns_listbox = tk.Listbox(nouns_frame, font=("Arial", 12))
            nouns_listbox.pack(fill=tk.BOTH, expand=True)

            # Insert verbal nouns into the listbox
            for noun in verbal_nouns:
                nouns_listbox.insert(tk.END, noun)

            # Add a scrollbar if needed
            scrollbar = ttk.Scrollbar(nouns_frame, orient=tk.VERTICAL, command=nouns_listbox.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            nouns_listbox.config(yscrollcommand=scrollbar.set)
        else:
            no_nouns_label = ttk.Label(nouns_adjectives_frame, text="No verbal nouns available.",
                                       font=("Arial", 12, "italic"))
            no_nouns_label.grid(row=0, column=0, padx=5, sticky='w')

        # --- Verbal Adjectives Section ---
        verbal_adjectives = verb_data.get('verbal_adjectives', [])
        if verbal_adjectives:
            adjectives_frame = ttk.LabelFrame(nouns_adjectives_frame, text="Verbal Adjectives", padding="10")
            adjectives_frame.grid(row=0, column=1, padx=5, sticky='nsew')  # Place next to nouns_frame

            listbox_height = min(len(verbal_adjectives), 10)  # Show up to 10 items without scrolling
            adjectives_listbox = tk.Listbox(adjectives_frame, font=("Arial", 12), height=listbox_height)
            # adjectives_listbox = tk.Listbox(adjectives_frame, font=("Arial", 12))
            adjectives_listbox.pack(fill=tk.BOTH, expand=True)

            # Insert verbal adjectives into the listbox
            for adjective in verbal_adjectives:
                adjectives_listbox.insert(tk.END, adjective)

            # Add a scrollbar if needed
            scrollbar = ttk.Scrollbar(adjectives_frame, orient=tk.VERTICAL, command=adjectives_listbox.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            adjectives_listbox.config(yscrollcommand=scrollbar.set)
        else:
            no_adjectives_label = ttk.Label(nouns_adjectives_frame, text="No verbal adjectives available.",
                                            font=("Arial", 12, "italic"))
            no_adjectives_label.grid(row=0, column=1, padx=5, sticky='w')

        # Configure grid weights to allow proper resizing
        nouns_adjectives_frame.columnconfigure(0, weight=1)
        nouns_adjectives_frame.columnconfigure(1, weight=1)
        nouns_adjectives_frame.rowconfigure(0, weight=1)

        # Optional: Add a Close button at the bottom
        close_button = ttk.Button(main_frame, text="Close", command=forms_window.destroy)
        close_button.pack(pady=10)

        # Create a Notebook widget
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Display forms for each tense
        for tense_name, conjugations in paradigm_data.items():
            # Create a frame for each tense
            tense_frame = ttk.Frame(notebook)
            notebook.add(tense_frame, text=f"{tense_name.title()} Tense")

            # Create a scrollbar for the text widget
            scrollbar = ttk.Scrollbar(tense_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Display the forms in the text widget
            forms_text = tk.Text(tense_frame, wrap='word', yscrollcommand=scrollbar.set)
            forms_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

            # Configure the 'bold' tag for the forms_text widget
            forms_text.tag_configure('bold', font=('Arial', 10, 'bold'))

            # Insert all forms into the text widget
            for pronoun, forms in conjugations.items():
                forms_text.insert(tk.END, f"{pronoun}:\n", 'bold')
                for form_entry in forms:
                    # Handle different lengths of form_entry
                    if isinstance(form_entry, (list, tuple)):
                        if len(form_entry) == 3:
                            form, form_type, form_marker = form_entry
                            forms_text.insert(tk.END, f"  - {form} ({form_type}, {form_marker})\n")
                        elif len(form_entry) == 2:
                            form, form_type = form_entry
                            forms_text.insert(tk.END, f"  - {form} ({form_type})\n")
                        else:
                            forms_text.insert(tk.END, f"  - {form_entry}\n")
                    else:
                        forms_text.insert(tk.END, f"  - {form_entry}\n")
                forms_text.insert(tk.END, "\n")
            forms_text.config(state='disabled')  # Make the text read-only

            # Configure the scrollbar
            scrollbar.config(command=forms_text.yview)

        # **Bind the <<NotebookTabChanged>> Event**
        notebook.bind("<<NotebookTabChanged>>", lambda event: forms_window.update_idletasks())

    except Exception as e:
        logging.error(f"Error in display_paradigm: {e}")
        messagebox.showerror("Error", f"An error occurred while displaying the paradigm: {e}")