import tkinter as tk
from tkinter import messagebox

import gurobipy as gp
import numpy as np

class employe:
    def __init__(self, jours):
        self.jours = jours
        self.jour = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

    def run(self):
        jours_de_conges = np.ones((7, 7), dtype=int)
        for k in range(7):
            jours_de_conges[k, k] = 0
            jours_de_conges[k, (k + 1) % 7] = 0
        model = gp.Model("employe")
        x = model.addVars(7, lb=0, vtype=gp.GRB.INTEGER, name=['x' + str(i) for i in range(7)])
        model.setObjective(gp.quicksum(x[i] for i in range(7)), gp.GRB.MINIMIZE)



        for j in range(7):
            expr = gp.LinExpr()
            for i in range(7):
                expr.add(jours_de_conges[i, j] * x[i])
            model.addConstr(expr >= self.jours[j])

        model.optimize()


        nb = [int(v.x) for v in model.getVars()]
        result = {}
        for i in range(7):
            val = model.objVal - (nb[i] + nb[(i-1) % 7])
            result[str(i+1) + ' - ' + self.jour[i]] = " : %d employés" % val
        result["8 - Nombre d'employes"] = str(int(model.objVal))

        return result


def run_optimization():
    try:
        jobs = [int(day_entry.get()) for day_entry in day_entries]
        if len(jobs) != len(day_labels):
            raise ValueError("The number of job entries does not match the number of days.")

        optimization_model = employe(jobs)
        results = optimization_model.run()
        result_text.delete(1.0, tk.END)

        for day, employees in results.items():
            result_text.insert(tk.END, f"{day}: {employees}\n")
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("Job Optimization")
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10)

day_labels = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
day_entries = []

for i, day in enumerate(day_labels):
    tk.Label(input_frame, text=f"{day}:").grid(row=i, column=0)
    day_entry = tk.Entry(input_frame)
    day_entry.grid(row=i, column=1)
    day_entries.append(day_entry)

run_button = tk.Button(root, text="Run Optimization", command=run_optimization)
run_button.pack(pady=5)
result_text = tk.Text(root, height=10, width=50)
result_text.pack(pady=5)
root.mainloop()
