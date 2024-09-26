import os
import shutil
import sys
import appdirs

def get_data_file_path(custom_path: str = None) -> str:
    """
    Get the path to the verb data file.

    Args:
        custom_path (str, optional): Custom path provided by the user. Defaults to None.

    Returns:
        str: Path to the verb data file.
    """
    if custom_path:
        # Use the custom path provided by the user
        return custom_path

    if getattr(sys, 'frozen', False):
        # If the application is frozen, use the user data directory
        data_dir = appdirs.user_data_dir("IrishVerbQuiz", "YourCompany")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        data_file = os.path.join(data_dir, 'verbs.json')
    else:
        # If the application is not frozen
        # Check if a command-line argument is provided
        if len(sys.argv) > 1:
            # Use the provided file name in the 'data' directory
            application_path = os.path.dirname(os.path.abspath(__file__))
            data_file = os.path.join(application_path, 'data', sys.argv[1])
        else:
            # Default to 'verbs.json' in 'data' directory
            application_path = os.path.dirname(os.path.abspath(__file__))
            data_file = os.path.join(application_path, 'data', 'verbs.json')
    return data_file

def ensure_data_file(custom_path: str = None) -> None:
    """
    Ensure that the verb data file exists. If not, copy the default one.

    Args:
        custom_path (str, optional): Custom path provided by the user. Defaults to None.
    """
    data_file = get_data_file_path(custom_path)
    if not os.path.exists(data_file):
        if getattr(sys, 'frozen', False):
            # If the application is frozen, copy the default data file to the user's data directory
            application_path = sys._MEIPASS
            default_json_path = os.path.join(application_path, 'data', 'verbs.json')
            shutil.copy(default_json_path, data_file)
        else:
            if custom_path:
                # If a custom path was provided and file doesn't exist, inform the user
                raise FileNotFoundError(f"Custom data file '{data_file}' not found.")
            else:
                # If running normally and the default file doesn't exist, raise an error
                raise FileNotFoundError(f"Data file '{data_file}' not found.")

### To allow dynamic loading, uncomment this call to `ensure_data_file()`:
# ensure_data_file()
