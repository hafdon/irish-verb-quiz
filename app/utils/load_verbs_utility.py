import json

from app.utils.file_utility import ensure_data_file, get_data_file_path

from typing import TypedDict, Optional, List

VerbEntry = TypedDict('VerbEntry', {
    'verb': str,
    'future_root': str,
    'impersonal_present': Optional[str],
    'class': int,
    'width': str,
    'definition': str,
    'verbal_nouns': Optional[List[str]],
    'verbal_adjectives': Optional[List[str]],
}, total=False)

def load_verbs(custom_path: str = None) -> List[VerbEntry]:
    """
    Load the verbs from the JSON data file.

    Args:
        custom_path (str, optional): Custom path to the verb data file. Defaults to None.

    Returns:
        List[VerbEntry]: A list of verb entries with their data.
    """
    ensure_data_file(custom_path)
    data_file = get_data_file_path(custom_path)
    with open(data_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    verbs: List[VerbEntry] = []
    for item in data:
        try:
            verb_entry: VerbEntry = {
                'verb': item['verb'],
                'future_root': item['future_root'],
                'impersonal_present': item.get('impersonal_present'),
                'class': item['class'],
                'width': item['width'],
                'definition': item['definition'],
                'verbal_nouns': item.get('verbal_nouns'),
                'verbal_adjectives': item.get('verbal_adjectives'),
            }
            verbs.append(verb_entry)
        except KeyError as e:
            print(f"Missing key {e} in item: {item}")
            # Handle the error as needed

    return verbs
