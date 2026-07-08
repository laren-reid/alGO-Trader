import tkinter as tk
import tkinter.ttk as ttk

window=tk.Tk()
window.title("Algorithmic Trader Dashboard")
window.geometry("800x600")
window.configure(padx=15, pady=15)

big_button = tk.Frame(window)
big_button.pack(fill=tk.X, pady=(0,30))

chframe = tk.LabelFrame(big_button, text="", bd=2, relief="solid", width=350, height=200)
chframe.pack_propagate(False)
chframe.pack(side="left", padx=(0, 20))

chlabel = tk.Label(chframe, text="- NULL -", font=("Maven Pro", 12, "bold"))
chlabel.pack(expand=True)

conf_bar_frame = tk.Frame(big_button)
conf_bar_frame.pack(side="left", expand=True)

conf_bar_label = tk.Label(conf_bar_frame, text="Confidence Level : NULL", font=("Maven Pro", 12, "bold"))
conf_bar_label.pack(fill=tk.X, pady=(0,0))

conf_bar = tk.LabelFrame(conf_bar_frame, text="", bd=2, relief="solid", width=600, height=50)
conf_bar.pack(side="left", padx=(0, 0))

tab1 = tk.Frame(window)
tab1.pack(fill=tk.X, pady=(0, 15))

t1frame = tk.LabelFrame(tab1, text="", bd=2, relief="solid", width=1450, height=200)
t1frame.pack_propagate(False)
t1frame.pack(side="left", padx=(0, 20))

window.mainloop()