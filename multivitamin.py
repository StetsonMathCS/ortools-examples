# https://app.codility.com/programmers/task/multivitamin/

from ortools.sat.python import cp_model
import random

model = cp_model.CpModel()

juice = [1, 2, 3, 4]
capacity = [3, 6, 4, 4]
#juice = [10, 2, 1, 1]
#capacity = [10, 3, 2, 2]
#juice = [2, 3]
#capacity = [3, 4]
#juice = [1, 1, 5]
#capacity = [6, 5, 8]

#juice = []
#capacity = []
#for i in range(10):
#    juice.append(random.randint(1, 10))
#    capacity.append(random.randint(juice[i], 20))

destination_glass_matrix = []
not_pouring = []
for i in range(len(juice)):
    destination_glass_row = []
    for j in range(len(juice)):
        destination_glass_row.append(model.NewBoolVar("juice %d is moving to glass %d" % (i,j)))
    not_pouring.append(model.NewBoolVar("juice %d is not pouring" % i))
    model.Add(not_pouring[i] == destination_glass_row[i])
    model.Add(sum(destination_glass_row) == 1)
    destination_glass_matrix.append(destination_glass_row)

dest_glass_pos_vars = []
for i in range(len(juice)):
    dest_glass_pos = model.NewIntVar(0, len(juice)-1, "destination of juice %d" % i)
    dest_glass_pos_vars.append(dest_glass_pos)
    model.Add(dest_glass_pos == cp_model.LinearExpr.ScalProd(destination_glass_matrix[i], list(range(len(juice)))))
    dest_glass_unpoured = model.NewBoolVar("ensure destination doesn't pour for glass %d" % i)
    model.AddElement(dest_glass_pos, not_pouring, dest_glass_unpoured)
    model.Add(dest_glass_unpoured == True)

capacity_moved_vars = []
shared_moved_vars = []
for j in range(len(juice)): # per column
    # i represents a particular glass with a capacity;
    # each true in the row means that juice moves here,
    # so we sum the juices that moved here and make sure it's less than capacity
    juices_here = []
    for i in range(len(juice)): # per row in this column
        juices_here.append(destination_glass_matrix[i][j])
    capacity_moved = model.NewIntVar(0, 10000000, "filled capacity for this glass %d" % j)
    model.Add(capacity_moved == cp_model.LinearExpr.ScalProd(juices_here, juice))
    model.Add(capacity_moved <= capacity[j])
    capacity_moved_vars.append(capacity_moved)
    shared_moved_vars.append(model.NewIntVar(0,len(juice), "# that moved to this glass %d" % j))
    model.Add(shared_moved_vars[j] == sum(juices_here))

shared_moved_max = model.NewIntVar(0, len(juice), "shared moved max")
model.AddMaxEquality(shared_moved_max, shared_moved_vars)
model.Maximize(shared_moved_max)

solver = cp_model.CpSolver()
solver.parameters.log_search_progress = True
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    for j in range(len(juice)):
        print("Juices in glass %d = %d" % (j, solver.Value(shared_moved_vars[j])))
    for i in range(len(juice)):
        print("Destination for juice %d = %d" % (i, solver.Value(dest_glass_pos_vars[i])))
        print("Not pouring? for juice %d = %d" % (i, solver.Value(not_pouring[i])))
    for i in range(len(juice)):
        for j in range(len(juice)):
            print(str(solver.Value(destination_glass_matrix[i][j])) + " ", end="")
        print()
    for i in range(len(juice)):
        print("Capacity for glass %d = %d" % (i, solver.Value(capacity_moved_vars[i])))
        for j in range(len(juice)):
            if solver.Value(destination_glass_matrix[i][j]) and i != j:
                print("Juice %d moved to glass %d" % (i,j))



