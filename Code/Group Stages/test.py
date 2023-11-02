from ortools.sat.python import cp_model

# Number of teams and matches
n_teams = 36
n_matches = 8

# Create a model
model = cp_model.CpModel()

# Decision variables
x = {}
y = {}
for i in range(n_teams):
    for j in range(n_teams):
        for k in range(n_matches):
            x[i, j, k] = model.NewBoolVar(f"x_{i}_{j}_{k}")
            y[i, j, k] = model.NewBoolVar(f"y_{i}_{j}_{k}")

# Constraints

# Each team plays 4 home and 4 away games
for i in range(n_teams):
    model.Add(sum(x[i, j, k] for j in range(n_teams) for k in range(n_matches)) == 4)
    model.Add(sum(y[i, j, k] for j in range(n_teams) for k in range(n_matches)) == 4)

# A team can't play against itself
for i in range(n_teams):
    for k in range(n_matches):
        model.Add(x[i, i, k] == 0)
        model.Add(y[i, i, k] == 0)

# A team can only play one game in each match k
for i in range(n_teams):
    for k in range(n_matches):
        model.Add(sum(x[i, j, k] + y[i, j, k] for j in range(n_teams)) == 1)

# Each team must play against teams from each pot
# Assuming the pots are divided as teams [0-8], [9-17], [18-26], [27-35]
pots = [range(0, 9), range(9, 18), range(18, 27), range(27, 36)]
for i in range(n_teams):
    for pot in pots:
        model.Add(sum(x[i, j, k] + y[i, j, k] for j in pot for k in range(n_matches)) == 2)  # One home, one away against each pot

# Solve the model and print out a possible scheduling
solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.FEASIBLE:
    for k in range(n_matches):
        for i in range(n_teams):
            for j in range(n_teams):
                if solver.Value(x[i, j, k]) == 1:
                    print(f"Match {k+1}: Team {i} (home) vs Team {j} (away)")
else:
    print("No solution found.")
