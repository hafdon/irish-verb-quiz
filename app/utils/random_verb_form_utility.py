import random

from app.utils.full_paradigm_utility import conjugate_future_tense, conjugate_present_tense, conjugate_past_tense, \
    conjugate_conditional_tense


def random_verb_form(verbs):

    # Randomly select a verb
    verb_data = random.choice(verbs)
    # Build a list of possible forms
    possible_forms = ['future', 'present', 'past', 'conditional']
    if 'verbal_nouns' in verb_data:
        possible_forms.append('verbal_noun')
    if 'verbal_adjectives' in verb_data:
        possible_forms.append('verbal_adjective')
    # Randomly select a form
    tense_or_form = random.choice(possible_forms)
    # Depending on the tense or form, generate the form
    if tense_or_form == 'future':
        conjugations = conjugate_future_tense(verb_data)
        # Randomly select a pronoun and its forms
        pronoun, forms = random.choice(list(conjugations.items()))
        # Randomly select one of the forms (e.g., base, "ní", or "an")
        form_tuple = random.choice(forms)
        form, form_type, form_marker = form_tuple
        # Return the verb data including the definition, tense, and conjugations
        return verb_data, pronoun, form, form_type, 'future', conjugations, form_marker
    elif tense_or_form == 'present':
        conjugations = conjugate_present_tense(verb_data)
        # Randomly select a pronoun and its forms
        pronoun, forms = random.choice(list(conjugations.items()))
        form_tuple = random.choice(forms)
        form, form_type, form_marker = form_tuple
        return verb_data, pronoun, form, form_type, 'present', conjugations, form_marker
    elif tense_or_form == 'past':
        conjugations = conjugate_past_tense(verb_data)
        pronoun, forms = random.choice(list(conjugations.items()))
        form_tuple = random.choice(forms)
        form, form_type, form_marker = form_tuple
        return verb_data, pronoun, form, form_type, 'past', conjugations, form_marker
    elif tense_or_form == 'conditional':
        conjugations = conjugate_conditional_tense(verb_data)
        pronoun, forms = random.choice(list(conjugations.items()))
        form_tuple = random.choice(forms)
        form, form_type, form_marker = form_tuple
        return verb_data, pronoun, form, form_type, 'conditional', conjugations, form_marker
    elif tense_or_form == 'verbal_noun':
        verbal_nouns = verb_data['verbal_nouns']
        form = random.choice(verbal_nouns)
        pronoun = 'verbal_noun'
        form_type = 'verbal_noun'
        form_marker = 'unmarked'
        conjugations = {}
        return verb_data, pronoun, form, form_type, 'verbal_noun', conjugations, form_marker
    elif tense_or_form == 'verbal_adjective':
        verbal_adjectives = verb_data['verbal_adjectives']
        form = random.choice(verbal_adjectives)
        pronoun = 'verbal_adjective'
        form_type = 'verbal_adjective'
        form_marker = 'unmarked'
        conjugations = {}
        return verb_data, pronoun, form, form_type, 'verbal_adjective', conjugations, form_marker
    else:
        raise ValueError(f"Form '{tense_or_form}' is not yet implemented.")

