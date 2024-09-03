import tkinter as tk
from tkinter import ttk
from handlers import show_offer_history, show_frame

def create_history_frame(main_frame, frames):
    history_frame = ttk.Frame(main_frame, padding="10")
    history_frame.grid(row=0, column=0, sticky="nsew")

    back_button = ttk.Button(history_frame, text="Terug", command=lambda: show_frame(frames["home"]))
    back_button.grid(row=1, column=1, pady=10, padx=10, sticky='se')

    show_offer_history(history_frame, show_frame, frames)

    return history_frame
