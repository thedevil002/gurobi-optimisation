import tkinter as tk
from tkinter import messagebox
import gurobipy as gp
from gurobipy import GRB


def solve_lp(entries):
    try:

        values = {cult: {param: float(entries[cult][param].get()) for param in params} for cult in cultures}
        irrigation_water = float(entries['irrigation_water'].get())
        machine_hours = float(entries['machine_hours'].get())
        labor = float(entries['labor'].get())


        m = gp.Model("agriculture")


        x = m.addVars(cultures, name="cultures")


        m.setObjective(
            gp.quicksum(
                x[cult] * (values[cult]['yield'] * values[cult]['price'] -
                           values[cult]['labor'] * values[cult]['labor_cost'] -
                           values[cult]['machine_time'] * 30 -
                           values[cult]['water'] * 0.1 - values[cult]['fixed_cost'])
                for cult in cultures), GRB.MAXIMIZE)


        m.addConstr(gp.quicksum(x[cult] * values[cult]['labor'] for cult in cultures) <= labor, "Labor")
        m.addConstr(x.sum() <= 1000, "TotalArea")
        m.addConstr(gp.quicksum(x[cult] * values[cult]['machine_time'] for cult in cultures) <= machine_hours, "MachineHours")
        m.addConstr(gp.quicksum(x[cult] * values[cult]['water'] for cult in cultures) <= irrigation_water, "IrrigationWater")


        m.optimize()


        result = ""
        for cult in cultures:
            result += f"{cult} hectares: {x[cult].x}\n"
        result += f"Optimal profit: {m.objVal}"

        messagebox.showinfo("Optimization Result", result)

    except gp.GurobiError as e:
        messagebox.showerror("Gurobi Error", e.message)

    except Exception as e:
        messagebox.showerror("Error", str(e))


params = ['yield', 'price', 'labor', 'machine_time', 'water', 'labor_cost', 'fixed_cost']
cultures = ['Blé', 'Orge', 'Mais', 'Bet-sucr', 'Tournesol']


root = tk.Tk()
root.title("Agricultural Zone Optimization")
default_values = {
    'Blé': {'yield': 75, 'price': 60, 'labor': 2, 'machine_time': 30, 'water': 3000, 'labor_cost': 500, 'fixed_cost': 250},
    'Orge': {'yield': 60, 'price': 50, 'labor': 1, 'machine_time': 24, 'water': 2000, 'labor_cost': 500, 'fixed_cost': 180},
    'Mais': {'yield': 55, 'price': 66, 'labor': 2, 'machine_time': 20, 'water': 2500, 'labor_cost': 600, 'fixed_cost': 190},
    'Bet-sucr': {'yield': 50, 'price': 110, 'labor': 3, 'machine_time': 28, 'water': 3800, 'labor_cost': 700, 'fixed_cost': 310},
    'Tournesol': {'yield': 60, 'price': 60, 'labor': 2, 'machine_time': 25, 'water': 3200, 'labor_cost': 550, 'fixed_cost': 320}
}


entries = {cult: {param: tk.StringVar(value=default_values[cult][param]) for param in params} for cult in cultures}
entries['irrigation_water'] = tk.StringVar(value="25000000")
entries['machine_hours'] = tk.StringVar(value="24000")
entries['labor'] = tk.StringVar(value="3000")



input_frame = tk.Frame(root)
input_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



entries = {}
for cult, params in default_values.items():
    frame = tk.LabelFrame(input_frame, text=cult)
    frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    entries[cult] = {}
    for row, (param, value) in enumerate(params.items()):
        tk.Label(frame, text=param).grid(row=row, column=0)
        entry = tk.Entry(frame, width=10)
        entry.insert(0, str(value))
        entry.grid(row=row, column=1)
        entries[cult][param] = entry


solve_button_frame = tk.Frame(root)
solve_button_frame.pack(side=tk.BOTTOM, fill=tk.X)
solve_button = tk.Button(solve_button_frame, text="Solve LP", command=lambda: solve_lp(entries))
solve_button.pack(side=tk.RIGHT, padx=10, pady=10)

additional_params_frame = tk.Frame(root)
additional_params_frame.pack(fill="both", expand="yes", padx=10, pady=5)
tk.Label(additional_params_frame, text="Irrigation water (m3)").grid(row=0, column=0)
irrigation_water_entry = tk.Entry(additional_params_frame)
irrigation_water_entry.insert(0, "25000000")
irrigation_water_entry.grid(row=0, column=1)

tk.Label(additional_params_frame, text="Machine hours").grid(row=1, column=0)
machine_hours_entry = tk.Entry(additional_params_frame)
machine_hours_entry.insert(0, "24000")
machine_hours_entry.grid(row=1, column=1)

tk.Label(additional_params_frame, text="Labor").grid(row=2, column=0)
labor_entry = tk.Entry(additional_params_frame)
labor_entry.insert(0, "3000")
labor_entry.grid(row=2, column=1)

entries['irrigation_water'] = irrigation_water_entry
entries['machine_hours'] = machine_hours_entry
entries['labor'] = labor_entry


root.mainloop()
