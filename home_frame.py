import tkinter as tk
from tkinter import ttk
from handlers import show_frame

def create_home_frame(parent, frames, open_settings_window):
    home_frame = ttk.Frame(parent, padding="10")
    home_frame.grid(row=0, column=0, sticky="nsew")

    ttk.Label(home_frame, text="Welkom bij de 3D Print Offerte Generator", font=("Arial", 14, "bold")).grid(pady=20)
    ttk.Button(home_frame, text="Nieuwe Offerte", command=lambda: frames["quote"].tkraise()).grid(pady=10)
    ttk.Button(home_frame, text="Bekijk Offertes", command=lambda: frames["history"].tkraise()).grid(pady=10)
    ttk.Button(home_frame, text="Instellingen", command=open_settings_window).grid(pady=10)

    return home_frame
