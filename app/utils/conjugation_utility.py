import pprint

from app.utils.initial_mutation_utility import eclipse_verb, lenite_verb, starts_with_vowel_or_f

future_root_endings = {
    1: {
        's': {
            'O': {
                'analytic': 'fidh',
                '1pl': 'fimid',
                'impersonal': 'fear',
                'relative': 'feas'
            }
        },
        'b': {
            'O': {
                'analytic': 'faidh',
                '1pl': 'faimid',
                'impersonal': 'far',
                'relative': 'fas'  # Relative form for 1st broad
            }
        }
    },
    2: {
        's': {
            'O': {
                'analytic': 'eoidh',
                '1pl': 'eoimid',
                'impersonal': 'eofar',
                'relative': 'eos'  # Relative form for 2nd slender
            }
        },
        'b': {
            'O': {
                'analytic': 'óidh',
                '1pl': 'óimid',
                'impersonal': 'ófar',
                'relative': 'ós'  # Relative form for 2nd broad
            }
        }
    },
    'irregular': {
        'msg': 'Irregular forms are not supported.'
    }
}

past_habitual_root_endings = {
    1: {
        's': {
            'O' : {
                'analytic': 'eadh',
                '1sg': 'inn',
                '2sg': 'teá',
                '1pl': 'imis',
                '3pl': 'idís',
                'impersonal': 'tí'
            }
        },
        'b': {
            'O' : {
                'analytic': 'adh',
                '1sg': 'ainn',
                '2sg': 'tá',
                '1pl': 'aimis',
                '3pl': 'aidís',
                'impersonal': 'taí'
            }
        }
    },
    2: {
        's': {
            'O' : {
                'analytic': 'íodh',
                '1sg': 'ínn',
                '2sg': 'íteá',
                '1pl': 'ímis',
                '3pl': 'ídís',
                'impersonal': 'ítí'
            }
        },
        'b': {
            'O' : {
                'analytic': 'aíodh',
                '1sg': 'aínn',
                '2sg': 'aíteá',
                '1pl': 'aímis',
                '3pl': 'aídís',
                'impersonal': 'aítí'
            }
        }
    }
}

conditional_root_endings = {
    1: {
        's': {
            'O': {
                'analytic': 'feadh',
                '1sg': 'finn',
                '2sg': 'feá',
                '1pl': 'fimis',
                '3pl': 'fidís',
                'impersonal': 'fí'
            }
        },
        'b': {
            'O': {
                'analytic': 'fadh',
                '1sg': 'fainn',
                '2sg': 'fá',
                '1pl': 'faimis',
                '3pl': 'faidís',
                'impersonal': 'faí'
            }
        }
    },
    2: {
        's': {
            'O': {
                'analytic': 'eodh',
                '1sg': 'eoinn',
                '2sg': 'eofá',
                '1pl': 'eoimis',
                '3pl': 'eoidís',
                'impersonal': 'eofaí'
            }
        },
        'b': {
            'O': {
                'analytic': 'ódh',
                '1sg': 'óinn',
                '2sg': 'ófá',
                '1pl': 'óimis',
                '3pl': 'óidís',
                'impersonal': 'ófaí'
            }
        }
    }
}

present_root_endings = {
    1: {
        's': {
            'O': {
                'analytic': 'eann',
                '1sg': 'im',
                '1pl': 'imid',
                'impersonal': 'tear',
                'relative1': 'eanns',
                'relative2': 'eas',
            }
        },
        'b': {
            'O': {
                'analytic': 'ann',
                '1sg': 'aim',
                '1pl': 'aimid',
                'impersonal': 'tar',
                'relative1': 'anns',
                'relative2': 'as',
            }
        }
    },
    2: {
        's': {
            'O': {
                'analytic': 'íonn',
                '1sg': 'ím',
                '1pl': 'ímid',
                'impersonal': 'ítear',
                'relative1': 'íonns',
                'relative2': 'íos',
            }
        },
        'b': {
            'O': {
                'analytic': 'aíonn',
                '1sg': 'aím',
                '1pl': 'aímid',
                'impersonal': 'aítear',
                'relative1': 'aíonns',
                'relative2': 'aíos',
            }
        }
    },
    'irregular': {
        'msg': 'Irregular forms are not supported.'
    }
}

past_root_endings = {
    1: {
        's': {
            'O': {
                'analytic': '',
                '1pl': 'eamar',
                '3pl': 'eadar',
                'impersonal': 'eadh',
            }
        },
        'b': {
            'O': {
                'analytic': '',
                '1pl': 'amar',
                '3pl': 'adar',
                'impersonal': 'adh',
            }
        }
    },
    2: {
        's': {
            'O': {
                'analytic': '',
                '1pl': 'íomar',
                '3pl': 'íodar',
                'impersonal': 'íodh'
            }
        },
        'b': {
            'O': {
                'analytic': '',
                '1pl': 'aíomar',
                '3pl': 'aíodar',
                'impersonal': 'aíodh',
            }
        }
    },
    'irregular': {
        'msg': 'Irregular forms are not supported.'
    }
}


def add_past_particle(verb_form, particle = "do", dialect='O'):
    if particle == 'do':
        if starts_with_vowel_or_f(verb_form):
            return f"d'{lenite_verb(verb_form)}"
        else:
            return f"{lenite_verb(verb_form)}"
    elif particle == "níor":
        return f"níor {lenite_verb(verb_form)}"
    elif particle == "ar":
        return f"ar {lenite_verb(verb_form)}"
    else:
        return lenite_verb(verb_form)

def add_unmarked_particle(verb_form, particle = "", dialect = 'O'):
    if particle == "":
        return verb_form
    elif particle == "Negative":
        return f"ní {lenite_verb(verb_form)}"
    elif particle == "Interrogative":
        return f"an {eclipse_verb(verb_form)}"
    else:
        return verb_form

# Conjugating PRESENT and FUTURE
def conjugate_futurey(tense, root, root_class, root_width, dialect):

    conjugation = {}

    tense_endings  = present_root_endings if tense == "present" else future_root_endings

    endings = tense_endings[root_class][root_width][dialect]

    # Apply endings to future root form
    for pronoun, ending in endings.items():
        conjugation[pronoun] = []
        base_form = f"{root}{ending}"
        base_form_lytic = 'analytic' if pronoun == 'analytic' else 'synthetic'

        # base form
        conjugation[pronoun].append((base_form, base_form_lytic, 'unmarked'))

        # Negative form with "ní"
        if not pronoun.startswith("relative"):
            lenited_verb = lenite_verb(root)
            negative_form = f"ní {lenited_verb}{ending}"
            conjugation[pronoun].append((negative_form, base_form_lytic, 'negative'))

            # Question form with "an"
            eclipsed_verb = eclipse_verb(root)
            question_form = f"an {eclipsed_verb}{ending}"
            conjugation[pronoun].append((question_form, base_form_lytic, 'interrogative'))

    return conjugation

def conjugate_future_tense(verb_data, dialect='O'):
    root = verb_data['future_root']
    root_class = verb_data.get('future_class' , verb_data['class'])
    root_width = verb_data.get('future_width' , verb_data['width'])

    return conjugate_futurey("future", root, root_class, root_width, dialect)

def conjugate_present_tense(verb_data, dialect = 'O'):
    root = verb_data.get('present_root', verb_data['future_root'])
    root_class = verb_data.get('future_class' , verb_data['class'])
    root_width = verb_data.get('future_width' , verb_data['width'])

    return conjugate_futurey("present", root, root_class, root_width, dialect)

def conjugate_past_habitual_tense(verb_data, dialect = 'O'):
    synthetic_form_root = verb_data.get('future_root', verb_data['verb'])
    endings_class = verb_data.get('future_class', verb_data['class'])
    endings_width = verb_data.get('future_width', verb_data['width'])

    conjugation = {}
    endings = past_habitual_root_endings[endings_class][endings_width][dialect]

    for pronoun, ending in endings.items():

        active_root = synthetic_form_root
        lytic_info = 'analytic' if pronoun == 'analytic' else 'synthetic'

        forms = []

        # All Past Habitual forms, including impersonal, get lenited

        unmarked_form = f"{add_past_particle(active_root, "do")}{ending}"
        negative_form =  f"{add_unmarked_particle(active_root, "Negative")}{ending}"
        interrogative_form =  f"{add_unmarked_particle(active_root, "Interrogative")}{ending}"

        forms.append((unmarked_form, lytic_info, 'unmarked'))
        forms.append((negative_form, lytic_info, 'negative'))
        forms.append((interrogative_form, lytic_info, 'interrogative'))

        conjugation[pronoun] = forms

    return conjugation

def conjugate_conditional_tense(verb_data, dialect = 'O'):
    synthetic_form_root = verb_data.get('future_root', verb_data['verb'])
    endings_class = verb_data.get('future_class', verb_data['class'])
    endings_width = verb_data.get('future_width', verb_data['width'])

    conjugation = {}
    endings = conditional_root_endings[endings_class][endings_width][dialect]

    for pronoun, ending in endings.items():

        active_root = synthetic_form_root
        lytic_info = 'analytic' if pronoun == 'analytic' else 'synthetic'

        forms = []

        # All conditional forms, including impersonal, get lenited

        unmarked_form = f"{add_past_particle(active_root, "do")}{ending}"
        negative_form =  f"{add_unmarked_particle(active_root, "Negative")}{ending}"
        interrogative_form =  f"{add_unmarked_particle(active_root, "Interrogative")}{ending}"

        forms.append((unmarked_form, lytic_info, 'unmarked'))
        forms.append((negative_form, lytic_info, 'negative'))
        forms.append((interrogative_form, lytic_info, 'interrogative'))

        conjugation[pronoun] = forms

    return conjugation


def conjugate_past_tense(verb_data, dialect = 'O'):

    analytic_form_root = verb_data.get('verb', '')
    synthetic_form_root = verb_data.get('past_root', verb_data.get('future_root', analytic_form_root))
    root_class = verb_data.get('past_class', verb_data['class'])
    root_width = verb_data.get('past_width', verb_data['width'])

    conjugation = {}
    endings = past_root_endings[root_class][root_width][dialect]

    for pronoun, ending in endings.items():
        """
            'analytic': '',
            '1pl': 'íomar',
            '3pl': 'íodar',
            'impersonal': 'íodh'
        """

        active_root = analytic_form_root if pronoun == 'analytic' else synthetic_form_root
        lytic_info = 'synthetic' if ending else 'analytic'

        forms = []

        # past impersonal forms not lenited

        unmarked_form = (f"{active_root}{ending}" if pronoun == "impersonal" else
            f"{add_past_particle(active_root, "do")}{ending}")
        negative_form =  (f"níor {active_root}{ending}" if pronoun == "impersonal" else
            f"{add_past_particle(active_root, "níor")}{ending}")
        interrogative_form = (f"ar {active_root}{ending}" if pronoun == "impersonal" else
                         f"{add_past_particle(active_root, "ar")}{ending}")

        forms.append((unmarked_form, lytic_info, 'unmarked'))
        forms.append((negative_form, lytic_info, 'negative'))
        forms.append((interrogative_form, lytic_info, 'interrogative'))

        conjugation[pronoun] = forms

    return conjugation