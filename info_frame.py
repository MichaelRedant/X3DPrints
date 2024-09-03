import tkinter as tk
from tkinter import ttk

def create_info_frame(parent, frames):
    info_frame = ttk.Frame(parent, padding="10")
    info_frame.grid(row=0, column=0, sticky="nsew")

    info_label = ttk.Label(info_frame, text="Deze applicatie is ontwikkeld door Michaël Redant voor X3DPrints.")
    info_label.grid(row=0, column=0, pady=20)

    back_button = ttk.Button(info_frame, text="Terug", command=lambda: frames["home"].tkraise())
    back_button.grid(row=1, column=0, pady=10, sticky="w")

    return info_frame
