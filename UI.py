import os
import sys
import threading
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "models"))

from data_fetcher import get_historical_data
from features import add_features
from config import MODEL_PATH
import predict as predict_module

window = tk.Tk()
window.title("Algorithmic Trader Dashboard")
window.geometry("800x600")
window.configure(padx=15, pady=15)

big_button = tk.Frame(window)
big_button.pack(fill=tk.X, pady=(0, 30))

tabs = ttk.Notebook(window)
tabs.pack(fill="both", expand=True, side="bottom", pady=(0, 15))

chframe = tk.LabelFrame(big_button, text="", bd=2, relief="solid", width=350, height=200)
chframe.pack_propagate(False)
chframe.pack(side="left", padx=(0, 20))

chlabel = tk.Label(chframe, text="- NULL -", font=("Maven Pro", 12, "bold"))
chlabel.pack(expand=True)

conf_bar_frame = tk.Frame(big_button)
conf_bar_frame.pack(side="left", expand=True)

conf_bar_label = tk.Label(conf_bar_frame, text="Confidence Level : NULL", font=("Maven Pro", 12, "bold"))
conf_bar_label.pack(fill=tk.X, pady=(0, 0))

conf_bar = tk.LabelFrame(conf_bar_frame, text="", bd=2, relief="solid", width=600, height=50)
conf_bar.pack(side="left", padx=(0, 0))

# Inner bar that grows/shrinks to visualize confidence percentage
conf_bar_fill = tk.Frame(conf_bar, bg="#4a90d9", width=0, height=46)
conf_bar_fill.place(x=2, y=2)

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

status_var = tk.StringVar(value="")
status_lbl = tk.Label(t1frame, textvariable=status_var, font=("Maven Pro", 10), fg="#666666")
status_lbl.pack(side="left", padx=(0, 10))

rsi_var = tk.StringVar(value="0.00")
macd_var = tk.StringVar(value="0.00")
ema_var = tk.StringVar(value="0.00")


def set_status(text, color="#666666"):
    status_var.set(text)
    status_lbl.configure(fg=color)


def set_signal_ui(signal: str, confidence: float):
    colors = {"BUY": "#2e7d32", "SELL": "#c62828", "HOLD": "#f9a825"}
    chlabel.configure(text=signal, fg=colors.get(signal, "black"))
    conf_bar_label.configure(text=f"Confidence Level : {confidence * 100:.1f}%")
    # conf_bar interior is ~596px wide (600 - 2*2 border)
    fill_width = int(596 * confidence)
    conf_bar_fill.place(x=2, y=2, width=fill_width, height=46)


def set_indicators_ui(row):
    rsi_var.set(f"{row['rsi']:.2f}")
    macd_var.set(f"{row['macd']:.4f}")
    ema_var.set(f"{row['ema_10']:.2f}")


def run_prediction(ticker: str):
    """Runs on a background thread: network fetch + feature calc + model
    inference. Only touches Tkinter widgets via window.after(), since
    Tkinter is not thread-safe and updating widgets directly from a
    background thread can crash or corrupt the UI."""
    try:
        df = get_historical_data(ticker, "2022-01-01", "2026-07-11")

        if df.empty:
            window.after(0, lambda: (
                set_status(f"No data found for {ticker}.", "#c62828"),
                messagebox.showerror("Data error", f"No data found for ticker '{ticker}'.")
            ))
            return

        if not os.path.exists(MODEL_PATH):
            window.after(0, lambda: (
                set_status("No trained model found.", "#c62828"),
                messagebox.showerror(
                    "Model error",
                    f"No trained model at {MODEL_PATH}.\nRun models/train.py first."
                )
            ))
            return

        result = predict_module.predict(df)
        features_df = add_features(df)
        last_row = features_df.iloc[-1]

        def update_ui():
            set_signal_ui(result["signal"], result["confidence"])
            set_indicators_ui(last_row)
            set_status(f"Updated: {ticker}", "#2e7d32")

        window.after(0, update_ui)

    except Exception as e:
        window.after(0, lambda: (
            set_status("Error.", "#c62828"),
            messagebox.showerror("Error", str(e))
        ))


def handle_submit():
    user_text = tickerinp.get().strip().upper()

    if not user_text:
        messagebox.showwarning("Missing ticker", "Please enter a stock ticker.")
        return

    print(f"User submitted ticker: {user_text}")
    set_status(f"Fetching {user_text}...", "#666666")
    submit_btn.configure(state="disabled")

    def worker():
        try:
            run_prediction(user_text)
        finally:
            window.after(0, lambda: submit_btn.configure(state="normal"))

    threading.Thread(target=worker, daemon=True).start()


submit_btn = tk.Button(t1frame, text="Submit", font=("Maven Pro", 11), command=handle_submit)
submit_btn.pack(side="left")

# Let Enter key in the ticker field trigger submit too
tickerinp.bind("<Return>", lambda event: handle_submit())

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

if __name__ == "__main__":
    window.mainloop()
