from tkinter.ttk import Entry

import gurobipy as gp
from gurobipy import GRB
import tkinter as tk
from tkinter import messagebox


initial_populations = [2, 3, 4, 5, 6, 7, 8, 9, 10]
initial_adjacency_matrix = [

    [1, 1, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 1],
    [0, 0, 0, 1, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 0, 1, 1],
]



class BankBranchOptimization:
    def __init__(self, populations, adjacency_matrix, budget, branch_cost, dab_cost, a_coverage, b_coverage,
                 c_coverage):
        self.populations = populations
        self.adjacency_matrix = adjacency_matrix
        self.budget = budget
        self.branch_cost = branch_cost
        self.dab_cost = dab_cost
        self.a_coverage = a_coverage
        self.b_coverage = b_coverage
        self.c_coverage = c_coverage

    def run(self):
        model = gp.Model("BankBranchOptimization")


        branches = model.addVars(len(self.populations), vtype=GRB.BINARY, name="branches")
        dabs = model.addVars(len(self.populations), vtype=GRB.BINARY, name="dabs")


        model.setObjective(
            gp.quicksum(self.populations[i] * (self.a_coverage * branches[i] +
                                               self.b_coverage * dabs[i] +
                                               self.c_coverage * (1 - branches[i]) * (1 - dabs[i]))
                        for i in range(len(self.populations))), GRB.MAXIMIZE)


        model.addConstr(self.branch_cost * gp.quicksum(branches[i] for i in range(len(self.populations))) +
                        self.dab_cost * gp.quicksum(dabs[i] for i in range(len(self.populations))) <= self.budget,
                        "Budget")


        for i in range(len(self.adjacency_matrix)):
            for j in range(i + 1, len(self.adjacency_matrix[i])):
                if self.adjacency_matrix[i][j] == 1:
                    model.addConstr(branches[i] + branches[j] <= 1, f"Neighboring_{i}_{j}")

        model.optimize()


        branches_solution = model.getAttr('x', branches)
        dabs_solution = model.getAttr('x', dabs)
        return branches_solution, dabs_solution



def run_gui_optimization():
    try:

        budget = float(budget_entry.get())
        branch_cost = float(branch_cost_entry.get())
        dab_cost = float(dab_cost_entry.get())
        a_coverage = float(a_coverage_entry.get()) / 100  # Convert percentage to proportion
        b_coverage = float(b_coverage_entry.get()) / 100  # Convert percentage to proportion
        c_coverage = float(c_coverage_entry.get()) / 100  # Convert percentage to proportion
        populations = [float(population_entries[i].get()) for i in range(len(population_entries))]
        adjacency_matrix = [[float(adjacency_entries[i][j].get()) for j in range(9)] for i in range(9)]

        optimization_model = BankBranchOptimization(populations, adjacency_matrix, budget, branch_cost, dab_cost,
                                                    a_coverage, b_coverage, c_coverage)


        branches_solution, dabs_solution = optimization_model.run()


        result_text.delete('1.0', tk.END)  # Clear previous results
        result_text.insert(tk.END, "Optimal solution:\n")
        for i in range(len(populations)):
            branch_status = 'Yes' if branches_solution[i] > 0.5 else 'No'
            dab_status = 'Yes' if dabs_solution[i] > 0.5 else 'No'
            result_text.insert(tk.END, f"Region {i + 1} - Branch: {branch_status}, DAB: {dab_status}\n")

    except gp.GurobiError as e:
        messagebox.showerror("Gurobi Error", str(e))
    except ValueError:
        messagebox.showerror("Input Error", "Please ensure all inputs are numbers.")
    except Exception as e:
        messagebox.showerror("Error", str(e))



root = tk.Tk()
root.title("Bank Branch Optimization GUI")

tk.Label(root, text="Populations:").pack()
population_entries = []
for i in range(len(initial_populations)):
    frame = tk.Frame(root)
    label = tk.Label(frame, text=f"Region {i + 1}:")
    label.pack(side=tk.LEFT)
    entry = Entry(frame)
    entry.insert(0, str(initial_populations[i]))
    entry.pack(side=tk.LEFT)
    frame.pack()
    population_entries.append(entry)

# Create dynamic entry fields for adjacency matrix
tk.Label(root, text="Adjacency Matrix:").pack()
adjacency_entries = []
for i in range(9):
    frame = tk.Frame(root)
    row_entries = []
    for j in range(9):
        entry = Entry(frame, width=3)
        entry.insert(0, str(initial_adjacency_matrix[i][j]))
        entry.pack(side=tk.LEFT)
        row_entries.append(entry)
    frame.pack()
    adjacency_entries.append(row_entries)

budget_entry = tk.Entry(root)
branch_cost_entry = tk.Entry(root)
dab_cost_entry = tk.Entry(root)
a_coverage_entry = tk.Entry(root)
b_coverage_entry = tk.Entry(root)
c_coverage_entry = tk.Entry(root)


labels_entries = {
    "Total Budget (B)": budget_entry,
    "Branch Cost (K)": branch_cost_entry,
    "DAB Server Cost (D)": dab_cost_entry,
    "A Coverage (a)": a_coverage_entry,
    "B Coverage (b)": b_coverage_entry,
    "C Coverage (c)": c_coverage_entry
}

for label, entry in labels_entries.items():
    tk.Label(root, text=label).pack()
    entry.pack()


run_button = tk.Button(root, text="Run Optimization", command=run_gui_optimization)
run_button.pack()


result_text = tk.Text(root, height=20, width=60)
result_text.pack()


root.mainloop()
