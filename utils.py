def pprint_cnf(cnf):
    if len(cnf) > 10:
        print('!WARNING! showing only first 10 clauses')

    def _pprint_clause(clause):
        vars = [
            f'\x1b[32m{k}\x1b[0m' if v else f'!\x1b[31m{k}\x1b[0m'
            for k, v in sorted([(k, v) for k, v in clause.items()])
        ]
        vars = ' ∨ '.join(vars)
        return f'( {vars} )'

    cnf = [_pprint_clause(clause) for clause in cnf[:10]]
    print(' ∧ \n'.join(cnf))


def pprint_result(result):
    for i, var in enumerate(sorted(result.keys())):
        if i % 17 == 16:
            print('')
        print(f'\x1b[32m{var}\x1b[0m ' if result[var] else f'!\x1b[31m{var}\x1b[0m ', end='')
    print('')
