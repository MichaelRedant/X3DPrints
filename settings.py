import tkinter as tk
from tkinter import ttk, messagebox
from styles import apply_styles

# Globale instellingen voor prijzen en kosten
settings = {
    "electricity_price": 0.23,  # Bijv. 0.23 EUR/kWh, vervang dit met de juiste waarde
    "pla_prices": {
        "PLA Basic": 23.38,
        "PLA Matte": 23.38,
        "PLA Basic Gradient": 33.54,
        "PLA Silk": 33.54,
        "PLA Silk Dual Color": 33.54,
        "PLA Metal": 33.54,
        "PLA Galaxy": 32.52,
        "PLA Sparkle": 33.54,
        "PLA Marble": 33.54,
        "PLA Glow": 33.54,
        "PLA-CF": 39.64,
        "TPU": 25.50,
        "PETG": 23.38,
        "PLA Wood": 28.46,
    },
    "profit_margin": 1.5,  # 150% winst
    "design_cost_per_hour": 40,
    "travel_cost_per_km": 0.35,
    "delivery_costs": {
        "Per post": 7.00,
        "Zelf leveren": {
            "normaal": 15.00,
            "spoed": 20.00,
        },
    },
}

def open_settings_window():
    settings_window = tk.Toplevel()
    settings_window.title("Instellingen")
    settings_window.geometry("800x600")  # Volledige breedte van het scherm gebruiken

    # Pas de centrale stijlen toe
    apply_styles(settings_window)

    canvas = tk.Canvas(settings_window)
    scrollbar = ttk.Scrollbar(settings_window, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Scrollen met muiswiel mogelijk maken
    scrollable_frame.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    ttk.Label(scrollable_frame, text="Filament Prijzen (per kg):").grid(column=0, row=0, columnspan=2, sticky=tk.W, pady=10)
    row = 1
    filament_entries = {}
    for filament_type, price in settings["pla_prices"].items():
        ttk.Label(scrollable_frame, text=filament_type).grid(column=0, row=row, sticky=tk.W, pady=5)
        filament_entry = ttk.Entry(scrollable_frame)
        filament_entry.insert(0, str(price))
        filament_entry.grid(column=1, row=row, pady=5, sticky=tk.EW)
        filament_entries[filament_type] = filament_entry
        row += 1

    ttk.Label(scrollable_frame, text="Leveringskosten:").grid(column=0, row=row, columnspan=2, sticky=tk.W, pady=10)
    row += 1
    ttk.Label(scrollable_frame, text="Per post (€):").grid(column=0, row=row, sticky=tk.W, pady=5)
    delivery_post_entry = ttk.Entry(scrollable_frame)
    delivery_post_entry.insert(0, str(settings["delivery_costs"]["Per post"]))
    delivery_post_entry.grid(column=1, row=row, pady=5, sticky=tk.EW)
    row += 1
    ttk.Label(scrollable_frame, text="Zelf leveren (€):").grid(column=0, row=row, sticky=tk.W, pady=5)
    delivery_own_normal_entry = ttk.Entry(scrollable_frame)
    delivery_own_normal_entry.insert(0, str(settings["delivery_costs"]["Zelf leveren"]["normaal"]))
    delivery_own_normal_entry.grid(column=1, row=row, pady=5, sticky=tk.EW)
    row += 1
    ttk.Label(scrollable_frame, text="Zelf leveren in spoed (€):").grid(column=0, row=row, sticky=tk.W, pady=5)
    delivery_own_urgent_entry = ttk.Entry(scrollable_frame)
    delivery_own_urgent_entry.insert(0, str(settings["delivery_costs"]["Zelf leveren"]["spoed"]))
    delivery_own_urgent_entry.grid(column=1, row=row, pady=5, sticky=tk.EW)
    row += 1

    ttk.Label(scrollable_frame, text="Ontwerpkosten (per uur, €):").grid(column=0, row=row, sticky=tk.W, pady=10)
    design_cost_entry = ttk.Entry(scrollable_frame)
    design_cost_entry.insert(0, str(settings["design_cost_per_hour"]))
    design_cost_entry.grid(column=1, row=row, pady=5, sticky=tk.EW)
    row += 1

    ttk.Label(scrollable_frame, text="Reiskosten (per km, €):").grid(column=0, row=row, sticky=tk.W, pady=10)
    travel_cost_entry = ttk.Entry(scrollable_frame)
    travel_cost_entry.insert(0, str(settings["travel_cost_per_km"]))
    travel_cost_entry.grid(column=1, row=row, pady=5, sticky=tk.EW)
    row += 1

    ttk.Label(scrollable_frame, text="Winstmarge (%):").grid(column=0, row=row, sticky=tk.W, pady=10)
    profit_margin_entry = ttk.Entry(scrollable_frame)
    profit_margin_entry.insert(0, str(settings["profit_margin"] * 100))
    profit_margin_entry.grid(column=1, row=row, pady=5, sticky=tk.EW)
    row += 1

    def save_settings():
        try:
            for filament_type, entry in filament_entries.items():
                settings["pla_prices"][filament_type] = float(entry.get())

            settings["delivery_costs"]["Per post"] = float(delivery_post_entry.get())
            settings["delivery_costs"]["Zelf leveren"]["normaal"] = float(delivery_own_normal_entry.get())
            settings["delivery_costs"]["Zelf leveren"]["spoed"] = float(delivery_own_urgent_entry.get())
            settings["design_cost_per_hour"] = float(design_cost_entry.get())
            settings["travel_cost_per_km"] = float(travel_cost_entry.get())
            settings["profit_margin"] = float(profit_margin_entry.get()) / 100

            messagebox.showinfo("Instellingen", "Instellingen succesvol opgeslagen.")
            settings_window.destroy()
        except ValueError:
            messagebox.showerror("Fout", "Ongeldige invoer. Zorg ervoor dat alle velden correcte numerieke waarden bevatten.")

    ttk.Button(scrollable_frame, text="Opslaan", command=save_settings, style="TButton").grid(column=0, row=row, columnspan=2, pady=20)
