import gurobipy as gp
from gurobipy import GRB
import tkinter as tk
from tkinter import messagebox


class AntennaPlacementOptimization:
    def run(self):
        model = gp.Model("AntennaPlacement")
        sites = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        antennas = model.addVars(sites, vtype=GRB.BINARY, name="antennas")


        model.setObjective(gp.quicksum(antennas[site] for site in sites), GRB.MINIMIZE)


        model.addConstr(antennas['A'] + antennas['B'] + antennas['C'] >= 1, "Zone1_Coverage")
        model.addConstr(antennas['A'] + antennas['E'] >= 1, "Zone2_Coverage")
        model.addConstr(antennas['B'] + antennas['D'] >= 1, "Zone3_Coverage")
        model.addConstr(antennas['C'] + antennas['D'] + antennas['E'] + antennas['G'] >= 2, "Zone4_Coverage")
        model.addConstr(antennas['F'] + antennas['G'] >= 1, "Zone5_Coverage")


        model.optimize()


        branches_solution = model.getAttr('x', antennas)
        return branches_solution


def run_optimization():
    try:
        optimization_model = AntennaPlacementOptimization()
        results = optimization_model.run()

        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Optimization Results:\n")
        for site, val in results.items():
            result_text.insert(tk.END, f"Site {site}: {'Place Antenna' if val > 0.5 else 'Do Not Place Antenna'}\n")
    except gp.GurobiError as e:
        messagebox.showerror("Gurobi Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Antenna Placement Optimization")

run_button = tk.Button(root, text="Run Optimization", command=run_optimization)
run_button.pack()

result_text = tk.Text(root, height=20, width=50)
result_text.pack()

root.mainloop()
