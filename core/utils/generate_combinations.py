from itertools import permutations
from core.types import SetStr


def generate_combinations(input_set: SetStr) -> SetStr:
    return {''.join(p) for r in range(1, len(input_set) + 1)
            for p in permutations(input_set, r)}
