import os
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Listbox
from tkinter import ttk  # Importeer ttk voor de widgets
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from quote_calculation import create_quote
import datetime
import logging
import webbrowser
from utils import display_generated_quote
from settings import settings  # Importeer settings

# Bestand voor offertes
OFFERS_FILE = "offertes.json"

def validate_print_time(entry_print_hours, entry_print_minutes, entry_print_seconds):
    """Controleert of ten minste één veld voor printtijd is ingevuld."""
    return any([
        entry_print_hours.get(),
        entry_print_minutes.get(),
        entry_print_seconds.get()
    ])

def validate_fields(*fields):
    """Controleert of alle verplichte velden zijn ingevuld."""
    for field in fields:
        if not field.get():
            return False
    return True

def save_quote_in_app(customer_name, quote_data):
    """Sla de offerte op in de applicatie."""
    if not customer_name:
        messagebox.showerror("Fout", "De offerte kan niet worden opgeslagen zonder een klantnaam.")
        return
    
    try:
        if not os.path.exists(OFFERS_FILE):
            offers = []
        else:
            with open(OFFERS_FILE, 'r') as file:
                offers = json.load(file)

        offer_data = {
            "customer_name": customer_name,
            "quote_data": quote_data,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        offers.append(offer_data)

        with open(OFFERS_FILE, 'w') as file:
            json.dump(offers, file, indent=4)

        messagebox.showinfo("Opgeslagen", "Offerte succesvol opgeslagen in de applicatie.")
    except Exception as e:
        logging.error(f"Fout bij het opslaan van de offerte: {e}")
        messagebox.showerror("Fout", f"Er is een fout opgetreden bij het opslaan van de offerte: {e}")

def save_as_pdf(quote_data):
    """Slaat de offerte op als PDF."""
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                             filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    if file_path:
        try:
            c = canvas.Canvas(file_path, pagesize=letter)
            width, height = letter

            y = height - 40
            for key, value in quote_data.items():
                if key != "netto_price":  # We laten de netto prijs weg uit de PDF
                    line = f"{key}: {value}"
                    c.drawString(40, y, line)
                y -= 12  # Regelafstand
            
            c.save()
            messagebox.showinfo("Opgeslagen", "Offerte succesvol opgeslagen als PDF")
        except Exception as e:
            logging.error(f"Fout bij het opslaan van de offerte als PDF: {e}")
            messagebox.showerror("Fout", f"Er is een fout opgetreden bij het opslaan van de offerte als PDF: {e}")

def generate_quote(entry_print_hours, entry_print_minutes, entry_print_seconds, combo_filament_type, entry_filament_weight, entry_number_of_prints, combo_delivery_type, entry_design_hours, entry_design_minutes, entry_travel_distance, urgent_checkbox, result_frame):
    """Genereer een offerte gebaseerd op de invoer."""
    try:
        logging.info("Start van de generate_quote functie.")
        
        # Validatie van invoervelden
        if not validate_print_time(entry_print_hours, entry_print_minutes, entry_print_seconds):
            messagebox.showerror("Fout", "Vul ten minste één veld in voor de printtijd (uren, minuten of seconden).")
            return
        
        fields_to_validate = [combo_filament_type, entry_filament_weight, entry_number_of_prints, combo_delivery_type]
        if not validate_fields(*fields_to_validate):
            messagebox.showerror("Fout", "Alle verplichte velden moeten worden ingevuld.")
            return
        
        printing_time_hours = (
            int(entry_print_hours.get() or 0) +
            int(entry_print_minutes.get() or 0) / 60 +
            int(entry_print_seconds.get() or 0) / 3600
        )
        filament_type = combo_filament_type.get()
        filament_weight_grams = float(entry_filament_weight.get().replace(',', '.') or 0)
        number_of_prints = int(entry_number_of_prints.get().replace(',', '.') or 0)
        delivery_type = combo_delivery_type.get()
        design_hours = (
            int(entry_design_hours.get() or 0) +
            int(entry_design_minutes.get() or 0) / 60
        )
        travel_distance_km = float(entry_travel_distance.get().replace(',', '.') or 0) if delivery_type in ["Zelf leveren", "Zelf leveren in spoed"] else 0
        urgent = urgent_checkbox.get() if delivery_type == "Zelf leveren in spoed" else False

        quote_data = create_quote(printing_time_hours, filament_type, filament_weight_grams, number_of_prints, delivery_type, design_hours, travel_distance_km, urgent)
        
        result_frame.quote_data = quote_data
        display_generated_quote(quote_data, result_frame)

    except Exception as e:
        logging.error(f"Fout bij het genereren van de offerte: {e}")
        tk.messagebox.showerror("Error", f"Er is een fout opgetreden: {e}")

def show_info():
    """Toon informatie over de applicatie."""
    info_window = Toplevel()
    info_window.title("Over deze applicatie")
    info_text = tk.Text(info_window, wrap="word", height=10, width=50, background="#ffffff", borderwidth=0)
    info_text.grid(padx=10, pady=10)

    info_message = (
        "Deze applicatie is ontwikkeld door Michaël Redant van Xinudesign in 2024.\n"
        "Voor meer informatie over zijn werk, kunt u terecht op de website "
        "<a href='https://www.xinudesign.be'>Xinudesign.be</a>.\n\n"
        "Deze specifieke applicatie is gemaakt voor X3DPrints en biedt op maat gemaakte "
        "3D-printoplossingen. Bezoek hun website op <a href='https://www.x3dprints.be'>X3DPrints.be</a> "
        "voor meer details over hun diensten en producten."
    )

    def open_url(event):
        webbrowser.open_new(event.widget.cget("text"))

    info_text.insert(tk.END, info_message)
    info_text.tag_add("url", "1.49", "1.69")
    info_text.tag_add("url2", "3.77", "3.99")
    info_text.tag_config("url", foreground="blue", underline=True)
    info_text.tag_config("url2", foreground="blue", underline=True)
    info_text.tag_bind("url", "<Button-1>", open_url)
    info_text.tag_bind("url2", "<Button-1>", open_url)

def load_offers_from_app():
    """Laad de opgeslagen offertes uit het bestand."""
    try:
        if not os.path.exists(OFFERS_FILE):
            messagebox.showinfo("Geen Offertes", "Er zijn geen offertes opgeslagen.")
            return []

        with open(OFFERS_FILE, 'r') as file:
            offers = json.load(file)

        return offers
    except Exception as e:
        logging.error(f"Fout bij het laden van offertes: {e}")
        messagebox.showerror("Fout", f"Er is een fout opgetreden bij het laden van offertes: {e}")
        return []

def view_offer(index):
    """Bekijk een specifieke offerte."""
    offers = load_offers_from_app()
    selected_offer = offers[index]

    # Haal de gegevens uit de opgeslagen offerte
    offer_data = selected_offer.get('quote_data', {})

    # Creëer een nieuw venster om de offerte weer te geven
    view_window = Toplevel()
    view_window.title(f"Offerte voor {selected_offer.get('customer_name', 'Onbekende klant')}")

    frame = ttk.Frame(view_window, padding="20")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(frame, text="Offerte Details", font=("Arial", 14, "bold")).grid(column=0, row=0, columnspan=2, pady=10)

    # Offerte details weergeven in labels
    details = [
        ("Filament Type", offer_data.get('filament_type', 'Onbekend')),
        ("Prijs Filament / kg", f"€{round(offer_data.get('filament_price_per_kg', 0), 2)}"),
        ("Droogkosten", f"€{round(offer_data.get('drying_cost', 0), 2)}"),
        ("Huidige Elektriciteitsprijs", f"€{round(offer_data.get('electricity_price', 0), 2)} per kWh"),
        ("Prijs van Elektriciteit voor Print", f"€{round(offer_data.get('electricity_cost', 0), 2)}"),
        ("Gewicht van Print", f"{offer_data.get('filament_weight_grams', 0)} gram"),
        ("Printtijd", f"{int(offer_data.get('printing_time_hours', 0))} uur {int((offer_data.get('printing_time_hours', 0) * 60) % 60)} min"),
        ("Leveringskosten", f"€{round(offer_data.get('delivery_cost', 0), 2)}"),
        ("Ontwerpkosten", f"€{round(offer_data.get('design_cost', 0), 2)}"),
        ("Ontwerptijd", f"{offer_data.get('design_hours', 0)} uur"),
        ("Netto Prijs (zonder winst)", f"€{round(offer_data.get('netto_price', 0), 2)}"),
        ("Winstmarge", f"{settings['profit_margin']*100}%"),
        ("Bedrag met Winst", f"€{round(offer_data.get('total_price', 0), 2)}"),
        ("BTW Bedrag", f"€{round(offer_data.get('btw', 0), 2)}"),
        ("Totaal Bedrag", f"€{round(offer_data.get('total_price_with_btw', 0), 2)}")
    ]

    for i, (label, value) in enumerate(details):
        ttk.Label(frame, text=label, font=("Arial", 10, "bold")).grid(column=0, row=i+1, sticky=tk.W, pady=5)
        ttk.Label(frame, text=value, font=("Arial", 10)).grid(column=1, row=i+1, sticky=tk.W, pady=5)

    # Voeg een "Sluiten" knop toe
    ttk.Button(frame, text="Sluiten", command=view_window.destroy).grid(column=1, row=len(details)+1, pady=10, sticky=tk.E)

def show_offer_history():
    """Toon een lijst van opgeslagen offertes."""
    offers = load_offers_from_app()
    if not offers:
        return

    def view_selected_offer():
        selection = listbox.curselection()
        if selection:
            view_offer(selection[0])

    def delete_offer(index):
        del offers[index]
        with open(OFFERS_FILE, 'w') as file:
            json.dump(offers, file, indent=4)
        listbox.delete(index)

    history_window = Toplevel()
    history_window.title("Offertes")

    listbox = Listbox(history_window)
    for i, offer in enumerate(offers):
        customer_name = offer.get('customer_name', 'Onbekende klant')
        date = offer.get('date', 'Geen datum beschikbaar')
        listbox.insert(tk.END, f"{customer_name} - {date}")
    listbox.grid(row=0, column=0, columnspan=2, sticky="nsew")

    view_button = tk.Button(history_window, text="Bekijk Offerte", command=view_selected_offer)
    view_button.grid(row=1, column=0, padx=5, pady=5)

    delete_button = tk.Button(history_window, text="Verwijder Offerte", command=lambda: delete_offer(listbox.curselection()[0]))
    delete_button.grid(row=1, column=1, padx=5, pady=5)

    history_window.mainloop()
