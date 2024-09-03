import tkinter as tk

def create_menubar(app, frames):
    """Creëer de menubalk voor de applicatie."""
    menubar = tk.Menu(app)

    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Instellingen", command=frames["settings"].tkraise)
    file_menu.add_command(label="Bekijk Offertes", command=frames["history"].tkraise)
    file_menu.add_separator()
    file_menu.add_command(label="Afsluiten", command=app.quit)
    menubar.add_cascade(label="Bestand", menu=file_menu)

    info_menu = tk.Menu(menubar, tearoff=0)
    info_menu.add_command(label="Over", command=frames["info"].tkraise)
    menubar.add_cascade(label="Info", menu=info_menu)

    return menubar

def show_frame(frame):
    """Toon een specifiek frame en verberg de rest."""
    for widget in frame.master.winfo_children():
        widget.grid_remove()  # Verberg alle frames
    frame.grid(row=0, column=0, sticky="nsew")  # Toon het geselecteerde frame

def validate_numeric_input(action, value_if_allowed):
    """Valideer numerieke invoer, staat alleen numerieke waarden toe."""
    if action != '1':  # Actie '1' betekent dat de invoer wordt toegevoegd
        return True
    try:
        float(value_if_allowed.replace(',', '.'))  # Ondersteunt zowel ',' als '.' als decimaal
        return True
    except ValueError:
        return False

def apply_styles(app):
    """Pas de centrale stijlen toe op de tkinter-app."""
    style = tk.ttk.Style()
    style.configure("TFrame", background="#f0f0f0")
    style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
    style.configure("TButton", background="#e0e0e0", font=("Arial", 10))
    app.option_add('*Font', 'Arial 10')
