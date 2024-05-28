import tkinter as tk
from tkinter import messagebox
from gurobipy import Model, GRB, quicksum

class shoes:
    def __init__(self, C, Cs, D, Ouv, Sal, Hsup, R, L, h, H, Hmax, StockInit):
        self.C = C
        self.Cs = Cs
        self.D = D
        self.Ouv = Ouv
        self.Sal = Sal
        self.Hsup = Hsup
        self.R = R
        self.L = L
        self.h = h
        self.H = H
        self.Hmax = Hmax
        self.StockInit = StockInit

    def run(self):
        model = Model()


        NHS = model.addVars(range(4), vtype=GRB.INTEGER, lb=0, name="NHS")
        NCH = model.addVars(range(4), vtype=GRB.INTEGER, lb=0, name="NCH")
        NOR = model.addVars(range(4), vtype=GRB.INTEGER, lb=0, name="NOR")
        NOL = model.addVars(range(4), vtype=GRB.INTEGER, lb=0, name="NOL")
        S = model.addVars(range(5), vtype=GRB.INTEGER, lb=0, name="S")
        NO = model.addVars(range(5), vtype=GRB.INTEGER, lb=0, name="NO")


        obj = (quicksum(self.Cs * S[i] for i in range(4)) +
               quicksum(self.Sal * NO[i] for i in range(4)) +
               quicksum(self.Hsup * NHS[i] for i in range(4)) +
               quicksum(self.R * NOR[i] for i in range(4)) +
               quicksum(self.L * NOL[i] for i in range(4)) +
               quicksum(self.C * NCH[i] for i in range(4)))
        model.setObjective(obj, GRB.MINIMIZE)



        for i in range(4):
            model.addConstr(NHS[i] <= self.Hmax * NO[i])

        for i in range(4):
            model.addConstr(S[i] + NCH[i] >= self.D[i])

        for i in range(4):
            model.addConstr(NCH[i] <= (1 / self.h) * (NHS[i] + NO[i] * self.H))

        model.addConstr(NO[0] == self.Ouv)
        for i in range(3):
            model.addConstr(NO[i+1] == NO[i] + NOR[i] - NOL[i])



        model.addConstr(S[0] == int(self.StockInit))
        model.addConstr(S[1] == S[0] + NCH[0] - int(self.D[0]))
        model.addConstr(S[2] == S[1] + NCH[1] - int(self.D[1]))
        model.addConstr(S[3] == S[2] + NCH[2] - int(self.D[2]))
        model.addConstr(S[4] == S[3] + NCH[3] - int(self.D[3]))


        for i in range(4):
          model.addConstr(S[i] >= 0)
          model.addConstr(NO[i] >= 0)
          model.addConstr(NOR[i] >= 0)
          model.addConstr(NOL[i] >= 0)
          model.addConstr(NHS[i] >= 0)

        model.optimize()


        result = {}
        for i in range(4):
            result["Month " + str(i + 1)] = {
                "NHS": NHS[i].X,
                "NCH": NCH[i].X,
                "NOR": NOR[i].X,
                "NOL": NOL[i].X,
                "S": S[i].X,
                "NO": NO[i].X
            }
        return result

def run_optimization():
    try:

        C = float(c_entry.get())
        Cs = float(cs_entry.get())
        D = [float(d_entry.get()) for d_entry in d_entries]
        Ouv = int(ouv_entry.get())
        Sal = float(sal_entry.get())
        Hsup = float(hsup_entry.get())
        R = float(r_entry.get())
        L = float(l_entry.get())
        h = float(h_entry.get())
        H = float(H_entry.get())
        Hmax = float(hmax_entry.get())
        StockInit = float(stock_init_entry.get())

        model = shoes(C, Cs, D, Ouv, Sal, Hsup, R, L, h, H, Hmax, StockInit)
        results = model.run()


        result_text.delete(1.0, tk.END)  # Clear the text area before displaying new results
        for month, data in results.items():
            result_text.insert(tk.END, f"Results for Month {month}:\n")
            for key, value in data.items():
                result_text.insert(tk.END, f"{key}: {value}\n")
            result_text.insert(tk.END, "\n")  # Add a newline after each month's results
    except ValueError as e:
        messagebox.showerror("Input Error", "Please check the input values.")
    except Exception as e:
        messagebox.showerror("Error", str(e))



root = tk.Tk()
root.title("Production Optimization")


input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10)


tk.Label(input_frame, text="C (Raw Material Cost):").grid(row=0, column=0)
c_entry = tk.Entry(input_frame)
c_entry.grid(row=0, column=1)

tk.Label(input_frame, text="Cs (Storage Cost):").grid(row=1, column=0)
cs_entry = tk.Entry(input_frame)
cs_entry.grid(row=1, column=1)


d_labels = ["D1 (Month 1 Demand):", "D2 (Month 2 Demand):", "D3 (Month 3 Demand):", "D4 (Month 4 Demand):"]
d_entries = []
for i, label in enumerate(d_labels):
    tk.Label(input_frame, text=label).grid(row=i + 2, column=0)
    d_entry = tk.Entry(input_frame)
    d_entry.grid(row=i + 2, column=1)
    d_entries.append(d_entry)

tk.Label(input_frame, text="Ouv (Initial Workers):").grid(row=6, column=0)
ouv_entry = tk.Entry(input_frame)
ouv_entry.grid(row=6, column=1)

tk.Label(input_frame, text="Sal (Worker Salary):").grid(row=7, column=0)
sal_entry = tk.Entry(input_frame)
sal_entry.grid(row=7, column=1)

tk.Label(input_frame, text="Hsup (Overtime Cost):").grid(row=8, column=0)
hsup_entry = tk.Entry(input_frame)
hsup_entry.grid(row=8, column=1)

tk.Label(input_frame, text="R (Recruitment Cost):").grid(row=9, column=0)
r_entry = tk.Entry(input_frame)
r_entry.grid(row=9, column=1)

tk.Label(input_frame, text="L (Layoff Cost):").grid(row=10, column=0)
l_entry = tk.Entry(input_frame)
l_entry.grid(row=10, column=1)

tk.Label(input_frame, text="h (Hours per Pair):").grid(row=11, column=0)
h_entry = tk.Entry(input_frame)
h_entry.grid(row=11, column=1)

tk.Label(input_frame, text="H (Working Hours):").grid(row=12, column=0)
H_entry = tk.Entry(input_frame)
H_entry.grid(row=12, column=1)

tk.Label(input_frame, text="Hmax (Max Overtime Hours):").grid(row=13, column=0)
hmax_entry = tk.Entry(input_frame)
hmax_entry.grid(row=13, column=1)

tk.Label(input_frame, text="StockInit (Initial Stock):").grid(row=14, column=0)
stock_init_entry = tk.Entry(input_frame)
stock_init_entry.grid(row=14, column=1)


run_button = tk.Button(root, text="Run Optimization", command=run_optimization)
run_button.pack(pady=5)


result_text = tk.Text(root, height=15, width=50)
result_text.pack(pady=5)

c_entry.insert(0, "15")
cs_entry.insert(0, "3")

ouv_entry.insert(0, "100")
sal_entry.insert(0, "1500")
hsup_entry.insert(0, "13")
r_entry.insert(0, "1600")
l_entry.insert(0, "2000")
h_entry.insert(0, "4")
H_entry.insert(0, "160")
hmax_entry.insert(0, "20")
stock_init_entry.insert(0, "500")

root.mainloop()