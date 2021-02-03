# https://app.codility.com/programmers/task/cover_buildings/

from ortools.sat.python import cp_model

model = cp_model.CpModel()

heights = [1, 1, 7, 6, 6, 6]
max_height = max(heights)

banner1_width = model.NewIntVar(1, len(heights), "banner 1 width")
banner1_height = model.NewIntVar(1, max_height, "banner 1 height")
banner2_width = model.NewIntVar(0, len(heights), "banner 2 width")
model.Add(banner2_width == len(heights) - banner1_width)
banner2_height = model.NewIntVar(0, max_height, "banner 2 height")

banner1_area = model.NewIntVar(1, max_height * len(heights), "banner 1 area")
banner2_area = model.NewIntVar(0, max_height * len(heights), "banner 2 area")

model.AddMultiplicationEquality(banner1_area, [banner1_width, banner1_height])
model.AddMultiplicationEquality(banner2_area, [banner2_width, banner2_height])

covered_by_banner1_vars = []
covered_by_banner2_vars = []
for x, h in enumerate(heights):
    covered_by_banner1 = model.NewBoolVar("building %d/%d covered by banner 1" % (x, h))
    covered_by_banner2 = model.NewBoolVar("building %d/%d covered by banner 2" % (x, h))
    covered_by_banner1_vars.append(covered_by_banner1)
    covered_by_banner2_vars.append(covered_by_banner2)

    model.AddBoolOr([covered_by_banner1, covered_by_banner2])
    model.AddImplication(covered_by_banner1, covered_by_banner2.Not())
    model.AddImplication(covered_by_banner2, covered_by_banner1.Not())
    # if covered by banner 1:
    model.Add(x < banner1_width).OnlyEnforceIf(covered_by_banner1)
    model.Add(h <= banner1_height).OnlyEnforceIf(covered_by_banner1)
    # if covered by banner 2:
    model.Add(x >= banner1_width).OnlyEnforceIf(covered_by_banner2)
    model.Add(h <= banner2_height).OnlyEnforceIf(covered_by_banner2)

model.Minimize(banner1_area + banner2_area)

solver = cp_model.CpSolver()
solver.parameters.log_search_progress = True
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    for x, h in enumerate(heights):
        if solver.Value(covered_by_banner1_vars[x]):
            print("Building %d,%d is covered by banner 1" % (x,h))
        else:
            print("Building %d,%d is covered by banner 2" % (x,h))

