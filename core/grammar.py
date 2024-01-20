from .types import GrammarType, TupleStr, SetStr


class Grammar:
    EPSILON = 'ε'

    def __init__(
        self,
        grammar: GrammarType,
        first_non_terminal: str = 'S'
    ) -> None:
        self.first_non_terminal: str = first_non_terminal
        self.grammar: GrammarType = self._sort_grammar(grammar)
        self.non_terminals = self._get_non_terminals()
        self.terminals = self._get_terminals()

    def _sort_grammar(self, grammar: GrammarType) -> GrammarType:
        if grammar.get(self.first_non_terminal) is None:
            raise Exception("The non_terminal variable "
                            f"'{self.first_non_terminal}' does not exist.")
        return dict(
            sorted(
                grammar.items(),
                key=lambda item: (
                    int(item[0] != self.first_non_terminal),
                    item[0])))

    def _get_non_terminals(self) -> TupleStr:
        return tuple(self.grammar.copy().keys())

    def _get_terminals(self) -> TupleStr:
        productions = "".join(self._get_all_productions())
        return tuple(prod for prod in productions
                     if prod.islower() and prod != self.EPSILON)

    def _get_all_productions(self) -> SetStr:
        return {prod for no_terminal in self.non_terminals
                for prod in self.grammar.get(no_terminal, set())}

    def get_all_productions_as_str(self) -> str:
        return "".join(self._get_all_productions())
