from core.utils.process_productions import process_productions

from .chomsky.chomsky import Chomsky
from .grammar import Grammar
from .types import Dict, GrammarType, SetStr, Tuple


class Greibach:
    EPSILON = Chomsky.EPSILON

    def cfg_to_cnf(
        self,
        grammar: Grammar
    ) -> GrammarType:
        return Chomsky().convert(
            grammar=grammar.grammar,
            first_non_terminal=grammar.first_non_terminal)

    def rename_variables(
        self,
        grammar: Grammar
    ) -> Tuple[GrammarType, Dict]:
        renames = {}
        new_grammar: GrammarType = {}

        for i, nt in enumerate(grammar.non_terminals):
            renames[nt] = f'{i + 1}'

        @process_productions(grammar=grammar)
        def rename(nt: str, prods: SetStr):
            new_prods = set()
            for prod in prods:
                new_prod = ''
                if prod.islower():
                    new_prods.update({prod})
                    continue
                for char in prod:
                    if char.islower():
                        new_prod += renames.get(f'V{char}')
                        continue
                    new_prod += renames.get(char, char)
                new_prods.update({new_prod})
            new_grammar[renames[nt]] = new_prods
        rename()

        return new_grammar, renames

    def transform_productions(
        self,
        grammar: Grammar
    ) -> GrammarType:
        @process_productions(grammar=grammar)
        def transform(nt: str, prods: SetStr):
            new_prods: SetStr = set()
            for prod in prods:
                if prod[0].isnumeric() and int(nt) > int(prod[0]):
                    for pr in grammar.grammar[prod[0]]:
                        new_prods.update({f'{pr}{prod[1:]}'})
                    continue
                new_prods.update({prod})
            grammar.grammar[nt] = new_prods
        transform()

        return grammar.grammar

    def exclude_recursions(
        self,
        grammar: Grammar
    ) -> GrammarType:
        recursions: SetStr = set()

        @process_productions(grammar=grammar)
        def get_recursions(nt: str, prods: SetStr):
            for prod in prods:
                if prod[0].isnumeric() and int(nt) == int(prod[0]):
                    recursions.update({nt})
        get_recursions()

        if not len(recursions):
            return grammar.grammar

        new_grammar: GrammarType = grammar.grammar.copy()

        for nt in recursions:
            new_grammar[nt] = set()
            new_grammar[f"{nt}'"] = set()
            for prod in grammar.grammar[nt]:
                if prod[0] != nt:
                    new_grammar[nt].update({f"{prod}{nt}'"})
                    continue
                new_grammar[f"{nt}'"].update({f"{prod[1:]}{nt}'",
                                             f'{prod[1:]}'})

        return new_grammar

    def terminal_left_hand_side(
        self,
        grammar: Grammar
    ) -> Tuple[GrammarType, SetStr]:
        errors: SetStr = set()

        @process_productions(grammar=grammar)
        def get_errors(nt: str, prods: SetStr):
            for prod in prods:
                if prod[0] not in grammar.terminals:
                    errors.update({nt})
        get_errors()

        return grammar.grammar, errors

    def greibach_normal_form(
        self,
        grammar: Grammar,
        errors: SetStr
    ) -> GrammarType:
        @process_productions(grammar=grammar)
        def greibach(nt: str, prods: SetStr):
            if nt not in errors:
                return
            new_prods: SetStr = set()
            for prod in prods:
                if prod[0].isnumeric():
                    for pr in grammar.grammar[prod[0]]:
                        new_prods.update({f'{pr}{prod[1:]}'})
                    continue
                new_prods.update({prod})
            grammar.grammar[nt] = new_prods
        greibach()

        return grammar.grammar

    def format_grammar(
        self,
        grammar: Grammar
    ) -> GrammarType:
        new_grammar: GrammarType = {}
        
        @process_productions(grammar=grammar)
        def format(nt: str, prods: SetStr):
            new_prods: SetStr = set()
            for prod in prods:
                new_prod = ""
                for pr in prod:
                    if pr.isnumeric():
                        new_prod += f"A{pr}"
                        continue
                    new_prod += pr
                new_prods.update({new_prod})
            new_grammar[f'A{nt}'] = new_prods
        format()
        
        return new_grammar
