import tkinter as tk
from tkinter import ttk, messagebox
from settings import open_settings_window, settings
from handlers import generate_quote, save_as_pdf, show_info, show_offer_history, save_quote_in_app, show_frame, update_design_time_visibility, update_delivery_related_fields
from styles import apply_styles

# Validatiefunctie voor numerieke invoer
def validate_numeric_input(action, value_if_allowed):
    if action != '1':  # Actie '1' betekent dat de invoer wordt toegevoegd
        return True
    try:
        float(value_if_allowed.replace(',', '.'))  # Ondersteunt zowel ',' als '.' als decimaal
        return True
    except ValueError:
        return False

def create_main_window():
    app = tk.Tk()
    app.title("3D Print Offerte Generator")

    # Pas de centrale stijlen toe
    apply_styles(app)

    main_frame = ttk.Frame(app, padding="10")
    main_frame.grid(row=0, column=0, sticky="nsew")

    # Maak de menubalk aan
    menubar = tk.Menu(app)
    app.config(menu=menubar)

    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Instellingen", command=open_settings_window)
    file_menu.add_command(label="Bekijk Offertes", command=lambda: show_offer_history(history_frame, show_frame, frames))
    file_menu.add_separator()
    file_menu.add_command(label="Afsluiten", command=app.quit)
    menubar.add_cascade(label="Bestand", menu=file_menu)

    info_menu = tk.Menu(menubar, tearoff=0)
    info_menu.add_command(label="Over", command=show_info)
    menubar.add_cascade(label="Info", menu=info_menu)

    # Frames voor verschillende secties
    home_frame = ttk.Frame(main_frame, padding="10")
    home_frame.grid(row=0, column=0, sticky="nsew")
    quote_frame = ttk.Frame(main_frame, padding="10")
    quote_frame.grid(row=0, column=0, sticky="nsew")
    history_frame = ttk.Frame(main_frame, padding="10")
    history_frame.grid(row=0, column=0, sticky="nsew")
    
    # Voeg frames toe aan een dictionary voor eenvoudig toegang
    frames = {
        "home": home_frame,
        "quote": quote_frame,
        "history": history_frame
    }

    # Home Frame: Hoofdmenu
    ttk.Label(home_frame, text="Welkom bij de 3D Print Offerte Generator", font=("Arial", 14, "bold")).grid(pady=20)
    ttk.Button(home_frame, text="Nieuwe Offerte", command=lambda: show_frame(quote_frame)).grid(pady=10)
    ttk.Button(home_frame, text="Bekijk Offertes", command=lambda: show_offer_history(history_frame, show_frame, frames)).grid(pady=10)
    ttk.Button(home_frame, text="Instellingen", command=open_settings_window).grid(pady=10)

    # Quote Frame: Offerte genereren
    back_button = ttk.Button(quote_frame, text="Terug", command=lambda: show_frame(home_frame))
    back_button.grid(row=0, column=2, pady=10, sticky=tk.E)

    result_frame = ttk.Frame(quote_frame)
    result_frame.grid(row=12, column=0, columnspan=2, sticky="nsew")

    # Validatieconfiguratie
    vcmd = (app.register(validate_numeric_input), '%d', '%P')

    # Klantnaam
    ttk.Label(quote_frame, text="Klant:").grid(column=0, row=0, sticky=tk.W, pady=10)
    entry_customer_name = ttk.Entry(quote_frame)
    entry_customer_name.grid(column=1, row=0, sticky=tk.EW, pady=10)

    # Filament type
    ttk.Label(quote_frame, text="Filament type:").grid(column=0, row=1, sticky=tk.W, pady=10)
    combo_filament_type = ttk.Combobox(quote_frame, values=list(settings["pla_prices"].keys()), state="readonly")
    combo_filament_type.grid(column=1, row=1, sticky=tk.EW, pady=10)

    # Ontwerp keuze
    ttk.Label(quote_frame, text="Ontwerpkeuze:").grid(column=0, row=2, sticky=tk.W, pady=10)
    combo_design_choice = ttk.Combobox(quote_frame, values=["Klantontwerp", "Eigen ontwerp"], state="readonly")
    combo_design_choice.grid(column=1, row=2, sticky=tk.EW, pady=10)
    combo_design_choice.bind("<<ComboboxSelected>>", lambda e: update_design_time_visibility(combo_design_choice, design_frame))

    # Printtijd voor 1 print
    ttk.Label(quote_frame, text="Printtijd voor 1 print:").grid(column=0, row=3, sticky=tk.W, pady=10)
    entry_print_hours = ttk.Entry(quote_frame, width=5, validate="key", validatecommand=vcmd)
    entry_print_hours.grid(column=1, row=3, sticky=tk.W)
    ttk.Label(quote_frame, text="uur").grid(column=1, row=3, padx=(60, 0), sticky=tk.W)

    entry_print_minutes = ttk.Entry(quote_frame, width=5, validate="key", validatecommand=vcmd)
    entry_print_minutes.grid(column=1, row=3, padx=(120, 0), sticky=tk.W)
    ttk.Label(quote_frame, text="min").grid(column=1, row=3, padx=(180, 0), sticky=tk.W)

    entry_print_seconds = ttk.Entry(quote_frame, width=5, validate="key", validatecommand=vcmd)
    entry_print_seconds.grid(column=1, row=3, padx=(240, 0), sticky=tk.W)
    ttk.Label(quote_frame, text="sec").grid(column=1, row=3, padx=(300, 0), sticky=tk.W)

    # Gewicht van 3D print voor 1 print
    ttk.Label(quote_frame, text="Gewicht van 3D print voor 1 print (gram):").grid(column=0, row=4, sticky=tk.W, pady=10)
    entry_filament_weight = ttk.Entry(quote_frame, validate="key", validatecommand=vcmd)
    entry_filament_weight.grid(column=1, row=4, sticky=tk.EW, pady=10)

    # Aantal prints
    ttk.Label(quote_frame, text="Aantal prints:").grid(column=0, row=5, sticky=tk.W, pady=10)
    entry_number_of_prints = ttk.Entry(quote_frame, validate="key", validatecommand=vcmd)
    entry_number_of_prints.grid(column=1, row=5, sticky=tk.EW, pady=10)

    # Leveringstype
    ttk.Label(quote_frame, text="Leveringstype:").grid(column=0, row=6, sticky=tk.W, pady=10)
    combo_delivery_type = ttk.Combobox(quote_frame, values=["Geen", "Per post", "Zelf leveren", "Zelf leveren in spoed"], state="readonly")
    combo_delivery_type.grid(column=1, row=6, sticky=tk.EW, pady=10)
    combo_delivery_type.bind("<<ComboboxSelected>>", lambda e: update_delivery_related_fields(combo_delivery_type, travel_distance_label, entry_travel_distance, urgent_checkbox))

    # Ontwerptijd (zichtbaar als Eigen ontwerp is geselecteerd)
    design_frame = ttk.Frame(quote_frame)
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
    travel_distance_label = ttk.Label(quote_frame, text="Reisafstand (km):")
    travel_distance_label.grid(column=0, row=8, sticky=tk.W, pady=10)
    entry_travel_distance = ttk.Entry(quote_frame, validate="key", validatecommand=vcmd)
    entry_travel_distance.grid(column=1, row=8, sticky=tk.EW, pady=10)
    urgent_checkbox = ttk.Checkbutton(quote_frame, text="Spoedlevering")
    urgent_checkbox.grid(column=1, row=9, sticky=tk.W, pady=10)
    travel_distance_label.grid_remove()
    entry_travel_distance.grid_remove()
    urgent_checkbox.grid_remove()

    # Resultaat frame
    result_frame = ttk.Frame(quote_frame)
    result_frame.grid(column=0, row=12, columnspan=2, sticky=tk.EW, pady=10)

    # Knoppen toevoegen
    button_frame = ttk.Frame(quote_frame)
    button_frame.grid(column=0, row=10, columnspan=2, pady=20)

    ttk.Button(button_frame, text="Genereer Offerte", command=lambda: generate_quote(entry_print_hours, entry_print_minutes, entry_print_seconds, combo_filament_type, entry_filament_weight, entry_number_of_prints, combo_delivery_type, entry_design_hours, entry_design_minutes, entry_travel_distance, urgent_checkbox, result_frame)).grid(column=0, row=0, padx=10)

    ttk.Button(button_frame, text="Sla Op Als PDF", command=lambda: save_as_pdf(result_frame.quote_data)).grid(column=1, row=0, padx=10)

    ttk.Button(button_frame, text="Opslaan in Applicatie", command=lambda: save_quote_in_app(entry_customer_name.get(), result_frame.quote_data)).grid(column=2, row=0, padx=10)

    show_frame(home_frame)

    app.mainloop()
