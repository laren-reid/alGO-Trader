import tkinter as tk
import tkinter.ttk as ttk

window=tk.Tk()
window.title("Algorithmic Trader Dashboard")
window.geometry("800x500")
window.configure(padx=15, pady=15)

big_button = tk.Frame(window)
big_button.pack(fill="x", pady=(0,15))

chframe = tk.LabelFrame(big_button, text="", bd=2, relief="solid", width=350, height=200)
chframe.pack_propagate(False)  # Maintain explicit size
chframe.pack(side="left", padx=(0, 20))

chlabel = tk.Label(chframe, text="- NULL -", font=("Maven Pro", 12, "bold"))
chlabel.pack(expand=True)

conf_bar_frame = tk.Frame(big_button)
conf_bar_frame.pack(side="left", fill="both", expand=True)

conf_bar_label = tk.Label(conf_bar_frame, text="Confidence : NULL", font=("Maven Pro", 12, "bold"))
conf_bar_label.pack(fill="x", pady=(0,15))

window.mainloop()