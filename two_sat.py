from cdcl import unit_resolution, Unsatisfiable, Var
from collections import deque, Counter


class Graph:
    adjustment_list = None
    post_order = None
    scc = None

    def __init__(self, edges):
        self.adjustment_list = {}
        for from_vertex, to_vertex in edges:
            if from_vertex not in self.adjustment_list:
                self.adjustment_list[from_vertex] = []
            self.adjustment_list[from_vertex].append(to_vertex)

        print(self.adjustment_list)

    def reversed(self) -> 'Graph':
        edges = set()
        for from_vertex in self.adjustment_list.keys():
            for to_vetrex in self.adjustment_list[from_vertex]:
                edges.add((to_vetrex, from_vertex))
        return Graph(edges)

    def dfs(self, vertices=None):
        self.scc = []
        self.post_order = []

        marked = set()
        if not vertices:
            vertices = self.adjustment_list.keys()
        queue = deque()
        for starting_vertex in vertices:
            if starting_vertex not in marked:
                queue.appendleft(starting_vertex)
            else:
                continue
            current_scc = set()
            while len(queue):
                vertex = queue.popleft()
                current_scc.add(vertex)
                if vertex in marked:
                    self.post_order.append(vertex)
                else:
                    queue.appendleft(vertex)
                    marked.add(vertex)
                    for to_vertex in self.adjustment_list.get(vertex, []):
                        if to_vertex not in marked:
                            queue.appendleft(to_vertex)
            self.scc.append(current_scc)

        self.post_order = list(reversed(self.post_order))
        return self


def two_sat(cnf):
    all_variables = set()
    [all_variables.update(set(clause.keys())) for clause in cnf]

    state = []
    while True:
        state = unit_resolution(cnf, state)
        if len(state) == len(all_variables):
            return {var.name: var.val for var in state}

        state_dict = {var.name: var.val for var in state}

        # create implication graph
        edges = set()
        unresolved_clause = False
        for clause in cnf:
            # skip clause if any variables already true
            skip_clause = False
            for clause_var, clause_val in clause.items():
                if state_dict.get(clause_var) is clause_val:
                    skip_clause = True
            if skip_clause:
                continue

            unresolved_clause = True

            vars = list(clause.items())
            assert len(vars) == 2
            (var0, val0), (var1, val1) = vars
            edges.add((
                (var0, not val0),
                (var1, val1),
            ))
            edges.add((
                (var1, not val1),
                (var0, val0),
            ))
        if not unresolved_clause:
            return {var.name: var.val for var in state}

        graph = Graph(edges)
        # run DFS with post orders on reverse graph
        scc_sink_orders = graph.reversed().dfs().post_order
        # find SCC
        graph.dfs(scc_sink_orders)

        # check for complement variable onside one SCC
        for scc in graph.scc:
            c = Counter([var for var, val in scc])
            if c.most_common(1)[0][1] != 1:
                raise Unsatisfiable

        # satisfy source SCC
        for val, var in graph.scc[0]:
            state.append(Var(val, var))
