grammars = [
    {
        'grammar': {
            'S': {'AB', 'bA', 'A'},
            'A': {'aAS', 'a', 'ε'},
            'B': {'SbB', 'AB', 'bB'}
        },
        'first-non-terminal': 'S'
    },
    {
        'grammar': {
            'S': {'A', 'AA', 'AAA'},
            'A': {'ABa', 'ACa', 'a'},
            'B': {'ABa', 'Ab', 'ε'},
            'C': {'Cab', 'CC'},
            'D': {'CD', 'Cd', 'CEa'},
            'E': {'b'}
        },
        'first-non-terminal': 'S'
    },
    {
        'grammar': {
            'R': {'bAA', 'a', 'b', 'bA'},
            'A': {'a', 'Rq', 'q'}
        },
        'first-non-terminal': 'R'
    },
    {
        'grammar': {
            'S': {'aSA', 'BSB', 'D'},
            'A': {'C'},
            'C': {'a'},
            'B': {'b'},
            'D': {'ε'}
        },
        'first-non-terminal': 'S'
    },
    {
        'grammar': {
            'D': {'eEM', 'Mm', 'mD', 'ε'},
            'E': {'ED', 'eM', 'm'},
            'M': {'dD', 'eE', 'e'}
        },
        'first-non-terminal': 'D'
    }
]
