import tkinter as tk
from tkinter import ttk

def create_settings_frame(parent, frames):
    settings_frame = ttk.Frame(parent, padding="10")
    settings_frame.grid(row=0, column=0, sticky="nsew")

    ttk.Label(settings_frame, text="Instellingen", font=("Arial", 14, "bold")).grid(pady=20)
    ttk.Label(settings_frame, text="Voorbeeldinstelling:").grid(sticky=tk.W, pady=5)
    ttk.Entry(settings_frame).grid(sticky=tk.W, pady=5)

    back_button = ttk.Button(settings_frame, text="Terug", command=lambda: frames["home"].tkraise())
    back_button.grid(row=1, column=0, pady=10, sticky="w")

    return settings_frame
