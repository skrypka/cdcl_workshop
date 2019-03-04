import pytest

from cdcl import read_dimacs, unit_resolution, Var, Unsatisfiable


def test_sat():
    cnf = read_dimacs("""
    p cnf 3 3 
    -1 -2 3 0
    -1 2 0
    1 0
    """)
    assert unit_resolution(cnf, []) == [Var(1, True), Var(2, True), Var(3, True)]


def test_unsat():
    cnf = read_dimacs("""
    p cnf 2 3
    1 -2 0
    -1 -2 0
    2 0
    """)
    with pytest.raises(Unsatisfiable):
        print(unit_resolution(cnf, []))
