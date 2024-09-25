def starts_with_vowel_or_f(word):
    return word[0] in 'aeiouáéíóú' or word.startswith('f')


def eclipse_verb(verb):
    # Implementing eclipsis (urú) for the verb
    eclipsis_map = {
        'b': 'mb',
        'c': 'gc',
        'd': 'nd',
        'f': 'bhf',
        'g': 'ng',
        'p': 'bp',
        't': 'dt',
    }
    first_letter = verb[0]
    if first_letter in eclipsis_map:
        return eclipsis_map[first_letter] + verb[1:]
    else:
        return verb


def eclipse_impersonal_interrogative(verb):
    # Eclipsis used in impersonal interrogative forms in present and future tenses
    eclipsis_map = {
        'b': 'mb',
        'c': 'gc',
        'd': 'nd',
        'f': 'bhf',
        'g': 'ng',
        'p': 'bp',
        't': 'dt',
    }
    first_letter = verb[0]
    if first_letter in eclipsis_map:
        return eclipsis_map[first_letter] + verb[1:]
    else:
        return verb  # Vowels and other consonants remain unchanged


def lenite_verb(verb):
    # Implementing lenition (séimhiú) for the verb
    if verb.startswith(('b', 'c', 'd', 'f', 'g', 'm', 'p', 's', 't')):
        if verb.startswith('s') and len(verb) > 1 and verb[1] in 'aeiouáéíóúlnr':
            return 'sh' + verb[1:]
        elif verb.startswith('s'):
            return 's' + verb[1:]
        elif verb.startswith('f'):
            return 'fh' + verb[1:]
        else:
            return verb[0] + 'h' + verb[1:]
    return verb
