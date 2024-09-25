from app.utils.conjugation_utility import conjugate_past_tense
from deepdiff import DeepDiff

verb_data = [
    ({
        "verb": "achainigh",
        "future_root": "achain",
        "class": 2,
        "width": "s",
        "definition": "request"
    }, {'1pl': [("d'achainíomar", 'synthetic', 'unmarked'),
         ('níor achainíomar', 'synthetic', 'negative'),
         ('ar achainíomar', 'synthetic', 'interrogative')],
 '3pl': [("d'achainíodar", 'synthetic', 'unmarked'),
         ('níor achainíodar', 'synthetic', 'negative'),
         ('ar achainíodar', 'synthetic', 'interrogative')],
 'analytic': [("d'achainigh", 'analytic', 'unmarked'),
              ('níor achainigh', 'analytic', 'negative'),
              ('ar achainigh', 'analytic', 'interrogative')],
 'impersonal': [('achainíodh', 'synthetic', 'unmarked'),
                ('níor achainíodh', 'synthetic', 'negative'),
                ('ar achainíodh', 'synthetic', 'interrogative')]}) ,
    ({
        "verb": "bac",
        "future_root": "bac",
        "class": 1,
        "width": "b",
        "definition": "1. balk, hinder. 3. heed."
    },{'1pl': [('bhacamar', 'synthetic', 'unmarked'),
         ('níor bhacamar', 'synthetic', 'negative'),
         ('ar bhacamar', 'synthetic', 'interrogative')],
 '3pl': [('bhacadar', 'synthetic', 'unmarked'),
         ('níor bhacadar', 'synthetic', 'negative'),
         ('ar bhacadar', 'synthetic', 'interrogative')],
 'analytic': [('bhac', 'analytic', 'unmarked'),
              ('níor bhac', 'analytic', 'negative'),
              ('ar bhac', 'analytic', 'interrogative')],
 'impersonal': [('bacadh', 'synthetic', 'unmarked'),
                ('níor bacadh', 'synthetic', 'negative'),
                ('ar bacadh', 'synthetic', 'interrogative')]})
]


for item, expected in verb_data:
    actual = conjugate_past_tense(item)
    diff = DeepDiff(actual, expected)
    print('Difference: ' , diff)