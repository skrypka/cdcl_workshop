import pytest

from cdcl import read_dimacs, Unsatisfiable
from two_sat import two_sat


def test_two_sat():
    cnf = read_dimacs("""
        p cnf X X
        1 2 0
        -1 -2 0
        1 -2 0
        -1 2 0
        """)
    with pytest.raises(Unsatisfiable):
        assert two_sat(cnf) is None

    cnf = read_dimacs("""
    p cnf X X
    -1 -2 0
    -1 2 0
    1 3 0
    4 5 0
    2 4 0
    """)
    assert two_sat(cnf) == {1: False, 3: True, 4: True, 5: True}
