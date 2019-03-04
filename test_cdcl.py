import pytest

from cdcl import cdcl, read_dimacs, Unsatisfiable


def test_sat():
    cnf = read_dimacs("""
    p cnf 3 3 
    -1 -2 3 0
    -1 2 0
    1 0
    """)
    assert cdcl(cnf) == {1: True, 2: True, 3: True}


def test_unsat():
    cnf = read_dimacs("""
    p cnf 1 2 
    1 0
    -1 0
    """)
    with pytest.raises(Unsatisfiable):
        cdcl(cnf)
