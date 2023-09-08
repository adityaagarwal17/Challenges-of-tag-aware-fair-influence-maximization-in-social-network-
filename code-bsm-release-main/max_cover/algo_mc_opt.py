import timeit

import gurobipy as gp
from gurobipy import GRB

from max_cover.algo_mc import SetItem


def max_cover_ip(items: list[SetItem], k: int):
    start = timeit.default_timer()

    sol = list()
    n = len(items)
    m = len(items)

    try:
        model = gp.Model("max_cov")
        model.setParam(GRB.Param.TimeLimit, 600)

        vars_x = model.addVars(n, vtype=GRB.BINARY, name="x")

        obj_y = [1] * m
        vars_y = model.addVars(m, vtype=GRB.BINARY, obj=obj_y, name="y")

        model.modelSense = GRB.MAXIMIZE

        expr = gp.LinExpr()
        for j in range(n):
            expr.addTerms(1, vars_x[j])
        model.addConstr(expr <= k, "size")

        for i in range(m):
            expr = gp.LinExpr()
            for j in range(n):
                if i in items[j].elem:
                    expr.addTerms(1, vars_x[j])
            model.addConstr(expr >= vars_y[i], "cover_" + str(i))

        model.optimize()

        for j in range(n):
            if vars_x[j].X > 0.5:
                sol.append(j)

    except gp.GurobiError as error:
        print("Error code " + str(error))
        exit(0)
    end = timeit.default_timer()

    cov = set()
    for v in sol:
        cov.update(items[v].elem)

    return sol, cov, (end - start)


def robust_max_cover_ip(items: list[SetItem], k: int, attr: list[int], groups: list[set]):
    start = timeit.default_timer()

    sol = list()
    c = len(groups)
    n = len(items)
    m = len(items)

    try:
        model = gp.Model("robust_max_cov")
        model.setParam(GRB.Param.TimeLimit, 300)

        vars_x = model.addVars(n, vtype=GRB.BINARY, name="x")
        vars_y = model.addVars(m, vtype=GRB.BINARY, name="y")
        w = model.addVar(lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS, obj=1.0, name="w", column=None)

        model.modelSense = GRB.MAXIMIZE

        expr = gp.LinExpr()
        for j in range(n):
            expr.addTerms(1, vars_x[j])
        model.addConstr(expr <= k, "size")

        for i in range(m):
            expr = gp.LinExpr()
            for j in range(n):
                if i in items[j].elem:
                    expr.addTerms(1, vars_x[j])
            model.addConstr(expr >= vars_y[i], "cover_" + str(i))

        for cc in range(c):
            expr = gp.LinExpr()
            for u in groups[cc]:
                expr.addTerms(1 / len(groups[cc]), vars_y[u])
            model.addConstr(expr >= w, "maximin_" + str(cc))

        model.optimize()

        for j in range(n):
            if vars_x[j].X > 0.5:
                sol.append(j)

    except gp.GurobiError as error:
        print("Error code " + str(error))
        exit(0)
    end = timeit.default_timer()

    cov = set()
    for v in sol:
        cov.update(items[v].elem)

    return sol, cov, (end - start)


def bsm_max_cover_ip(items: list[SetItem], k: int, tau: float, opt_g: float, attr: list[int], groups: list[set]):
    start = timeit.default_timer()

    sol = list()
    c = len(groups)
    n = len(items)
    m = len(items)

    try:
        model = gp.Model("bsm_max_cov")
        model.setParam(GRB.Param.TimeLimit, 300)

        vars_x = model.addVars(n, vtype=GRB.BINARY, name="x")

        obj_y = [1] * m
        vars_y = model.addVars(m, vtype=GRB.BINARY, obj=obj_y, name="y")

        model.modelSense = GRB.MAXIMIZE

        expr = gp.LinExpr()
        for j in range(n):
            expr.addTerms(1, vars_x[j])
        model.addConstr(expr <= k, "size")

        for i in range(m):
            expr = gp.LinExpr()
            for j in range(n):
                if i in items[j].elem:
                    expr.addTerms(1, vars_x[j])
            model.addConstr(expr >= vars_y[i], "cover_" + str(i))

        for cc in range(c):
            expr = gp.LinExpr()
            for u in groups[cc]:
                expr.addTerms(1, vars_y[u])
            cap = tau * opt_g * len(groups[cc])
            model.addConstr(expr >= cap, "cap_" + str(cc))

        model.optimize()

        for j in range(n):
            if vars_x[j].X > 0.5:
                sol.append(j)

    except gp.GurobiError as error:
        print("Error code " + str(error))
        exit(0)
    end = timeit.default_timer()

    cov = set()
    for v in sol:
        cov.update(items[v].elem)

    return sol, cov, (end - start)
