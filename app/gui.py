# gui.py
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import logging
import random

from app.utils.full_paradigm_utility import generate_full_paradigm
from app.utils.definition_utility import edit_definition
from app.utils.load_verbs_utility import load_verbs
from app.paradigm_display import display_paradigm

from typing import Dict, Any

# Additional Imports for Audio Playback
import requests
from playsound import playsound
import tempfile
import urllib.parse
import threading

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to capture all levels of logs
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='../app.log',  # Log to a file named app.log
    filemode='a'  # Append mode
)


class VerbConjugationApp():
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Irish Verb Conjugation Quiz")

        # Initialize verb data
        self.verbs = []
        self.current_paradigm = None
        self.current_verb_data = None

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

        # Initialize GUI components
        self._init_gui()

    def load_default_verbs(self):
        """
        Load verbs from the default data file.
        """
        try:
            self.verbs = load_verbs()
            logging.debug(f"Loaded {len(self.verbs)} verbs from default data file.")
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
            text="Generate Random Form",
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
        self.selected_tenses = {
            'Present': tk.BooleanVar(value=True),
            'Past': tk.BooleanVar(value=True),
            'Future': tk.BooleanVar(value=True),
            'Conditional': tk.BooleanVar(value=True),
            'verbal_noun': tk.BooleanVar(value=True),
            'verbal_adjective': tk.BooleanVar(value=True),
        }

        # Create Checkbuttons for each verb form
        ttk.Checkbutton(forms_selection_frame, text="Present", variable=self.selected_tenses['Present']).grid(row=0, column=0, sticky='w', padx=5)
        ttk.Checkbutton(forms_selection_frame, text="Past", variable=self.selected_tenses['Past']).grid(row=0, column=1, sticky='w', padx=5)
        ttk.Checkbutton(forms_selection_frame, text="Future", variable=self.selected_tenses['Future']).grid(row=0, column=2, sticky='w', padx=5)
        ttk.Checkbutton(forms_selection_frame, text="Conditional", variable=self.selected_tenses['Conditional']).grid(row=0, column=3, sticky='w', padx=5)
        ttk.Checkbutton(forms_selection_frame, text="Verbal Noun", variable=self.selected_tenses['verbal_noun']).grid(row=0, column=4, sticky='w', padx=5)
        ttk.Checkbutton(forms_selection_frame, text="Verbal Adjective", variable=self.selected_tenses['verbal_adjective']).grid(row=0, column=5, sticky='w', padx=5)

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
            text="Check Answer",
            command=self.check_answer,
            state="disabled"
        )
        self.check_answer_button.grid(row=3, column=0, pady=10, sticky='w')

        # Result display
        self.result_text = tk.Text(bottom_frame, height=6, width=60, wrap='word', state='disabled')
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

            # **Get the selected dialect**
            selected_dialect = self.dialect_var.get()
            logging.debug(f"Selected Dialect: {selected_dialect}")

            # **Step 1: Determine Whether to Use a Frozen Verb or Select a New One**
            if self.freeze_verb_var.get() and self.current_verb_data:
                # Use the currently frozen verb
                verb_data = self.current_verb_data
                verb = verb_data['verb']
                definition = verb_data.get('definition', '')
                logging.debug(f"Using frozen verb: {verb}")
            else:
                # Select a new random verb
                verb_data = random.choice(self.verbs)
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
            if selected_tense in ['verbal_noun', 'verbal_adjective']:
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
        user_form_marker = self.user_form_marker_var.get()
        user_pronoun = self.user_form_var.get()

        # Clear the result_text widget
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', tk.END)

        # Initialize feedback
        feedback = []

        # Check verb correctness
        if user_verb.lower() == self.correct_verb.lower():
            feedback.append(("Correct: Verb", 'correct'))
        else:
            feedback.append((f"Incorrect: Verb (Correct: '{self.correct_verb}')", 'incorrect'))

        # **Modified Tense Comparison for Case-Insensitive Check**
        # Log the values for debugging
        logging.debug(f"User Tense: '{user_tense}' | Correct Tense: '{self.correct_tense}'")

        if user_tense.lower() == self.correct_tense.lower():
            feedback.append((f"Correct: Tense '{self.correct_tense}'", 'correct'))
        else:
            feedback.append((f"Incorrect: Tense (Correct: '{self.correct_tense}')", 'incorrect'))

        # Check based on tense type
        if self.correct_tense.lower() in ['verbal_noun', 'verbal_adjective']:
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

        self.result_text.config(state='disabled')

        # Disable further interactions until next question
        self._disable_all_inputs()

        # Show pronunciation buttons
        self.pronunciation_frame.grid()

    def _disable_all_inputs(self):
        # Disable tense radio buttons
        self._disable_radio_buttons(self.tense_radio_buttons)
        # Disable form marker radio buttons
        self._disable_radio_buttons(self.form_marker_radio_buttons)
        # Disable form radio buttons
        self._disable_radio_buttons(self.form_radio_buttons)
        # Disable 'Check Answer' button
        self.check_answer_button.config(state="disabled")

    def on_verb_entry_change(self, *args):
        entry_content = self.verb_entry_var.get()
        if not self.correct_verb:
            return
        if entry_content.strip() and self.user_tense_var.get():
            if self.correct_tense.lower() in ['verbal_noun', 'verbal_adjective']:
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
        if not self.correct_verb:
            return
        if self.verb_entry_var.get().strip() and self.user_tense_var.get():
            if self.correct_tense.lower() in ['verbal_noun', 'verbal_adjective']:
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
        if not self.correct_verb:
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
        if not self.correct_verb:
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
