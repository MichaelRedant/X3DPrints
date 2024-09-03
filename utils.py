# utils.py

import tkinter as tk
from tkinter import ttk
from settings import settings

def display_generated_quote(quote_data, frame):
    # Verwijder bestaande widgets in het frame
    for widget in frame.winfo_children():
        widget.destroy()

    ttk.Label(frame, text="Offerte Details", font=("Arial", 14, "bold")).grid(column=0, row=0, columnspan=2, pady=10)

    details = [
        ("Filament Type", quote_data.get('filament_type', 'Onbekend')),
        ("Prijs Filament / kg", f"€{quote_data.get('filament_price_per_kg', 0):.2f}"),
        ("Droogkosten", f"€{quote_data.get('drying_cost', 0):.2f}"),
        ("Huidige Elektriciteitsprijs", f"€{quote_data.get('electricity_price', 0):.2f} per kWh"),
        ("Prijs van Elektriciteit voor Print", f"€{quote_data.get('electricity_cost', 0):.2f}"),
        ("Gewicht van Print", f"{quote_data.get('filament_weight_grams', 0):.2f} gram"),
        ("Printtijd", f"{quote_data.get('printing_time_hours', 0):.2f} uur"),
        ("Leveringskosten", f"€{quote_data.get('delivery_cost', 0):.2f}"),
        ("Ontwerpkosten", f"€{quote_data.get('design_cost', 0):.2f}"),
        ("Ontwerptijd", f"{quote_data.get('design_hours', 0):.2f} uur"),
        ("Netto Prijs (zonder winst)", f"€{quote_data.get('netto_price', 0):.2f}"),
        ("Winstmarge", f"{settings['profit_margin']*100}%"),
        ("Bedrag met Winst", f"€{quote_data.get('total_price', 0):.2f}"),
        ("BTW Bedrag", f"€{quote_data.get('btw', 0):.2f}"),
        ("Totaal Bedrag", f"€{quote_data.get('total_price_with_btw', 0):.2f}")
    ]

    for i, (label, value) in enumerate(details):
        ttk.Label(frame, text=label, font=("Arial", 10, "bold")).grid(column=0, row=i+1, sticky=tk.W, pady=5)
        ttk.Label(frame, text=value, font=("Arial", 10)).grid(column=1, row=i+1, sticky=tk.W, pady=5)
