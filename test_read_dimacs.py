import pytest
from cdcl import read_dimacs, Unsatisfiable


def test_read_dimacs():
    # test simplest DIMACS .cnf file
    dimacs = """p cnf 1 1
1 0"""
    assert read_dimacs(dimacs) == [
        {1: True},
    ]

    # test DIMACS with negation
    dimacs = """p cnf 1 1
    -1 0"""
    assert read_dimacs(dimacs) == [
        {1: False},
    ]

    # test comments
    dimacs = """
    c Just comment
    p cnf 1 1
    -1 0"""
    assert read_dimacs(dimacs) == [
        {1: False},
    ]

    # test complicated CNF
    dimacs = """
        c A sample .cnf file.
        p cnf 3 2
        1 -3 0
        2 3 -1 0"""
    assert read_dimacs(dimacs) == [
        {1: True, 3: False},
        {2: True, 3: True, 1: False}
    ]

    # test basic unsatisfiable cnf
    dimacs = """
    c A sample .cnf file.
    p cnf 1 1
    1 -1 0"""
    with pytest.raises(Unsatisfiable):
        read_dimacs(dimacs)
