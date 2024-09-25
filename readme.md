# Irish Verb Conjugation Quiz

## Description

A Tkinter-based application for practicing Irish verb conjugations. It allows users to generate random verb forms, view all forms, edit definitions, and load custom verb data.

## Features

- Generate random verb forms based on selected tenses.
- View all conjugated forms of a verb in a separate window.
- Edit verb definitions.
- Load custom verb data from JSON files.
- Comprehensive logging for debugging.

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/verb_conjugation_app.git
    cd verb_conjugation_app
    ```

2. **Set Up a Virtual Environment (Optional but Recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the application using the following command:

```bash
python main.py
```

## build

`pyinstaller --onefile --add-data "data/verbs_debug.json:data" main.py`