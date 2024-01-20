import sys
import os

from core import Grammar
from core.test.grammars import grammars
from core.types import GrammarType, Productions, Tuple
from fng import greibach_normal_form

def get_grammar() -> Tuple[GrammarType, str]:
    grammar: GrammarType = {}
    print(f"EPSILON: {Grammar.EPSILON}")
    first_non_terminal = 'S'
    while True:
        key = input("Ingrese la variable o enter: ")
        if not len(key):
            break
        productions: Productions = set()
        while True:
            production = input("Ingrese una produccion o enter: ")
            if not len(production):
                break
            productions.update({production})
        if not len(productions):
            continue
        if not len(grammar):
            first_non_terminal = key
        grammar[key] = productions
        print()
    if not len(grammar):
        print("La gramatica está vacia!")
        exit()
    return grammar, first_non_terminal

def run_gnf_test():
    for i, gr in enumerate(grammars):
        os.system('cls')
        greibach_normal_form(
            grammar=gr['grammar'],
            first_non_terminal=gr['first-non-terminal']
        )
        if i < len(grammars) - 1:
            input("siguiente...")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        grammar, first_non_terminal = get_grammar()
        greibach_normal_form(
            grammar=grammar,
            first_non_terminal=first_non_terminal)
    elif sys.argv[1] == '--test':
        run_gnf_test()
