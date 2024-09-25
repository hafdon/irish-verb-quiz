from app.utils.conjugation_utility import conjugate_present_tense
from deepdiff import DeepDiff

verb_data = [
    ({
        "verb": "achainigh",
        "future_root": "achain",
        "class": 2,
        "width": "s",
        "definition": "request"
    }, {'1pl': [('achainímid', 'synthetic', 'unmarked'),
         ('ní achainímid', 'synthetic', 'negative'),
         ('an achainímid', 'synthetic', 'interrogative')],
 '1sg': [('achainím', 'synthetic', 'unmarked'),
         ('ní achainím', 'synthetic', 'negative'),
         ('an achainím', 'synthetic', 'interrogative')],
 'analytic': [('achainíonn', 'analytic', 'unmarked'),
              ('ní achainíonn', 'analytic', 'negative'),
              ('an achainíonn', 'analytic', 'interrogative')],
 'impersonal': [('achainítear', 'synthetic', 'unmarked'),
                ('ní achainítear', 'synthetic', 'negative'),
                ('an achainítear', 'synthetic', 'interrogative')],
 'relative1': [('achainíonns', 'synthetic', 'unmarked')],
 'relative2': [('achainíos', 'synthetic', 'unmarked')]}
) ,
    ({
        "verb": "bac",
        "future_root": "bac",
        "class": 1,
        "width": "b",
        "definition": "1. balk, hinder. 3. heed."
    },{'1pl': [('bacaimid', 'synthetic', 'unmarked'),
         ('ní bhacaimid', 'synthetic', 'negative'),
         ('an mbacaimid', 'synthetic', 'interrogative')],
 '1sg': [('bacaim', 'synthetic', 'unmarked'),
         ('ní bhacaim', 'synthetic', 'negative'),
         ('an mbacaim', 'synthetic', 'interrogative')],
 'analytic': [('bacann', 'analytic', 'unmarked'),
              ('ní bhacann', 'analytic', 'negative'),
              ('an mbacann', 'analytic', 'interrogative')],
 'impersonal': [('bactar', 'synthetic', 'unmarked'),
                ('ní bhactar', 'synthetic', 'negative'),
                ('an mbactar', 'synthetic', 'interrogative')],
 'relative1': [('bacanns', 'synthetic', 'unmarked')],
 'relative2': [('bacas', 'synthetic', 'unmarked')]}
)
]

# pprint.pprint(conjugate_present_tense({
#         "verb": "bac",
#         "future_root": "bac",
#         "class": 1,
#         "width": "b",
#         "definition": "1. balk, hinder. 3. heed."
#     }))

for item, expected in verb_data:
    actual = conjugate_present_tense(item)
    diff = DeepDiff(actual, expected)
    print('Difference: ' , diff)