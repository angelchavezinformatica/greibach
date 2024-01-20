from core.chomsky import Chomsky
from core.greibach import Greibach
from core.grammar import Grammar

from core.types import GrammarType, SetStr


def print_grammar(grammar: GrammarType, errors: SetStr = set()):
    for key, value in grammar.items():
        print(f"\t{key} → {' | '.join(value)}", end='')
        if key[1:] in errors:
            print(" (ERROR)", end='')
        print()

def print_grammar_format(grammar: GrammarType, first_non_terminal: str, errors: SetStr = set()):
    print_grammar(grammar=Greibach().format_grammar(grammar=Grammar(
        grammar=grammar,
        first_non_terminal=first_non_terminal)),
        errors=errors)
    print()

def greibach_normal_form(grammar: GrammarType, first_non_terminal: str):
    gch = Greibach()
    print("GRAMMAR:")
    print_grammar(grammar=grammar)
    print("\n1. Convertir a Forma Normal de Chomsky")
    grammar = gch.cfg_to_cnf(grammar=Grammar(
        grammar=grammar,
        first_non_terminal=first_non_terminal))
    print_grammar(grammar=Chomsky().format_grammar(grammar=Grammar(
        grammar=grammar,
        first_non_terminal=first_non_terminal)))
    print()
    
    print("\n2. Renombrar variables en orden creciente")
    grammar, renames = gch.rename_variables(grammar=Grammar(
        grammar=grammar,
        first_non_terminal=first_non_terminal))
    first_non_terminal = renames[first_non_terminal]
    
    for key, value in renames.items():
        print(f"\t{key} ≡ A{value}")
    print()
    print_grammar_format(grammar=grammar, first_non_terminal=first_non_terminal)
    input("continuar...")
    
    
    print("\n3. Transformar las producciones en la forma Ar → Asα, donde r <= s")
    grammar = gch.transform_productions(grammar=Grammar(
        grammar=grammar,
        first_non_terminal=first_non_terminal))
    print_grammar_format(grammar=grammar, first_non_terminal=first_non_terminal)
    input("continuar...")

    print("\n4. Excluir recursiones Ar → Asα")
    grammar = gch.exclude_recursions(grammar=Grammar(
        grammar=grammar,
        first_non_terminal=first_non_terminal))
    print_grammar_format(grammar=grammar, first_non_terminal=first_non_terminal)
    input("continuar...")
    
    print("\n5. Un terminal en el incio del lado directo de cada produccion")
    grammar, errors = gch.terminal_left_hand_side(grammar=Grammar(
        grammar=grammar,
        first_non_terminal=first_non_terminal))
    print_grammar_format(
        grammar=grammar, first_non_terminal=first_non_terminal, errors=errors)
    input("continuar...")
    
    print("\n6. Produccion en la Forma Normal de Greibach")
    grammar = gch.greibach_normal_form(
            grammar=Grammar(grammar=grammar, first_non_terminal=first_non_terminal),
            errors=errors)
    print_grammar_format(grammar=grammar, first_non_terminal=first_non_terminal)
    
    grammar, errors = gch.terminal_left_hand_side(grammar=Grammar(
            grammar=grammar,
            first_non_terminal=first_non_terminal))
    while len(errors):
        grammar = gch.greibach_normal_form(
            grammar=Grammar(grammar=grammar, first_non_terminal=first_non_terminal),
            errors=errors)
        print_grammar_format(grammar=grammar, first_non_terminal=first_non_terminal)
        grammar, errors = gch.terminal_left_hand_side(grammar=Grammar(
            grammar=grammar,
            first_non_terminal=first_non_terminal))
    