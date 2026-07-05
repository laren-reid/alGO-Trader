import tkinter as tk

root=tk.Tk()
root.title("Test Python GUI")
root.geometry("600x400")

def on_button_click():
    label.config(text="Success")
    
label = tk.Label(root, text="Welcome! Click the button below.", font=("Arial", 14))
button = tk.Button(root, text="I like to eat food and swim", command=on_button_click, bg="blue", fg="white")

label.pack(pady=20)
button.pack(pady=10)

root.mainloop()