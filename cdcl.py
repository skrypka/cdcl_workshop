import itertools
import re
import random
import argparse
import sys
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
CNF = List[Dict[int, bool]]
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
    """Iterate once over clauses and do unit propogation on CNF

    Args:
        cnf: CNF
        state: new state
    Raises:
        Unsatisfiable: when cannot satisfy CNF
    Returns:
        new updated state
    """
    state_dict = {var.name: var.val for var in state}
    state_vars = set(state_dict.keys())

    for clause in cnf:
        # skip clause if any variables already true
        skip_clause = False
        for clause_var, clause_val in clause.items():
            if state_dict.get(clause_var) is clause_val:
                skip_clause = True
        if skip_clause:
            continue

        # find left unsat clause variables
        clause_vars = set(clause.keys())
        left_vars = clause_vars - state_vars

        # unsat: because all variables is False
        if len(left_vars) == 0:
            raise Unsatisfiable(clause=clause)
        # if only one left - make it true
        elif len(left_vars) == 1:
            name = next(iter(left_vars))
            new_var = Var(name=name, val=clause[name], reason=clause)
            state.append(new_var)
            return state

    return state


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
    if not state:
        state = []
    all_clauses = {frozenset(clause.items()) for clause in cnf}

    all_variables = set()
    [all_variables.update(set(clause.keys())) for clause in cnf]

    total_decisions = None
    new_clauses = 0
    for iteration in itertools.count():
        # print progress
        if iteration % 1000 == 0:
            sys.stdout.write(f'progress {iteration}: state_len={len(state)}/{len(all_variables)}; total_decisions={total_decisions}; new_clauses={new_clauses}' + ' ' * 10)
            sys.stdout.write('\r')
            sys.stdout.flush()

        try:
            state = unit_resolution(cnf, state)
        except Unsatisfiable as e:
            total_decisions = 0
            last_decision_index = None
            for i, var in enumerate(state):
                if var.decision:
                    last_decision_index = i
                    total_decisions += 1
            if last_decision_index is None:
                raise
            else:
                # maybe learn clause
                if e.clause and state[-1].reason and state[-1].decision is False:
                    conflict_var1 = state[-1]
                    conflict_clause1 = e.clause
                    conflict_clause2 = conflict_var1.reason
                    new_clause = {**conflict_clause1, **conflict_clause2}
                    new_clause.pop(conflict_var1.name)
                    new_clause_frozen = frozenset(new_clause.items())

                    if new_clause_frozen not in all_clauses:
                        all_clauses.add(new_clause_frozen)
                        cnf.append(new_clause)
                        new_clauses += 1

                # do backtrack
                last_decision_var = state[last_decision_index]
                var = Var(last_decision_var.name, not last_decision_var.val, decision=False)
                state[last_decision_index] = var
                state = state[:last_decision_index + 1]
                continue

        if len(state) == len(all_variables):
            return {var.name: var.val for var in state}

        # in smart way set some variable
        current_vars = {var.name for var in state}
        name = random.choice(list(all_variables - current_vars))
        var = Var(name=name, val=True, decision=True)
        state.append(var)


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
