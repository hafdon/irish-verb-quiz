# gui.py
import json
import logging
import os
import random
import tempfile
import textwrap
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from app.paradigm_display import display_paradigm
from app.utils.definition_utility import edit_definition
from app.utils.full_paradigm_utility import generate_full_paradigm
from app.utils.load_verbs_utility import load_verbs

# Configure logging

# Get a temporary directory
temp_dir = tempfile.gettempdir()
log_file_path = os.path.join(temp_dir, 'app.log')

# Handle Exceptions When Configuring Logging
try:
    logging.basicConfig(
        level=logging.DEBUG,  # Set to DEBUG to capture all levels of logs
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=log_file_path,
        filemode='a'
    )
except PermissionError as e:
    # If logging to a file fails, log to stderr
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.error(f"Failed to write log to {log_file_path}: {e}")

class VerbConjugationApp():
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Irish Verb Conjugation Quiz")

        # Initialize verb data
        self.verbs = []
        self.current_paradigm = None
        self.current_verb_data = None

        # **Initialize verb selection variables**
        self.verb_selection_vars = {}

        # Load default verbs
        self.load_default_verbs()

        # Initialize state variables
        self.correct_verb = None
        self.correct_definition = None
        self.correct_pronoun = None
        self.correct_form_type = None
        self.correct_tense = None
        self.correct_form_marker = None

        # **Initialize the Freeze Verb Variable**
        self.freeze_verb_var = tk.BooleanVar(value=False)  # Default is not frozen

        # **Initialize the Dialect Variable**
        self.dialect_var = tk.StringVar(value='O')  # Default dialect is Official

        # Initialize a flag to track if we're in dictionary-form-only mode
        self.only_dictionary_form_selected = False

        # Initialize GUI components
        self._init_gui()

        # **Bind Shortcuts**
        self.root.bind('<Command-r>', lambda event: self.display_random_form())
        self.root.bind('<Command-c>', lambda event: self.check_answer())


    def load_default_verbs(self):
        """
        Load verbs from the default data file.
        """
        try:
            self.verbs = load_verbs()
            logging.debug(f"Loaded {len(self.verbs)} verbs from default data file.")

            # **Update verb selection variables**
            for verb_data in self.verbs:
                verb = verb_data['verb']
                if verb not in self.verb_selection_vars:
                    self.verb_selection_vars[verb] = tk.BooleanVar(value=True)
        except FileNotFoundError as e:
            logging.error(f"Default data file not found: {e}")
            messagebox.showerror("Error", f"Default data file not found: {e}")
            self.verbs = []

    def _init_gui(self):
        # Create Frames for better layout management
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.grid(row=0, column=0, sticky="ew")

        middle_frame = ttk.Frame(self.root, padding="10")
        middle_frame.grid(row=1, column=0, sticky="ew")

        bottom_frame = ttk.Frame(self.root, padding="10")
        bottom_frame.grid(row=2, column=0, sticky="ew")

        # === Top Frame: Buttons ===
        self.generate_button = ttk.Button(
            top_frame,
            text="Generate Random Form (⌘R)",
            command=self.display_random_form
        )
        self.generate_button.grid(row=0, column=0, padx=5, pady=5)

        self.show_forms_button = ttk.Button(
            top_frame,
            text="Show All Forms",
            command=self.show_all_forms
        )
        self.show_forms_button.grid(row=0, column=1, padx=5, pady=5)

        self.edit_definition_button = ttk.Button(
            top_frame,
            text="Edit Definition",
            command=lambda: edit_definition(self.current_verb_data, self.root)
        )
        self.edit_definition_button.grid(row=0, column=2, padx=5, pady=5)

        self.load_data_button = ttk.Button(
            top_frame,
            text="Load Verb Data",
            command=self.load_custom_verb_data
        )
        self.load_data_button.grid(row=0, column=3, padx=5, pady=5)

        # **Freeze Verb Checkbox**
        self.freeze_verb_check = ttk.Checkbutton(
            top_frame,
            text="Freeze Current Verb",
            variable=self.freeze_verb_var
        )
        self.freeze_verb_check.grid(row=0, column=4, padx=5, pady=5)  # Placed next to Load Verb Data

        # Add a label that becomes visible when a verb is frozen to inform the user.
        self.frozen_label = ttk.Label(
            top_frame,
            text="(Current verb is frozen)",
            foreground="red"
        )
        self.frozen_label.grid(row=0, column=5, padx=5, pady=5)
        self.frozen_label.grid_remove()  # Hide initially

        # Add a trace to show/hide the label based on checkbox state
        self.freeze_verb_var.trace_add('write', self.update_frozen_label)

        # Add the "Select Verbs" button
        self.select_verbs_button = ttk.Button(
            top_frame,
            text="Select Verbs",
           command=self.select_verbs
        )
        self.select_verbs_button.grid(row=0, column=6, padx=5, pady=5)

        # === Top Frame: Verb Forms Selection ===

        # **Added RadioButtons for selecting dialect**
        dialect_selection_frame = ttk.LabelFrame(top_frame, text="Select Dialect", padding="10")
        dialect_selection_frame.grid(row=1, column=0, columnspan=4, pady=10, sticky='w')

        # Create RadioButtons for each dialect
        ttk.Radiobutton(
            dialect_selection_frame,
            text="Official",
            variable=self.dialect_var,
            value='O'
        ).grid(row=0, column=0, sticky='w', padx=5)
        ttk.Radiobutton(
            dialect_selection_frame,
            text="Connacht",
            variable=self.dialect_var,
            value='C'
        ).grid(row=0, column=1, sticky='w', padx=5)
        ttk.Radiobutton(
            dialect_selection_frame,
            text="Ulster",
            variable=self.dialect_var,
            value='U'
        ).grid(row=0, column=2, sticky='w', padx=5)
        ttk.Radiobutton(
            dialect_selection_frame,
            text="Munster",
            variable=self.dialect_var,
            value='M'
        ).grid(row=0, column=3, sticky='w', padx=5)

        # Added Checkboxes for selecting verb forms
        forms_selection_frame = ttk.LabelFrame(top_frame, text="Select Verb Forms to Test", padding="10")
        forms_selection_frame.grid(row=2, column=0, columnspan=4, pady=10, sticky='w')

        # Initialize BooleanVars for each verb form
        # This dictionary holds the BooleanVar variables
        # that track whether each tense is selected in the GUI.
        self.selected_tenses = {
            'present': tk.BooleanVar(value=True),
            'past': tk.BooleanVar(value=True),
            'future': tk.BooleanVar(value=True),
            'conditional': tk.BooleanVar(value=True),
            'verbal_noun': tk.BooleanVar(value=True),
            'verbal_adjective': tk.BooleanVar(value=True),
            'dictionary_form': tk.BooleanVar(value=True),  # Added Dictionary Form
        }

        # Create Checkbuttons for each verb form
        # Checkbuttons allow user to select/deselect verb forms
        # on which they will be tested.
        ttk.Checkbutton(forms_selection_frame, text="Present", variable=self.selected_tenses['present']).grid(row=0, column=0, sticky='w', padx=5)
        ttk.Checkbutton(forms_selection_frame, text="Past", variable=self.selected_tenses['past']).grid(row=0, column=1, sticky='w', padx=5)
        ttk.Checkbutton(forms_selection_frame, text="Future", variable=self.selected_tenses['future']).grid(row=0, column=2, sticky='w', padx=5)
        ttk.Checkbutton(forms_selection_frame, text="Conditional", variable=self.selected_tenses['conditional']).grid(row=0, column=3, sticky='w', padx=5)
        ttk.Checkbutton(forms_selection_frame, text="Verbal Noun", variable=self.selected_tenses['verbal_noun']).grid(row=0, column=4, sticky='w', padx=5)
        ttk.Checkbutton(forms_selection_frame, text="Verbal Adjective", variable=self.selected_tenses['verbal_adjective']).grid(row=0, column=5, sticky='w', padx=5)
        ttk.Checkbutton(forms_selection_frame, text="Dictionary Form",
                        variable=self.selected_tenses['dictionary_form']).grid(row=0, column=6, sticky='w', padx=5)

        # === Middle Frame: Output and Entry ===
        # Output display
        self.output_text = tk.Text(middle_frame, height=5, width=60, wrap='word')
        self.output_text.grid(row=0, column=0, columnspan=6, pady=5)

        # Label and entry for the dictionary form of the verb
        self.verb_entry_label = ttk.Label(
            middle_frame,
            text="Enter the dictionary form of the verb:"
        )
        self.verb_entry_label.grid(row=1, column=0, columnspan=6, sticky='w', pady=(10, 0))

        self.verb_entry_var = tk.StringVar()
        self.verb_entry = ttk.Entry(
            middle_frame,
            width=30,
            textvariable=self.verb_entry_var
        )
        self.verb_entry.grid(row=2, column=0, columnspan=6, pady=5)
        self.verb_entry_var.trace_add('write', self.on_verb_entry_change)

        # === Bottom Frame: Selections and Check Button ===
        # Tense selection
        self.user_tense_var = tk.StringVar()
        self.user_tense_var.set('')  # Initialize with empty string
        self.user_tense_var.trace_add('write', self.on_tense_selected)

        self._create_radio_buttons(
            parent=bottom_frame,
            label_text="Select Tense:",
            options=[
                ('Future', 'future'),
                ('Present', 'present'),
                ('Past', 'past'),
                ('Conditional', 'conditional'),
                ('Verbal Noun', 'verbal_noun'),
                ('Verbal Adjective', 'verbal_adjective'),
            ],
            variable=self.user_tense_var,
            row=0,
            column=0
        )

        # Form marker selection
        self.user_form_marker_var = tk.StringVar()
        self.user_form_marker_var.set('')
        self.user_form_marker_var.trace_add('write', self.on_form_marker_selected)

        self._create_radio_buttons(
            parent=bottom_frame,
            label_text="Select Form Type:",
            options=[
                ('Unmarked', 'unmarked'),
                ('Negative', 'negative'),
                ('Interrogative', 'interrogative'),
            ],
            variable=self.user_form_marker_var,
            row=1,
            column=0
        )

        # Form selection
        self.user_form_var = tk.StringVar()
        self.user_form_var.set('')
        self.user_form_var.trace_add('write', self.on_form_selected)

        self._create_radio_buttons(
            parent=bottom_frame,
            label_text="Select Form:",
            options=[
                ("1sg", "1sg"),
                ("2sg", "2sg"),
                ("1pl", "1pl"),
                ("3pl", "3pl"),
                ("Analytic", "analytic"),
                ("Relative", "relative"),
                ("Impersonal", "impersonal"),
            ],
            variable=self.user_form_var,
            row=2,
            column=0,
            columns=4
        )

        # 'Check Answer' button
        self.check_answer_button = ttk.Button(
            bottom_frame,
            text="Check Answer (⌘C)",
            command=self.check_answer,
            state="disabled"
        )
        self.check_answer_button.grid(row=3, column=0, pady=10, sticky='w')

        # Result display
        self.result_text = tk.Text(bottom_frame, height=1, width=60, wrap='word', state='disabled')
        self.result_text.grid(row=4, column=0, columnspan=6, pady=5)

        # Define tags for coloring
        self.result_text.tag_configure('correct', foreground='green')
        self.result_text.tag_configure('incorrect', foreground='red')
        self.result_text.tag_configure('info', foreground='blue')
        self.result_text.tag_configure('bold', font=('Arial', 10, 'bold'))

        # Pronunciation buttons frame
        self.pronunciation_frame = ttk.Frame(bottom_frame)
        self.pronunciation_frame.grid(row=5, column=0, columnspan=6, pady=5)
        self.pronunciation_frame.grid_remove()  # Hide initially

        # Ulster pronunciation button
        self.ulster_button = ttk.Button(
            self.pronunciation_frame,
            text="Ulster Pronunciation",
            command=self.play_ulster_audio
        )
        self.ulster_button.grid(row=0, column=0, padx=5, pady=5)

        # Munster pronunciation button
        self.munster_button = ttk.Button(
            self.pronunciation_frame,
            text="Munster Pronunciation",
            command=self.play_munster_audio
        )
        self.munster_button.grid(row=0, column=1, padx=5, pady=5)

        # Connacht pronunciation button
        self.connacht_button = ttk.Button(
            self.pronunciation_frame,
            text="Connacht Pronunciation",
            command=self.play_connacht_audio
        )
        self.connacht_button.grid(row=0, column=2, padx=5, pady=5)

    def _create_radio_buttons(self, parent, label_text, options, variable, row, column, columns=6):
        """
        Helper method to create labeled radio buttons.

        Args:
            parent: The parent frame.
            label_text: The text for the label.
            options: A list of tuples (display_text, value).
            variable: The Tkinter variable associated with the radio buttons.
            row: The grid row.
            column: The grid column.
            columns: Number of columns to span for radio buttons.
        """
        label = ttk.Label(parent, text=label_text)
        label.grid(row=row, column=column, sticky='w', pady=(10 if row > 0 else 0, 0))

        radio_buttons = []
        for idx, (text, value) in enumerate(options):
            rb = ttk.Radiobutton(
                parent,
                text=text,
                variable=variable,
                value=value
            )
            rb.grid(row=row, column=column + idx + 1, sticky='w', padx=5)
            radio_buttons.append(rb)

        # Assign radio buttons to class attributes based on label_text
        if 'Tense' in label_text:
            self.tense_radio_buttons = getattr(self, 'tense_radio_buttons', []) + radio_buttons
        elif 'Form Type' in label_text:
            self.form_marker_radio_buttons = getattr(self, 'form_marker_radio_buttons', []) + radio_buttons
        elif 'Form:' in label_text or 'Form' in label_text:
            self.form_radio_buttons = getattr(self, 'form_radio_buttons', []) + radio_buttons

    @staticmethod
    def _enable_radio_buttons(radio_buttons, state="normal"):
        for rb in radio_buttons:
            rb.config(state=state)

    @staticmethod
    def _disable_radio_buttons(radio_buttons):
        for rb in radio_buttons:
            rb.config(state="disabled")

    def select_all_verbs(self):
        for var in self.verb_selection_vars.values():
            var.set(True)

    def deselect_all_verbs(self):
        for var in self.verb_selection_vars.values():
            var.set(False)

    def select_verbs(self):
        """
        Open a dialog window where the user can select/deselect verbs to include in the quiz.
        """
        # Create a new Toplevel window
        verb_selection_window = tk.Toplevel(self.root)
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

        # **Add the "Select All", "Deselect All", and "Save Selection" buttons in a new frame below the search bar**
        button_frame = ttk.Frame(verb_selection_window)
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        select_all_button = ttk.Button(button_frame, text="Select All", command=self.select_all_verbs)
        select_all_button.pack(side=tk.LEFT, padx=5)

        deselect_all_button = ttk.Button(button_frame, text="Deselect All", command=self.deselect_all_verbs)
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
                [verb_data for verb_data in self.verbs if search_term in verb_data['verb'].lower()],
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
                var = self.verb_selection_vars.get(verb, tk.BooleanVar(value=True))
                self.verb_selection_vars[verb] = var

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

        # search_var.trace_add('write', lambda *args: update_displayed_verbs())
        # show_definitions_var.trace_add('write', lambda *args: update_displayed_verbs())

        search_var.trace_add('write', update_displayed_verbs)
        show_definitions_var.trace_add('write', update_displayed_verbs)

        # Initially display all verbs
        update_displayed_verbs()

    def load_custom_verb_data(self):
        """
        Open a file dialog for the user to select a custom verb data file.
        Load verbs from the selected file.
        """
        file_path = filedialog.askopenfilename(
            title="Select Verb Data File",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                # Load verbs from the selected file
                self.verbs = load_verbs(custom_path=file_path)
                # **Reset verb selection variables**
                self.verb_selection_vars = {}
                for verb_data in self.verbs:
                    verb = verb_data['verb']
                    self.verb_selection_vars[verb] = tk.BooleanVar(value=True)
                self.current_paradigm = None  # Reset current paradigm
                self.current_verb_data = None  # Reset current verb data
                messagebox.showinfo("Success", f"Successfully loaded verb data from '{os.path.basename(file_path)}'.")
                logging.debug(f"Loaded verbs from custom file: {file_path}")

                # Clear any existing questions and UI elements
                self.output_text.config(state='normal')
                self.output_text.delete('1.0', tk.END)
                self.output_text.config(state='disabled')

                self.verb_entry.delete(0, tk.END)

                self.result_text.config(state='normal')
                self.result_text.delete('1.0', tk.END)
                self.result_text.config(state='disabled')

                self.user_tense_var.set('')
                self.user_form_marker_var.set('')
                self.user_form_var.set('')

                # Disable form buttons and check answer button
                self._disable_radio_buttons(self.form_radio_buttons)
                self._disable_radio_buttons(self.form_marker_radio_buttons)
                self.check_answer_button.config(state="disabled")

                # Hide pronunciation buttons
                self.pronunciation_frame.grid_remove()

            except FileNotFoundError as e:
                logging.error(f"Custom data file not found: {e}")
                messagebox.showerror("Error", f"Custom data file not found: {e}")
            except json.JSONDecodeError:
                logging.error("Selected file is not a valid JSON.")
                messagebox.showerror("Error", "The selected file is not a valid JSON.")
            except KeyError as e:
                logging.error(f"Missing key {e} in the selected JSON file.")
                messagebox.showerror("Error", f"Missing key {e} in the selected JSON file.")
            except Exception as e:
                logging.error(f"Error loading custom verb data: {e}")
                messagebox.showerror("Error", f"An error occurred while loading the file: {e}")

    def update_frozen_label(self, *args):
        if self.freeze_verb_var.get():
            self.frozen_label.grid()
        else:
            self.frozen_label.grid_remove()

    def display_random_form(self):
        if not self.verbs:
            messagebox.showwarning("No Verbs Loaded", "No verbs are loaded. Please load a verb data file first.")
            return
        try:
            # Retrieve selected tenses from checkboxes
            selected_tenses = [tense for tense, var in self.selected_tenses.items() if var.get()]
            if not selected_tenses:
                messagebox.showwarning("No Forms Selected", "Please select at least one verb form to test on.")
                return
            logging.debug(f"Selected Tenses for Quiz: {selected_tenses}")

            # Check if only "Dictionary Form" is selected
            self.only_dictionary_form_selected = len(selected_tenses) == 1 and 'dictionary_form' in selected_tenses


            # **Get the selected dialect**
            selected_dialect = self.dialect_var.get()
            logging.debug(f"Selected Dialect: {selected_dialect}")

            # **Get the list of selected verbs**
            selected_verbs = [verb_data for verb_data in self.verbs if
                              self.verb_selection_vars.get(verb_data['verb'], tk.BooleanVar(value=True)).get()]
            if not selected_verbs:
                messagebox.showwarning("No Verbs Selected", "Please select at least one verb to include in the quiz.")
                return
            logging.debug(f"Number of Selected Verbs: {len(selected_verbs)}")

            # **Determine Whether to Use a Frozen Verb or Select a New One**
            if self.freeze_verb_var.get() and self.current_verb_data:
                # Use the currently frozen verb
                verb_data = self.current_verb_data
                verb = verb_data['verb']
                definition = verb_data.get('definition', '')
                logging.debug(f"Using frozen verb: {verb}")
            else:
                # Select a new random verb from selected verbs
                verb_data = random.choice(selected_verbs)
                verb = verb_data['verb']
                definition = verb_data.get('definition', '')
                logging.debug(f"Selected Random Verb: {verb}")

                # **Update the Current Verb Data Only If Not Frozen**
                if not self.freeze_verb_var.get():
                    self.current_verb_data = verb_data
                    logging.debug(f"Set current_verb_data to: {verb}")

            # Step 2: Generate the full paradigm with the selected dialect
            paradigm_data = generate_full_paradigm(verb_data, dialect=selected_dialect)
            self.current_paradigm = paradigm_data  # Save the paradigm
            logging.debug(f"Generated Paradigm: {json.dumps(paradigm_data, indent=2)}")

            # Step 3: Select a random form from the paradigm
            # Flatten the paradigm to a list of (tense, pronoun, form_entry)
            forms_list = []
            for tense, conjugations in paradigm_data.items():
                if tense not in selected_tenses:
                    continue  # Skip tenses not selected
                logging.debug(f"Processing Tense: {tense}")
                for pronoun, forms in conjugations.items():
                    for form_entry in forms:
                        forms_list.append((tense, pronoun, form_entry))

            # Safely retrieve 'verbal_nouns' and 'verbal_adjectives' from verb_data
            verbal_nouns = verb_data.get("verbal_nouns", [])
            verbal_adjectives = verb_data.get("verbal_adjectives", [])

            # Optional: Validate that they are lists and check if their tenses are selected
            if isinstance(verbal_nouns, list) and 'verbal_noun' in selected_tenses:
                for form in verbal_nouns:
                    forms_list.append(('verbal_noun', 'verbal_noun', form))
            else:
                if not isinstance(verbal_nouns, list):
                    logging.warning(f"'verbal_nouns' is not a list in verb_data: {verb_data}")

            if isinstance(verbal_adjectives, list) and 'verbal_adjective' in selected_tenses:
                for form in verbal_adjectives:
                    forms_list.append(('verbal_adjective', 'verbal_adjective', form))
            else:
                if not isinstance(verbal_adjectives, list):
                    logging.warning(f"'verbal_adjectives' is not a list in verb_data: {verb_data}")

            # Include dictionary form if selected
            if 'dictionary_form' in selected_tenses:
                forms_list.append(('dictionary_form', 'dictionary_form', verb_data['verb']))

            logging.debug(f"Total Forms Collected: {len(forms_list)}")
            if not forms_list:
                logging.warning("No forms found for the selected tenses.")
                messagebox.showwarning("No Forms Available",
                                       "No verb forms found for the selected tenses. Please try selecting different tenses or load a different verb.")
                return

            selected_tense, selected_pronoun, selected_form_entry = random.choice(forms_list)
            logging.debug(
                f"Selected Form: Tense='{selected_tense}', Pronoun='{selected_pronoun}', Form='{selected_form_entry}'")

            # Handle different lengths of form_entry
            if isinstance(selected_form_entry, list) or isinstance(selected_form_entry, tuple):
                if len(selected_form_entry) == 3:
                    form, form_type, form_marker = selected_form_entry
                elif len(selected_form_entry) == 2:
                    form, form_type = selected_form_entry
                    form_marker = ''
                else:
                    form = selected_form_entry
                    form_type = ''
                    form_marker = ''
            else:
                form = selected_form_entry
                form_type = ''
                form_marker = ''

            if self.only_dictionary_form_selected:
                # Display the verb
                self.output_text.config(state='normal')
                self.output_text.delete('1.0', tk.END)
                self.output_text.insert(tk.END, f"Recall the definition for the verb:\n\n{self.correct_verb}\n")
                self.output_text.config(state='disabled')

                # Disable all input fields
                self.verb_entry.delete(0, tk.END)
                self.verb_entry.config(state='disabled')
                self._disable_radio_buttons(self.tense_radio_buttons)
                self._disable_radio_buttons(self.form_marker_radio_buttons)
                self._disable_radio_buttons(self.form_radio_buttons)

                # Enable 'Check Answer' button
                self.check_answer_button.config(state="normal")
            else:

                # Display the form to the user
                self.output_text.config(state='normal')
                self.output_text.delete('1.0', tk.END)
                self.output_text.insert(tk.END, f"Identify the verb, tense, form, and type:\n\n{form}\n")
                self.output_text.config(state='disabled')

                # Clear the result_text widget
                self.result_text.config(state='normal')
                self.result_text.delete('1.0', tk.END)
                self.result_text.config(state='disabled')

                # Clear the verb entry
                self.verb_entry.delete(0, tk.END)

                # Store the correct answers for later comparison
                self.correct_verb = verb
                self.correct_definition = definition
                self.correct_pronoun = selected_pronoun
                self.correct_form_type = form_type
                self.correct_tense = selected_tense
                self.correct_form_marker = form_marker
                self.current_conjugations = paradigm_data  # Update current conjugations
                self.current_verb_data = verb_data  # Store verb data for later use

                # Clear user's selections
                self.user_tense_var.set('')
                self.user_form_marker_var.set('')
                self.user_form_var.set('')

                # Adjust GUI based on tense
                # These are conditions that check if the selected tense
                # is one that doesn't require form markers or pronouns
                if selected_tense in ['verbal_noun', 'verbal_adjective', 'dictionary_form']:
                    # Disable form buttons and form marker radio buttons
                    self._disable_radio_buttons(self.form_radio_buttons)
                    self._disable_radio_buttons(self.form_marker_radio_buttons)
                    # Enable 'Check Answer' button
                    self.check_answer_button.config(state="normal")
                else:
                    # Enable form marker radio buttons
                    self._enable_radio_buttons(self.form_marker_radio_buttons)
                    # Disable form buttons initially
                    self._disable_radio_buttons(self.form_radio_buttons)
                    # Disable 'Check Answer' button
                    self.check_answer_button.config(state="disabled")

                # Enable tense radio buttons
                self._enable_radio_buttons(self.tense_radio_buttons)

            # Hide pronunciation buttons
            self.pronunciation_frame.grid_remove()

        except ValueError as ve:
            logging.error(f"ValueError in display_random_form: {ve}")
            messagebox.showerror("Error", f"An error occurred: {ve}")
        except Exception as e:
            logging.error(f"Unexpected error in display_random_form: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def show_all_forms(self) -> None:
        """
        Show all forms of the current verb by using the saved paradigm.
        """
        # Check if a paradigm has been generated
        if not self.current_paradigm or not self.current_verb_data:
            messagebox.showinfo("No Verb Selected", "Please generate a verb form first.")
            return

        try:
            # Use the saved paradigm_data
            paradigm_data = self.current_paradigm
            logging.debug(f"Using Saved Paradigm: {paradigm_data}")

            # Display the paradigm
            display_paradigm(self.root, self.current_verb_data, paradigm_data)
        except Exception as e:
            logging.error(f"Error in show_all_forms: {e}")
            messagebox.showerror("Error", f"An error occurred while showing all forms: {e}")

    def check_answer(self):

        # Check if correct_verb is set
        if not self.correct_verb:
            messagebox.showinfo("No Verb Generated", "Please generate a verb form first.")
            return

        # Get user inputs
        user_verb = self.verb_entry.get().strip()
        user_tense = self.user_tense_var.get()
        user_form_marker = self.user_form_marker_var.get() # e.g. Unmarked, Negative, Interrogative
        user_pronoun = self.user_form_var.get()

        # Clear the result_text widget
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', tk.END)

        # Initialize feedback
        feedback = []

        if self.only_dictionary_form_selected:
            pass
        else:

            # Check verb correctness
            if user_verb.lower() == self.correct_verb.lower(): # Case-Insensitive Check
                feedback.append((f"Correct: Verb ({self.correct_verb})", 'correct'))
            else:
                feedback.append((f"Incorrect: Verb (Correct: '{self.correct_verb}')", 'incorrect'))

            # Log the values for debugging
            logging.debug(f"User Tense: '{user_tense}' | Correct Tense: '{self.correct_tense}'")

            # Check tense correctness
            if user_tense.lower() == self.correct_tense.lower(): # Case-Insensitive Check
                feedback.append((f"Correct: Tense '{self.correct_tense}'", 'correct'))
            else:
                feedback.append((f"Incorrect: Tense (Correct: '{self.correct_tense}')", 'incorrect'))

            # Check pronoun and form marker based on tense type
            # These tense types don't have pronouns or form markers to check.
            if self.correct_tense.lower() in ['verbal_noun', 'verbal_adjective', 'dictionary_form']:
                # No form marker or pronoun to check
                pass
            else:
                # Check pronoun/form type
                pronoun_match = False
                if user_pronoun == self.correct_pronoun:
                    pronoun_match = True
                elif self.correct_pronoun in ['relative1', 'relative2'] and user_pronoun == 'relative':
                    pronoun_match = True
                elif user_pronoun == self.correct_form_type:
                    pronoun_match = True

                if pronoun_match:
                    feedback.append((f"Correct: Form [{self.correct_pronoun}]", 'correct'))
                else:
                    feedback.append((f"Incorrect: Form (Correct: [{self.correct_pronoun}])", 'incorrect'))

                # Check form marker
                if user_form_marker == self.correct_form_marker:
                    feedback.append((f"Correct: Form Type '{self.correct_form_marker}'", 'correct'))
                else:
                    feedback.append((f"Incorrect: Form Type (Correct: '{self.correct_form_marker}')", 'incorrect'))

            # Display feedback
            for message, tag in feedback:
                self.result_text.insert(tk.END, message + "\n", tag)

        # Display the definition if available
        if self.correct_definition:
            self.result_text.insert(tk.END, f"\nDefinition: {self.correct_definition}", 'info')
        else:
            self.result_text.insert(tk.END, "No definition available.", 'info')

        # Disable interaction with result text box
        self.result_text.config(state='disabled')

        # Adjust the size of result_text to fit the content
        self._adjust_result_text_height()

        # Disable further interactions until next question
        self._disable_all_inputs()

        # Show pronunciation buttons
        self.pronunciation_frame.grid()

    def _adjust_result_text_height(self):
        self.result_text.update_idletasks()
        num_lines = int(self.result_text.index('end').split('.')[0])
        self.result_text.config(height=num_lines)

    def _disable_all_inputs(self):
        # Disable tense radio buttons
        self._disable_radio_buttons(self.tense_radio_buttons)
        # Disable form marker radio buttons
        self._disable_radio_buttons(self.form_marker_radio_buttons)
        # Disable form radio buttons
        self._disable_radio_buttons(self.form_radio_buttons)
        # Disable 'Check Answer' button
        self.check_answer_button.config(state="disabled")
        # Disable verb entry
        self.verb_entry.config(state='disabled')

    def on_verb_entry_change(self, *args):
        entry_content = self.verb_entry_var.get()
        if not self.correct_verb or self.only_dictionary_form_selected:
            return
        if entry_content.strip() and self.user_tense_var.get():
            if self.correct_tense.lower() in ['verbal_noun', 'verbal_adjective', 'dictionary_form']:
                # Enable the 'Check Answer' button
                self.check_answer_button.config(state="normal")
                # Disable form buttons
                self._disable_radio_buttons(self.form_radio_buttons)
            elif self.user_form_marker_var.get():
                # Enable form buttons
                self._enable_radio_buttons(self.form_radio_buttons)
                # Disable 'Check Answer' button
                self.check_answer_button.config(state="disabled")
            else:
                # Disable form buttons
                self._disable_radio_buttons(self.form_radio_buttons)
                # Disable 'Check Answer' button
                self.check_answer_button.config(state="disabled")
        else:
            # Disable buttons
            self._disable_radio_buttons(self.form_radio_buttons)
            self.check_answer_button.config(state="disabled")

    def on_tense_selected(self, *args):
        if not self.correct_verb or self.only_dictionary_form_selected:
            return
        if self.verb_entry_var.get().strip() and self.user_tense_var.get():
            if self.correct_tense.lower() in ['verbal_noun', 'verbal_adjective', 'dictionary_form']:
                # Enable the 'Check Answer' button
                self.check_answer_button.config(state="normal")
                # Disable form buttons
                self._disable_radio_buttons(self.form_radio_buttons)
            elif self.user_form_marker_var.get():
                # Enable form buttons
                self._enable_radio_buttons(self.form_marker_radio_buttons)
                self._enable_radio_buttons(self.form_radio_buttons)
                # Disable 'Check Answer' button
                self.check_answer_button.config(state="disabled")
            else:
                # Disable form buttons
                self._disable_radio_buttons(self.form_radio_buttons)
                self.check_answer_button.config(state="disabled")
        else:
            # Disable buttons
            self._disable_radio_buttons(self.form_radio_buttons)
            self.check_answer_button.config(state="disabled")

    def on_form_marker_selected(self, *args):
        if not self.correct_verb or self.only_dictionary_form_selected:
            return
        if self.verb_entry_var.get().strip() and self.user_tense_var.get() and self.user_form_marker_var.get():
            # Enable form buttons
            self._enable_radio_buttons(self.form_radio_buttons)
            # Disable 'Check Answer' button
            self.check_answer_button.config(state="disabled")
        else:
            # Disable form buttons
            self._disable_radio_buttons(self.form_radio_buttons)
            # Disable 'Check Answer' button
            self.check_answer_button.config(state="disabled")

    def on_form_selected(self, *args):
        if not self.correct_verb or self.only_dictionary_form_selected:
            return
        if self.verb_entry_var.get().strip() and self.user_tense_var.get() and self.user_form_var.get():
            # Enable 'Check Answer' button
            self.check_answer_button.config(state="normal")
        else:
            # Disable 'Check Answer' button
            self.check_answer_button.config(state="disabled")

    def play_ulster_audio(self):
        self.play_audio('U')

    def play_munster_audio(self):
        self.play_audio('M')

    def play_connacht_audio(self):
        self.play_audio('C')

    def play_audio(self, dialect_code):
        threading.Thread(target=self._play_audio_thread, args=(dialect_code,), daemon=True).start()

    def _play_audio_thread(self, dialect_code):
        import requests
        import urllib.parse
        from playsound import playsound
        import tempfile
        import os

        try:
            verb = self.correct_verb
            encoded_verb = urllib.parse.quote(verb)
            if dialect_code == 'U':
                url = f'https://www.teanglann.ie/CanU/{encoded_verb}.mp3'
            elif dialect_code == 'M':
                url = f'https://www.teanglann.ie/CanM/{encoded_verb}.mp3'
            elif dialect_code == 'C':
                url = f'https://www.teanglann.ie/CanC/{encoded_verb}.mp3'
            else:
                raise ValueError(f"Unknown dialect code: {dialect_code}")
            # Download the mp3 file
            response = requests.get(url)
            if response.status_code == 200:
                # Save to a temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                    temp_file.write(response.content)
                    temp_file.flush()  # Ensure data is written
                    temp_file_name = temp_file.name
                # Play the audio file
                playsound(temp_file_name)
                # Remove the temp file after playing
                os.remove(temp_file_name)
            else:
                self.root.after(0, messagebox.showerror, "Error", f"Audio file not found for '{verb}' in dialect '{dialect_code}'")
        except Exception as e:
            logging.error(f"Error playing audio: {e}")
            # Since we're in a thread, need to use tkinter's thread-safe method to show messagebox
            self.root.after(0, messagebox.showerror, "Error", f"An error occurred while playing audio: {e}")
