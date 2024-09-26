# Irish Verb Conjugation Quiz

## Description

A Tkinter-based application for practicing Irish verb conjugations. It allows users to generate random verb forms, view all forms, edit definitions, and load custom verb data.

## Features

- Generate random verb forms based on selected tenses.
- View all conjugated forms of a verb in a separate window.
- Edit verb definitions.
- Load custom verb data from JSON files.
- Integration with `teanglann.ie/en/fuaim` pronunciation files 
- Comprehensive logging for debugging.

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/hafdon/irish-verb-quiz.git
    cd irish-verb-quiz
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

Or, build the application to an executable at `dist/main.exe`:

```bash
pyinstaller --onefile --add-data "app/utils/data/verbs.json:data" main.py
```

### Validate data file

Validate your custom data file:

```bash
 python validate_json.py <path/to/your/data.json> tests/schema.json
```