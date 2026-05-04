#pip install customtkinter matplotlibS

import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# =========================
# DATABASE
# =========================
conn = sqlite3.connect("employees.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    score INTEGER,
    traits TEXT
)
""")

# Ensure traits column exists
cursor.execute("PRAGMA table_info(performance)")
cols = [c[1] for c in cursor.fetchall()]
if "traits" not in cols:
    cursor.execute("ALTER TABLE performance ADD COLUMN traits TEXT")

conn.commit()

# =========================
# TRAITS
# =========================
TRAIT_SCORES = {
    "meets deadlines": 3, "misses deadlines": -5,
    "high productivity": 4, "low productivity": -4,
    "high quality work": 4, "low quality work": -4,
    "team player": 3, "poor collaboration": -3,
    "good communication": 3, "poor communication": -3,
    "initiative": 4, "mentors others": 4, "decision making": 3,
    "consistent": 3, "inconsistent": -3,
    "focused": 3, "lack of focus": -3,
    "problem solving": 4, "slow problem solving": -3
}

CATEGORY_MAP = {
    "Productivity": ["meets deadlines","misses deadlines","high productivity","low productivity"],
    "Quality": ["high quality work","low quality work"],
    "Teamwork": ["team player","poor collaboration"],
    "Communication": ["good communication","poor communication"],
    "Leadership": ["initiative","mentors others","decision making"],
    "Consistency": ["consistent","inconsistent"],
    "Focus": ["focused","lack of focus"],
    "Problem Solving": ["problem solving","slow problem solving"]
}

MAX_SCORE = sum(v for v in TRAIT_SCORES.values() if v > 0)

# =========================
# HELPERS
# =========================
def get_text_color(bg):
    bg = bg.lstrip('#')
    r,g,b = int(bg[0:2],16), int(bg[2:4],16), int(bg[4:6],16)
    brightness = (r*299 + g*587 + b*114)/1000
    return "black" if brightness > 150 else "white"

def calculate_category_scores(traits):
    scores = {}
    for cat, ts in CATEGORY_MAP.items():
        total, max_s = 0, 0
        for t in ts:
            if t in TRAIT_SCORES:
                w = TRAIT_SCORES[t]
                if w > 0: max_s += w
                if t in traits: total += w
        scores[cat] = max(int((total/max_s)*100),0) if max_s else 0
    return scores

# =========================
# APP
# =========================
class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("HR Dashboard")
        self.geometry("1100x750")

        self.selected_traits = set()
        self.loading_running = False

        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.pack(fill="both", expand=True)

        ctk.CTkLabel(self.scroll, text="Employee Performance Dashboard",
                     font=("Segoe UI",22,"bold")).pack(pady=10)

        # KPI
        self.kpi_frame = ctk.CTkFrame(self.scroll)
        self.kpi_frame.pack(pady=10)

        self.kpi_current = ctk.CTkLabel(self.kpi_frame, text="Current\n--%", width=150)
        self.kpi_current.grid(row=0,column=0,padx=10)

        self.kpi_prev = ctk.CTkLabel(self.kpi_frame, text="Previous\n--%", width=150)
        self.kpi_prev.grid(row=0,column=1,padx=10)

        self.kpi_change = ctk.CTkLabel(self.kpi_frame, text="Change\n--%", width=150)
        self.kpi_change.grid(row=0,column=2,padx=10)

        # Employee
        self.emp_var = ctk.StringVar()
        self.dropdown = ctk.CTkComboBox(self.scroll, variable=self.emp_var)
        self.dropdown.pack(pady=5)

        self.new_entry = ctk.CTkEntry(self.scroll, placeholder_text="New Employee")
        self.new_entry.pack(pady=5)

        ctk.CTkButton(self.scroll, text="Add Employee",
                      command=self.add_employee).pack(pady=5)

        # Traits
        self.trait_frame = ctk.CTkScrollableFrame(self.scroll, height=250)
        self.trait_frame.pack(fill="x", pady=10)

        self.buttons = {}
        for i,t in enumerate(TRAIT_SCORES):
            b = ctk.CTkButton(self.trait_frame, text=t, fg_color="#3a3a3a",
                              command=lambda x=t: self.toggle_trait(x))
            b.grid(row=i//2,column=i%2,padx=10,pady=5)
            self.buttons[t] = b

        # Buttons
        btn_frame = ctk.CTkFrame(self.scroll)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame,text="Evaluate",command=self.evaluate).grid(row=0,column=0,padx=10)
        ctk.CTkButton(btn_frame,text="Reset",command=self.reset).grid(row=0,column=1,padx=10)

        self.output = ctk.CTkLabel(self.scroll,text="")
        self.output.pack(pady=10)

        self.loading_label = ctk.CTkLabel(self.scroll, text="")
        self.loading_label.pack()

        # Graphs
        self.graph_frame = ctk.CTkFrame(self.scroll)
        self.graph_frame.pack(fill="both",expand=True,pady=10)

        self.line_frame = ctk.CTkFrame(self.graph_frame)
        self.line_frame.pack(side="left",fill="both",expand=True,padx=10)

        self.radar_frame = ctk.CTkFrame(self.graph_frame)
        self.radar_frame.pack(side="right",fill="both",expand=True,padx=10)

        self.load_employees()

    def load_employees(self):
        cursor.execute("SELECT DISTINCT name FROM performance")
        self.dropdown.configure(values=[r[0] for r in cursor.fetchall()])

    def add_employee(self):
        name = self.new_entry.get().strip()
        if not name: return
        vals = list(self.dropdown.cget("values"))
        if name not in vals:
            vals.append(name)
            self.dropdown.configure(values=vals)
        self.emp_var.set(name)
        self.new_entry.delete(0,"end")

    def toggle_trait(self,t):
        if t in self.selected_traits:
            self.selected_traits.remove(t)
            self.buttons[t].configure(fg_color="#3a3a3a")
        else:
            self.selected_traits.add(t)
            self.buttons[t].configure(fg_color="#00cc66")

    def reset(self):
        self.selected_traits.clear()
        for b in self.buttons.values():
            b.configure(fg_color="#3a3a3a")

        self.kpi_current.configure(text="Current\n--%", fg_color="#3a3a3a", text_color="white")
        self.kpi_prev.configure(text="Previous\n--%", fg_color="#3a3a3a", text_color="white")
        self.kpi_change.configure(text="Change\n--%", fg_color="#3a3a3a", text_color="white")

        self.output.configure(text="")

        for w in self.line_frame.winfo_children(): w.destroy()
        for w in self.radar_frame.winfo_children(): w.destroy()

        self.emp_var.set("")

    # =========================
    # LOADING
    def show_loading(self):
        self.loading_running = True
        self.dots = 0
        def animate():
            if not self.loading_running: return
            self.loading_label.configure(text="Processing" + "."*(self.dots%4))
            self.dots += 1
            self.after(400, animate)
        animate()

    def stop_loading(self):
        self.loading_running = False
        self.loading_label.configure(text="")

    # =========================
    def evaluate(self):
        name = self.emp_var.get()
        if not name:
            messagebox.showerror("Error","Select employee")
            return
        if not self.selected_traits:
            messagebox.showerror("Error","Select traits")
            return

        self.show_loading()
        self.after(1000, lambda: self._run_eval(name))

    def _run_eval(self,name):
        score = sum(TRAIT_SCORES[t] for t in self.selected_traits)
        percent = max(int((score/MAX_SCORE)*100),0)

        traits_str = ",".join(self.selected_traits)

        cursor.execute("INSERT INTO performance (name,score,traits) VALUES (?,?,?)",
                       (name,percent,traits_str))
        conn.commit()

        cursor.execute("SELECT score,traits FROM performance WHERE name=? ORDER BY id",(name,))
        rows = cursor.fetchall()

        history = [r[0] for r in rows]
        prev = history[-2] if len(history)>1 else None

        change = percent - prev if prev else 0

        color = "#2ecc71" if change>0 else "#e74c3c" if change<0 else "#f1c40f"
        txt = get_text_color(color)

        self.kpi_current.configure(text=f"Current\n{percent}%", fg_color=color, text_color=txt)
        self.kpi_prev.configure(text=f"Previous\n{prev if prev else '--'}%", fg_color="#3a3a3a", text_color="white")
        self.kpi_change.configure(text=f"Change\n{change:+}%", fg_color=color, text_color=txt)

        self.output.configure(text=f"{name} Score: {percent}%")

        self.draw_line(history)
        self.draw_radar(self.selected_traits)

        self.stop_loading()

    def draw_line(self,history):
        for w in self.line_frame.winfo_children(): w.destroy()
        fig,ax = plt.subplots(figsize=(5,3))
        x=list(range(1,len(history)+1))
        ax.plot(x,history,marker='o')
        ax.set_ylim(0,100)
        ax.set_title("Trend")
        ax.grid(True)
        canvas=FigureCanvasTkAgg(fig,master=self.line_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both",expand=True)

    def draw_radar(self,traits):
        for w in self.radar_frame.winfo_children(): w.destroy()
        fig,ax = plt.subplots(subplot_kw=dict(polar=True), figsize=(5,5))

        scores = calculate_category_scores(traits)
        labels=list(scores.keys())
        vals=list(scores.values())+[list(scores.values())[0]]

        angles=np.linspace(0,2*np.pi,len(labels),endpoint=False).tolist()
        angles+=angles[:1]

        ax.plot(angles,vals)
        ax.fill(angles,vals,alpha=0.25)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels,fontsize=8)

        canvas=FigureCanvasTkAgg(fig,master=self.radar_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both",expand=True)

app=Dashboard()
app.mainloop()