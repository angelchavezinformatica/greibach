from core.utils.generate_combinations import generate_combinations

from core.grammar import Grammar
from core.types import GrammarType, SetStr, Tuple, UnitProductions
from core.utils.process_productions import process_productions


class Chomsky:
    EPSILON = Grammar.EPSILON

    def remove_epsilon_productions(
        self,
        grammar: Grammar
    ) -> Tuple[GrammarType, SetStr]:
        nullable: SetStr = set()

        @process_productions(grammar=grammar)
        def remove_epsilon(nt: str, prods: SetStr):
            if self.EPSILON in prods:
                prods.remove(self.EPSILON)
                nullable.add(nt)
                grammar.grammar[nt] = prods
        remove_epsilon()

        @process_productions(grammar=grammar)
        def get_nullable(nt: str, prods: SetStr):
            if len(nullable & prods):
                nullable.update(nt)

        for _ in range(len(grammar.non_terminals)):
            if not len(nullable):
                break
            aux = nullable.copy()
            get_nullable()
            if aux == nullable:
                break

        @process_productions(grammar=grammar)
        def generate_productions(nt: str, prods: SetStr):
            combs = generate_combinations(input_set=nullable)
            new_prods = prods.copy()
            for prod in prods:
                for comb in combs:
                    if comb in prod:
                        new_prod = prod.replace(comb, '')
                        if len(new_prod):
                            new_prods.update({new_prod})
            grammar.grammar[nt] = new_prods
        generate_productions()

        aux_grammar = grammar.grammar.copy()

        @process_productions(grammar=grammar)
        def remove_non_terminals(nt: str, prods: SetStr):
            if not len(prods):
                aux_grammar.pop(nt)
        remove_non_terminals()

        if aux_grammar != grammar.grammar:
            new_grammar = Grammar(grammar=aux_grammar)
            diff_non_terminals = set(
                grammar.non_terminals) - set(new_grammar.non_terminals)

            @process_productions(grammar=new_grammar)
            def clear_grammar(nt: str, prods: SetStr):
                new_prods = set()
                for diff in diff_non_terminals:
                    for prod in prods:
                        if diff not in prod:
                            new_prods.update({prod})
                if len(new_prods):
                    new_grammar.grammar[nt] = new_prods
                else:
                    new_grammar.grammar.pop(nt)
            clear_grammar()
            grammar = Grammar(grammar=new_grammar.grammar)

        return grammar.grammar, nullable

    def remove_unit_productions(
        self,
        grammar: Grammar
    ) -> Tuple[GrammarType, UnitProductions]:
        unit_productions: UnitProductions = {}

        @process_productions(grammar=grammar)
        def get_unit_productions(nt: str, prods: SetStr):
            unit_productions[nt] = {nt}
            new_prods = prods.copy()
            for prod in prods:
                if prod in grammar.non_terminals:
                    unit_productions[nt].update({prod})
                    new_prods.update(grammar.grammar[prod])
                    new_prods.remove(prod)
            grammar.grammar[nt] = new_prods
        get_unit_productions()

        return grammar.grammar, unit_productions

    def remove_non_generators(
        self,
        grammar: Grammar
    ) -> Tuple[GrammarType, SetStr]:
        generators: SetStr = {grammar.first_non_terminal}

        @process_productions(grammar=grammar)
        def get_generators(nt: str, prods: SetStr):
            for prod in prods:
                if prod in grammar.terminals:
                    generators.update({nt})
                    if generators == grammar.non_terminals:
                        break
        get_generators()

        if generators != grammar.non_terminals:
            non_generators = set(grammar.non_terminals) - generators
            new_grammar = grammar

            for n_gen in non_generators:
                for nt in grammar.non_terminals:
                    if nt in non_generators:
                        new_grammar.grammar.pop(nt)
                        continue
                    prods = grammar.grammar.get(nt, set())
                    n_prods: SetStr = set()
                    for prod in prods:
                        if n_gen not in prod:
                            n_prods.update({prod})
                    new_grammar.grammar[nt] = n_prods
                grammar = Grammar(
                    grammar=new_grammar.grammar,
                    first_non_terminal=new_grammar.first_non_terminal)

        return grammar.grammar, generators

    def remove_non_reachables(
        self,
        grammar: Grammar
    ) -> Tuple[GrammarType, SetStr]:
        reachables: SetStr = {grammar.first_non_terminal}
        all_productions = grammar.get_all_productions_as_str()

        for prod in all_productions:
            if prod in grammar.non_terminals:
                reachables.update({prod})
                if reachables == grammar.non_terminals:
                    break

        if reachables != grammar.non_terminals:
            new_grammar: GrammarType = {}
            for reachable in reachables:
                new_grammar[reachable] = grammar.grammar[reachable]
            grammar = Grammar(
                grammar=new_grammar,
                first_non_terminal=grammar.first_non_terminal)

        return grammar.grammar, reachables

    def remove_mixed_right_hand_side(
        self,
        grammar: Grammar
    ) -> GrammarType:
        new_grammar = grammar.grammar.copy()

        @process_productions(grammar=grammar)
        def add_non_terminals(nt: str, prods: SetStr):
            for terminal in grammar.terminals:
                for prod in prods:
                    if prod.islower():
                        continue
                    if terminal in prod:
                        new_grammar[f'V{terminal}'] = {terminal}
        add_non_terminals()

        return new_grammar

    def factorize_long_productions(
        self,
        grammar: Grammar
    ) -> GrammarType:
        def get_new_non_terminals_variables():
            nntv = ""
            upps = 'XYZABCDEFGHIJKLMNOPQRSTUVW'
            for upp in upps:
                if upp not in grammar.non_terminals:
                    nntv += upp
            return nntv

        nntv = get_new_non_terminals_variables()
        nnt = dict()
        new_grammar = grammar.grammar.copy()

        @process_productions(grammar=grammar)
        def factorize(nt: str, prods: SetStr):
            nonlocal nntv
            if nt.startswith('V'):
                return
            new_prods: SetStr = set()
            for prod in prods:
                new_prods.update({prod})
                if len(prod) >= 3:
                    value = prod[1:]

                    if value in nnt.keys():
                        key = nnt.get(value)
                    else:
                        key = nntv[0]
                        nnt[value] = key
                        new_grammar[key] = {value}
                        nntv = nntv[1:]

                    new_prods.remove(prod)
                    new_prods.update({prod.replace(value, key)})
            new_grammar[nt] = new_prods
        factorize()

        return new_grammar

    def format_grammar(
        self,
        grammar: Grammar
    ):
        new_grammar: GrammarType = {}

        @process_productions(grammar=grammar)
        def set_vs(nt: str, prods: SetStr):
            if nt.startswith('V'):
                new_grammar[nt] = grammar.grammar[nt]
                return
            new_prods: SetStr = set()
            for prod in prods:
                new_prod = ''
                if prod.islower():
                    new_prods.update({prod})
                    continue
                for char in prod:
                    if char in grammar.terminals:
                        new_prod += f'V{char}'
                        continue
                    new_prod += char
                new_prods.update({new_prod})
            new_grammar[nt] = new_prods
        set_vs()

        return new_grammar

    def convert(
        self,
        grammar: GrammarType,
        first_non_terminal: str
    ) -> GrammarType:
        gr, _ = self.remove_epsilon_productions(grammar=Grammar(
            grammar=grammar,
            first_non_terminal=first_non_terminal))
        gr, _ = self.remove_unit_productions(grammar=Grammar(
            grammar=gr,
            first_non_terminal=first_non_terminal))
        gr, _ = self.remove_non_generators(grammar=Grammar(
            grammar=gr,
            first_non_terminal=first_non_terminal))
        gr, _ = self.remove_non_reachables(grammar=Grammar(
            grammar=gr,
            first_non_terminal=first_non_terminal))
        gr = self.remove_mixed_right_hand_side(grammar=Grammar(
            grammar=gr,
            first_non_terminal=first_non_terminal))
        gr = self.factorize_long_productions(grammar=Grammar(
            grammar=gr,
            first_non_terminal=first_non_terminal))
        return gr
