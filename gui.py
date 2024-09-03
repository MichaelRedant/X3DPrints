import tkinter as tk
from tkinter import ttk
from home_frame import create_home_frame
from quote_frame import create_quote_frame
from history_frame import create_history_frame
from gui_helpers import create_menubar
from settings_frame import create_settings_frame
from info_frame import create_info_frame

def create_main_window():
    app = tk.Tk()
    app.title("3D Print Offerte Generator")
    app.geometry("800x600")

    main_frame = ttk.Frame(app, padding="10")
    main_frame.grid(row=0, column=0, sticky="nsew")

    app.columnconfigure(0, weight=1)
    app.rowconfigure(0, weight=1)

    # Maak de frames dictionary eerst leeg aan
    frames = {}

    # Voeg de frames toe aan de frames dictionary
    frames["home"] = create_home_frame(main_frame, frames, lambda: open_settings_window(frames))
    frames["quote"] = create_quote_frame(main_frame, frames)
    frames["history"] = create_history_frame(main_frame, frames)
    frames["settings"] = create_settings_frame(main_frame, frames)
    frames["info"] = create_info_frame(main_frame, frames)  # Nieuw toegevoegd

    # Maak de menubalk aan
    menubar = create_menubar(app, frames)
    app.config(menu=menubar)

    # Toon het home frame bij het opstarten
    frames["home"].tkraise()

    app.mainloop()

def open_settings_window(frames):
    frames["settings"].tkraise()

if __name__ == "__main__":
    create_main_window()
