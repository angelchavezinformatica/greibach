from core.grammar import Grammar


def process_productions(grammar: Grammar):
    def decotator_process_productions(func):
        def decorator_function(*args, **kwars):
            for no_terminal in grammar.non_terminals:
                prods = grammar.grammar.get(no_terminal, set())
                func(no_terminal, prods.copy(), *args, **kwars)
        return decorator_function
    return decotator_process_productions
