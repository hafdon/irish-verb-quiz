import pprint
from typing import Dict, Any

from app.utils.conjugation_utility import conjugate_future_tense, conjugate_present_tense, conjugate_past_tense, \
    conjugate_conditional_tense, conjugate_past_habitual_tense

def generate_full_paradigm(verb_data: Dict[str, Any], dialect = "O") -> Dict[str, Any]:
    """
    Generate the full verb paradigm for all tenses.

    Args:
        verb_data (dict): The data of the current verb.

    Returns:
        dict: A dictionary containing conjugations for all tenses.
    """

    tenses = ['Present', 'Future', 'Past', 'Conditional', 'Past Habitual']

    paradigm = {}

    for tense_name in tenses:
        if tense_name.lower() == 'future':
            conjugations = conjugate_future_tense(verb_data, dialect)
        elif tense_name.lower() == 'present':
            conjugations = conjugate_present_tense(verb_data, dialect)
        elif tense_name.lower() == 'past':
            conjugations = conjugate_past_tense(verb_data, dialect)
        elif tense_name.lower() == 'conditional':
            conjugations = conjugate_conditional_tense(verb_data, dialect)
        elif tense_name.lower() == 'past habitual':
            conjugations = conjugate_past_habitual_tense(verb_data, dialect)

        else:
            continue
        paradigm[tense_name] = conjugations

    return paradigm

