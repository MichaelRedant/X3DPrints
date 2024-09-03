import tkinter as tk
from tkinter import ttk, messagebox
from settings import open_settings_window, settings
from handlers import generate_quote, save_as_pdf, show_info, show_offer_history, save_quote_in_app
from styles import apply_styles
from utils import display_generated_quote

def validate_numeric_input(action, value_if_allowed):
    if action != '1':  # Actie '1' betekent dat de invoer wordt toegevoegd
        return True
    try:
        float(value_if_allowed.replace(',', '.'))  # Ondersteunt zowel ',' als '.' als decimaal
        return True
    except ValueError:
        return False

def update_design_time_visibility(combo_design_choice, design_frame):
    if combo_design_choice.get() == "Eigen ontwerp":
        design_frame.grid()
    else:
        design_frame.grid_remove()

def update_delivery_related_fields(combo_delivery_type, travel_distance_label, entry_travel_distance, urgent_checkbox):
    if combo_delivery_type.get() in ["Zelf leveren", "Zelf leveren in spoed"]:
        travel_distance_label.grid()
        entry_travel_distance.grid()
        urgent_checkbox.grid()
    else:
        travel_distance_label.grid_remove()
        entry_travel_distance.grid_remove()
        urgent_checkbox.grid_remove()

def validate_fields(*fields):
    for field in fields:
        if not field.get():
            return False
    return True

def create_main_window():
    app = tk.Tk()
    app.title("3D Print Offerte Generator")

    # Pas de centrale stijlen toe
    apply_styles(app)

    # Menubalk toevoegen
    menubar = tk.Menu(app)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Instellingen", command=open_settings_window)
    file_menu.add_command(label="Bekijk Offertes", command=show_offer_history)
    file_menu.add_separator()
    file_menu.add_command(label="Afsluiten", command=app.quit)
    menubar.add_cascade(label="Bestand", menu=file_menu)

    info_menu = tk.Menu(menubar, tearoff=0)
    info_menu.add_command(label="Over", command=show_info)
    menubar.add_cascade(label="Info", menu=info_menu)

    app.config(menu=menubar)

    frame = ttk.Frame(app, padding="20")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Validatieconfiguratie
    vcmd = (app.register(validate_numeric_input), '%d', '%P')

    # Klantnaam
    ttk.Label(frame, text="Klant:").grid(column=0, row=0, sticky=tk.W, pady=10)
    entry_customer_name = ttk.Entry(frame)
    entry_customer_name.grid(column=1, row=0, sticky=tk.EW, pady=10)

    # Filament type
    ttk.Label(frame, text="Filament type:").grid(column=0, row=1, sticky=tk.W, pady=10)
    combo_filament_type = ttk.Combobox(frame, values=list(settings["pla_prices"].keys()), state="readonly")
    combo_filament_type.grid(column=1, row=1, sticky=tk.EW, pady=10)

    # Ontwerp keuze
    ttk.Label(frame, text="Ontwerpkeuze:").grid(column=0, row=2, sticky=tk.W, pady=10)
    combo_design_choice = ttk.Combobox(frame, values=["Klantontwerp", "Eigen ontwerp"], state="readonly")
    combo_design_choice.grid(column=1, row=2, sticky=tk.EW, pady=10)
    combo_design_choice.bind("<<ComboboxSelected>>", lambda e: update_design_time_visibility(combo_design_choice, design_frame))

    # Printtijd
    ttk.Label(frame, text="Printtijd:").grid(column=0, row=3, sticky=tk.W, pady=10)
    entry_print_hours = ttk.Entry(frame, width=5, validate="key", validatecommand=vcmd)
    entry_print_hours.grid(column=1, row=3, sticky=tk.W)
    ttk.Label(frame, text="uur").grid(column=1, row=3, padx=(60, 0), sticky=tk.W)

    entry_print_minutes = ttk.Entry(frame, width=5, validate="key", validatecommand=vcmd)
    entry_print_minutes.grid(column=1, row=3, padx=(120, 0), sticky=tk.W)
    ttk.Label(frame, text="min").grid(column=1, row=3, padx=(180, 0), sticky=tk.W)

    entry_print_seconds = ttk.Entry(frame, width=5, validate="key", validatecommand=vcmd)
    entry_print_seconds.grid(column=1, row=3, padx=(240, 0), sticky=tk.W)
    ttk.Label(frame, text="sec").grid(column=1, row=3, padx=(300, 0), sticky=tk.W)

    # Gewicht van 3D print
    ttk.Label(frame, text="Gewicht van 3D print (gram):").grid(column=0, row=4, sticky=tk.W, pady=10)
    entry_filament_weight = ttk.Entry(frame, validate="key", validatecommand=vcmd)
    entry_filament_weight.grid(column=1, row=4, sticky=tk.EW, pady=10)

    # Aantal prints
    ttk.Label(frame, text="Aantal prints:").grid(column=0, row=5, sticky=tk.W, pady=10)
    entry_number_of_prints = ttk.Entry(frame, validate="key", validatecommand=vcmd)
    entry_number_of_prints.grid(column=1, row=5, sticky=tk.EW, pady=10)

    # Leveringstype
    ttk.Label(frame, text="Leveringstype:").grid(column=0, row=6, sticky=tk.W, pady=10)
    combo_delivery_type = ttk.Combobox(frame, values=["Geen", "Per post", "Zelf leveren", "Zelf leveren in spoed"], state="readonly")
    combo_delivery_type.grid(column=1, row=6, sticky=tk.EW, pady=10)
    combo_delivery_type.bind("<<ComboboxSelected>>", lambda e: update_delivery_related_fields(combo_delivery_type, travel_distance_label, entry_travel_distance, urgent_checkbox))

    # Ontwerptijd (zichtbaar als Eigen ontwerp is geselecteerd)
    design_frame = ttk.Frame(frame)
    ttk.Label(design_frame, text="Ontwerptijd:").grid(column=0, row=0, sticky=tk.W, pady=10)
    entry_design_hours = ttk.Entry(design_frame, width=5, validate="key", validatecommand=vcmd)
    entry_design_hours.grid(column=1, row=0, sticky=tk.W)
    ttk.Label(design_frame, text="uur").grid(column=1, row=0, padx=(60, 0), sticky=tk.W)

    entry_design_minutes = ttk.Entry(design_frame, width=5, validate="key", validatecommand=vcmd)
    entry_design_minutes.grid(column=1, row=0, padx=(120, 0), sticky=tk.W)
    ttk.Label(design_frame, text="min").grid(column=1, row=0, padx=(180, 0), sticky=tk.W)
    design_frame.grid(column=0, row=7, columnspan=2, sticky=tk.EW, pady=10)
    design_frame.grid_remove()

    # Reisafstand (zichtbaar als Zelf leveren of Zelf leveren in spoed is geselecteerd)
    travel_distance_label = ttk.Label(frame, text="Reisafstand (km):")
    travel_distance_label.grid(column=0, row=8, sticky=tk.W, pady=10)
    entry_travel_distance = ttk.Entry(frame, validate="key", validatecommand=vcmd)
    entry_travel_distance.grid(column=1, row=8, sticky=tk.EW, pady=10)
    urgent_checkbox = ttk.Checkbutton(frame, text="Spoedlevering")
    urgent_checkbox.grid(column=1, row=9, sticky=tk.W, pady=10)
    travel_distance_label.grid_remove()
    entry_travel_distance.grid_remove()
    urgent_checkbox.grid_remove()

    # Resultaat frame
    result_frame = ttk.Frame(frame)
    result_frame.grid(column=0, row=11, columnspan=2, sticky=tk.EW, pady=10)

    # Knoppen toevoegen
    button_frame = ttk.Frame(frame)
    button_frame.grid(column=0, row=10, columnspan=2, pady=20)

    ttk.Button(button_frame, text="Genereer Offerte", command=lambda: generate_quote(entry_print_hours, entry_print_minutes, entry_print_seconds, combo_filament_type, entry_filament_weight, entry_number_of_prints, combo_delivery_type, entry_design_hours, entry_design_minutes, entry_travel_distance, urgent_checkbox, result_frame)).grid(column=0, row=0, padx=10)

    ttk.Button(button_frame, text="Sla Op Als PDF", command=lambda: save_as_pdf(result_frame.quote_data)).grid(column=1, row=0, padx=10)

    ttk.Button(button_frame, text="Opslaan in Applicatie", command=lambda: save_quote_in_app(entry_customer_name.get(), result_frame.quote_data)).grid(column=2, row=0, padx=10)

    app.mainloop()
