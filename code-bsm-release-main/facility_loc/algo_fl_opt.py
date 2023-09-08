import timeit

import gurobipy as gp
from gurobipy import GRB


def fl_ip(bmat: list[list[float]], k: int):
    start = timeit.default_timer()

    sol = list()
    n = len(bmat)
    m = len(bmat[0])

    try:
        model = gp.Model("facility_loc")
        model.setParam(GRB.Param.TimeLimit, 300)

        vars_x = model.addVars(n, vtype=GRB.BINARY, name="x")

        obj_y = [0] * (m * n)
        for i in range(m):
            for j in range(n):
                obj_y[i * m + j] = bmat[j][i]
        vars_y = model.addVars(m * n, vtype=GRB.BINARY, obj=obj_y, name="y")

        model.modelSense = GRB.MAXIMIZE

        expr = gp.LinExpr()
        for j in range(n):
            expr.addTerms(1, vars_x[j])
        model.addConstr(expr <= k, "size")

        for i in range(m):
            for j in range(n):
                expr = gp.LinExpr()
                expr.addTerms(1, vars_y[i * m + j])
                model.addConstr(expr <= vars_x[j], "select_" + str(i) + str(j))

        for i in range(m):
            expr = gp.LinExpr()
            for j in range(n):
                expr.addTerms(1, vars_y[i * m + j])
            model.addConstr(expr <= 1, "row_" + str(i))

        model.optimize()

        for j in range(n):
            if vars_x[j].X > 0.5:
                sol.append(j)

    except gp.GurobiError as error:
        print("Error code " + str(error))
        exit(0)
    end = timeit.default_timer()

    return sol, (end - start)


def robust_fl_ip(bmat: list[list[float]], k: int, attr: list[int], groups: list[set]):
    start = timeit.default_timer()

    sol = list()
    c = len(groups)
    n = len(bmat)
    m = len(bmat[0])

    try:
        model = gp.Model("robust_clustering")
        model.setParam(GRB.Param.TimeLimit, 300)

        vars_x = model.addVars(n, vtype=GRB.BINARY, name="x")
        vars_y = model.addVars(m * n, vtype=GRB.BINARY, name="y")

        w = model.addVar(lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS, obj=1.0, name="w", column=None)

        model.modelSense = GRB.MAXIMIZE

        expr = gp.LinExpr()
        for j in range(n):
            expr.addTerms(1, vars_x[j])
        model.addConstr(expr <= k, "size")

        for i in range(m):
            for j in range(n):
                expr = gp.LinExpr()
                expr.addTerms(1, vars_y[i * m + j])
                model.addConstr(expr <= vars_x[j], "select_" + str(i) + str(j))

        for i in range(m):
            expr = gp.LinExpr()
            for j in range(n):
                expr.addTerms(1, vars_y[i * m + j])
            model.addConstr(expr <= 1, "row_" + str(i))

        for cc in range(c):
            expr = gp.LinExpr()
            for i in groups[cc]:
                for j in range(n):
                    expr.addTerms(bmat[j][i] / len(groups[cc]), vars_y[i * m + j])
            model.addConstr(expr >= w, "maximin_" + str(cc))

        model.optimize()

        for j in range(n):
            if vars_x[j].X > 0.5:
                sol.append(j)

    except gp.GurobiError as error:
        print("Error code " + str(error))
        exit(0)
    end = timeit.default_timer()

    return sol, (end - start)


def bsm_fl_ip(bmat: list[list[float]], k: int, tau: float, opt_g: float, attr: list[int], groups: list[set]):
    start = timeit.default_timer()

    sol = list()
    c = len(groups)
    n = len(bmat)
    m = len(bmat[0])

    try:
        model = gp.Model("bsm_clustering")
        model.setParam(GRB.Param.TimeLimit, 300)

        vars_x = model.addVars(n, vtype=GRB.BINARY, name="x")

        obj_y = [0] * (m * n)
        for i in range(m):
            for j in range(n):
                obj_y[i * m + j] = bmat[j][i]
        vars_y = model.addVars(m * n, vtype=GRB.BINARY, obj=obj_y, name="y")

        model.modelSense = GRB.MAXIMIZE

        expr = gp.LinExpr()
        for j in range(n):
            expr.addTerms(1, vars_x[j])
        model.addConstr(expr <= k, "size")

        for i in range(m):
            for j in range(n):
                expr = gp.LinExpr()
                expr.addTerms(1, vars_y[i * m + j])
                model.addConstr(expr <= vars_x[j], "select_" + str(i) + str(j))

        for i in range(m):
            expr = gp.LinExpr()
            for j in range(n):
                expr.addTerms(1, vars_y[i * m + j])
            model.addConstr(expr <= 1, "row_" + str(i))

        for cc in range(c):
            expr = gp.LinExpr()
            for i in groups[cc]:
                for j in range(n):
                    expr.addTerms(bmat[j][i], vars_y[i * m + j])
            model.addConstr(expr >= tau * opt_g * len(groups[cc]), "constraint_" + str(cc))

        model.optimize()

        for j in range(n):
            if vars_x[j].X > 0.5:
                sol.append(j)

    except gp.GurobiError as error:
        print("Error code " + str(error))
        exit(0)
    end = timeit.default_timer()
    return sol, (end - start)
