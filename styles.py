import tkinter as tk
from tkinter import ttk

def apply_styles(root):
    style = ttk.Style(root)
    style.theme_use('clam')

    # Algemene stijl voor labels
    style.configure("TLabel", font=("Open Sans", 12), background="#ffffff")

    # Stijl voor knoppen
    style.configure("TButton", font=("Open Sans", 12, "bold"), background="black", foreground="white", padding=10)
    style.map("TButton", background=[("active", "grey")], relief=[("pressed", "sunken")])
    style.configure("TButton", relief="flat", borderwidth=1, focusthickness=3, focuscolor="none")
    
    # Stijl voor invoervelden
    style.configure("TEntry", font=("Open Sans", 12), padding=5)
    
    # Stijl voor combobox
    style.configure("TCombobox", font=("Open Sans", 12), padding=5)

    # Achtergrondkleur voor het hele frame en venster
    root.configure(background='#ffffff')
    style.configure("TFrame", background="#ffffff")
