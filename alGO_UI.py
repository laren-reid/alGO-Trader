import tkinter as tk
import tkinter.ttk as ttk

window=tk.Tk()
window.title("Algorithmic Trader Dashboard")
window.geometry("800x600")
window.configure(padx=15, pady=15)

big_button = tk.Frame(window)
big_button.pack(fill=tk.X, pady=(0,30))

tabs = ttk.Notebook(window)
tabs.pack(fill="both", expand=True, side="bottom", pady=(0,15))

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

tab1 = ttk.Frame(tabs)
tab1.pack(fill=tk.X, pady=(0, 15))

tab2 = ttk.Frame(tabs)
tab2.pack(fill=tk.X, pady=(0, 15))

tabs.add(tab1, text="ENTER")
tabs.add(tab2, text="INDICATORS")

t1frame = tk.LabelFrame(tab1, text="TICKER SUBMISSION PANEL", bd=2, relief="solid", width=1450, height=200)
t1frame.pack_propagate(False)
t1frame.pack(side="left", padx=(0, 20))

tickerlbl = tk.Label(t1frame, text="Enter Stock Ticker:", font=("Maven Pro", 11))
tickerlbl.pack(side="left", padx=(0, 10))

tickerinp = tk.Entry(t1frame, font=("Maven Pro", 11), width=15)
tickerinp.pack(side="left", padx=(0, 15))

def handle_submit():
    user_text = tickerinp.get() 
    print(f"User submitted ticker: {user_text.upper()}")
    
    tickerinp.delete(0, tk.END)

rsi_var = tk.StringVar(value="0.00")
macd_var = tk.StringVar(value="0.00")
ema_var = tk.StringVar(value="0.00")

row_rsi = tk.Frame(tab2)
row_rsi.pack(fill=tk.X, pady=4, padx=10)

title_rsilbl = tk.Label(row_rsi, text="RSI:", font=("Arial", 10, "bold"), width=8, anchor="w")
title_rsilbl.pack(side=tk.LEFT)

value_rsilbl = tk.Label(row_rsi, textvariable=rsi_var, font=("Arial", 10))
value_rsilbl.pack(side=tk.LEFT, padx=5)

row_macd = tk.Frame(tab2)
row_macd.pack(fill=tk.X, pady=4, padx=10)

title_macdlbl = tk.Label(row_macd, text="MACD:", font=("Arial", 10, "bold"), width=8, anchor="w")
title_macdlbl.pack(side=tk.LEFT)

value_macdlbl = tk.Label(row_macd, textvariable=macd_var, font=("Arial", 10))
value_macdlbl.pack(side=tk.LEFT, padx=5)

row_ema = tk.Frame(tab2)
row_ema.pack(fill=tk.X, pady=4, padx=10)

title_emalbl = tk.Label(row_ema, text="EMA:", font=("Arial", 10, "bold"), width=8, anchor="w")
title_emalbl.pack(side=tk.LEFT)

value_emalbl = tk.Label(row_ema, textvariable=ema_var, font=("Arial", 10))
value_emalbl.pack(side=tk.LEFT, padx=5)

window.mainloop()