import re
import argparse
from typing import List, Dict, NamedTuple, Optional, Any

from utils import pprint_cnf, pprint_result


class Var(NamedTuple):
    name: int
    val: bool
    decision: bool = False
    reason: Optional[Dict[int, bool]] = None

    def __eq__(self, other: Any) -> bool:
        """just ignore reason"""
        if isinstance(other, Var):
            return (self.name == other.name and
                    self.val == other.val and
                    self.decision == other.decision)
        return False


Clause = Dict[int, bool]
CNF = List[Clause]
State = List[Var]
Result = Dict[int, bool]


class Unsatisfiable(Exception):
    clause = None

    def __init__(self, clause: Optional[Clause] = None) -> None:
        """
        Args:
            clause: clause that lead to unsat
        """
        self.clause = clause


def read_dimacs(dimacs_str: str) -> CNF:
    """Transforms DIMACS into inner representation of CNF

    https://people.sc.fsu.edu/~jburkardt/data/cnf/cnf.html

    Args:
        dimacs_str: string with DIMACS CNF
    Raises:
        Unsatisfiable: when same positive and negative variable in one clause
    Returns:
        Inner representation of CNF
    """
    cnf = []
    for line in re.split(r'\s*\n+\s*', dimacs_str.strip()):
        if line[0] in {'c', 'p'}:
            continue

        clause: Clause = {}
        variables = re.split(r'\s+', line)

        assert variables[-1] == '0'
        variables = variables[:-1]

        for var_str in variables:
            if var_str[0] == '-':
                val = False
                var_str = var_str[1:]
            else:
                val = True
            var = int(var_str)

            if var in clause and clause[var] != val:
                raise Unsatisfiable
            clause[var] = val
        cnf.append(clause)

    return cnf


def unit_resolution_once(cnf: CNF, state: State) -> State:
    """Iterate once over clauses and do unit propagation on CNF

    Args:
        cnf: CNF
        state: new state
    Raises:
        Unsatisfiable: when cannot satisfy CNF
    Returns:
        new updated state
    """
    # TODO
    pass


def unit_resolution(cnf: CNF, state: State) -> State:
    """Do unit resolution until stuck

    Args:
        cnf: CNF
        state: new state
    Raises:
        Unsatisfiable: when cannot satisfy CNF
    Returns:
        new updated state
    """
    previous_len = len(state)
    while True:
        state = unit_resolution_once(cnf, state)
        if len(state) > previous_len:
            previous_len = len(state)
        else:
            break
    return state


def cdcl(cnf: CNF, state: Optional[State] = None) -> Result:
    """
    CDCL algorithm

    Args:
        cnf: CNF of a problem
        state: optional State
    Raises:
        Unsatisfiable: when cannot satisfy CNF
    Returns:
        dictionary with result for all variables
    """
    # TODO
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dimacs", help="path to dimacs CNF file")
    args = parser.parse_args()
    dimacs = open(args.dimacs).read()
    cnf = read_dimacs(dimacs)
    pprint_cnf(cnf)
    result = cdcl(cnf)
    print('')
    pprint_result(result)
