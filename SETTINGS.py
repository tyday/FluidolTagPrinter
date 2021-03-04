# import os, sys



OUTPUT_FILE = 'g_code_output.ngc'
SPACING = 0.0125            # extra spacing between characters
CENTERED = True             # Centers text. Otherwise it is left justified
Z_HEIGHT_ENGAGED = -0.005   # depth of router when engaged
Z_HEIGHT_DISENGAGED = 0.25  # Height of router when disengaged


TAG_TYPES = [
    ("Tag_large", "Large Tag"),
    ("Tag_small", "Small Tag"),
    ("Tag_special", "Special Tag"),
]

TAG_DEFINITIONS = {
    "Tag_large": {
        'name': 'Large Tag',
        'local_origin': [
            {'x':0.5,'y':0.5}, # Bottom left corner of the tag. Measured from the origin.
        ],
        'slots': [  # Name of the available slots. Needs corresponding definitions below
            'style',
            'shaft',
            'serial'
        ],
        'style': {
            'y': 0.3346457,     # Refers to the bottom of the style box
            'x1': 0.7480315,    # Refers to the left edge of the box
            'x2': 2.515748      # Refers to the right edge of the box
        },
        'serial': {
            'y': 0.1968504,
            'x1': 0.6692913,
            'x2': 1.377953
        },
        'shaft': {
            'y': 0.1968504,
            'x1': 1.889764,
            'x2': 2.519685
        },
        'font': 'isocp2__0p11.json' # Font selected in same directory as program
    },
    "Tag_small": { 
        'name': 'Small Tag',
        'local_origin': [
            {'x':3.75,'y':0.5},
        ],   
        'slots': [
            'style',
            'shaft',
            'serial'
        ],
        'style': {
            'y': 0.2952756,
            'x1':0.7283465,
            'x2': 2.125984
        },
        'serial': {
            'y': 0.1574803,
            'x1': 0.5905512,
            'x2': 1.259843
        },
        'shaft': {
            'y': 0.1574803,
            'x1': 1.653543,
            'x2': 2.283465
        },
        'font': 'isocp2__0p10.json'
    },
    "Tag_special": {
        'name': 'Special Tag',
        'local_origin': [
            {'x':6.75, 'y':0.5},
        ],
        'slots': [
            'style',
            'serial'
        ],
        'style': {
            'y': 0.5211,
            'x1': 0.0572,
            'x2': 1.1038
        },
        'serial': {
            'y': 0.08267717,
            'x1': 0.0572,
            'x2': 1.1038
        },
        'font': 'isocp2__0p10.json'
    }
}