from copy import copy

from cdcl import cdcl, Unsatisfiable

N = 8


def pack(row, column):
    return 100 * row + column


def flip_dim(pos):
    return (N // 2) - (pos - ((N // 2) + 1))


def print_result(result):
    for row in range(1, N + 1):
        cx = [
            "\x1b[32m Q \x1b[0m" if result.get(pack(row, column)) else "   "
            for column in range(1, N + 1)
        ]
        print("|".join(cx))


cnf = []
# every row should have at least 1 queen
for row in range(1, N + 1):
    clause = {}
    for column in range(1, N + 1):
        clause[pack(row, column)] = True
    cnf.append(clause)

# every row should have only 1 queen
for row in range(1, N + 1):
    for c1 in range(1, N):
        for c2 in range(c1 + 1, N + 1):
            clause = {
                pack(row, c1): False,
                pack(row, c2): False,
            }
            cnf.append(clause)

# every column should have at least 1 queen
for column in range(1, N + 1):
    clause = {}
    for row in range(1, N + 1):
        clause[pack(row, column)] = True
    cnf.append(clause)

# every column should have only 1 queen
for column in range(1, N + 1):
    for r1 in range(1, N):
        for r2 in range(r1 + 1, N + 1):
            clause = {
                pack(r1, column): False,
                pack(r2, column): False,
            }
            cnf.append(clause)

# every diagonal should have only 1 queen
for init_row1 in range(1, N):
    for init_row2 in range(init_row1 + 1, N + 1):
        for shift in range(-N, N):
            row1 = init_row1
            row2 = init_row2
            column1 = init_row1 + shift
            column2 = init_row2 + shift
            if 0 < column1 <= N and 0 < column2 <= N:
                clause = {
                    pack(row1, column1): False,
                    pack(row2, column2): False,
                }
                cnf.append(clause)

                clause = {
                    pack(flip_dim(column1), row1): False,
                    pack(flip_dim(column2), row2): False,
                }
                cnf.append(clause)

result = None
for i in range(100):
    try:
        result = cdcl(copy(cnf))
        print('')
        print(f'Sol: {i}')
        print_result(result)
        cnf.append({
            var: not val
            for var, val in result.items()
        })
    except Unsatisfiable:
        print(f'\n# total solutions: {i}')
        # https://en.wikipedia.org/wiki/Eight_queens_puzzle#Solutions
        assert i == 92
        break
