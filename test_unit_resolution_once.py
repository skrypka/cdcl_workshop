import pytest

from cdcl import read_dimacs, unit_resolution_once, Var, Unsatisfiable


def test_without_single_variable():
    cnf = read_dimacs("""
    p cnf 2 1 
    1 2 0
    """)
    assert unit_resolution_once(cnf, []) == []


def test_only_single_variable():
    cnf = read_dimacs("""
    p cnf 1 1 
    1 0
    """)
    assert unit_resolution_once(cnf, []) == [Var(name=1, val=True)]

    cnf = read_dimacs("""
    p cnf 1 1 
    -1 0
    """)
    assert unit_resolution_once(cnf, []) == [Var(name=1, val=False)]

    cnf = read_dimacs("""
    p cnf 1 1 
    1 0
    """)
    assert unit_resolution_once(cnf, []) == [Var(name=1, val=True)]


def test_with_state():
    cnf = read_dimacs("""
    p cnf 2 1 
    1 2 0
    """)
    assert unit_resolution_once(cnf, [Var(name=1, val=False)]) == [Var(name=1, val=False), Var(name=2, val=True)]


def test_unsat_with_state():
    cnf = read_dimacs("""
    p cnf 2 1 
    1 2 0
    """)
    with pytest.raises(Unsatisfiable):
        unit_resolution_once(cnf, [Var(name=1, val=False), Var(name=2, val=False)])
