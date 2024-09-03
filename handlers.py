import os
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Listbox, ttk
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from quote_calculation import create_quote
import datetime
import logging
import webbrowser
from utils import display_generated_quote
from settings import settings

# Bestand voor offertes
OFFERS_FILE = "offertes.json"

def show_frame(frame):
    """Toon een specifiek frame en verberg de rest."""
    for widget in frame.master.winfo_children():
        widget.grid_remove()  # Verberg alle frames
    frame.grid(row=0, column=0, sticky="nsew")  # Toon het geselecteerde frame

def update_design_time_visibility(combo_design_choice, design_frame):
    """Zorg ervoor dat het ontwerptijd-frame alleen zichtbaar is als 'Eigen ontwerp' is geselecteerd."""
    if combo_design_choice.get() == "Eigen ontwerp":
        design_frame.grid()
    else:
        design_frame.grid_remove()

def update_delivery_related_fields(combo_delivery_type, travel_distance_label, entry_travel_distance, urgent_checkbox):
    """Pas de zichtbaarheid van leveringsgerelateerde velden aan op basis van het geselecteerde leveringsoptie."""
    if combo_delivery_type.get() in ["Zelf leveren", "Zelf leveren in spoed"]:
        travel_distance_label.grid()
        entry_travel_distance.grid()
        urgent_checkbox.grid()
    else:
        travel_distance_label.grid_remove()
        entry_travel_distance.grid_remove()
        urgent_checkbox.grid_remove()

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

def generate_quote(entry_print_hours, entry_print_minutes, entry_print_seconds, combo_filament_type, entry_filament_weight, entry_number_of_prints, combo_delivery_type, entry_design_hours, entry_design_minutes, entry_travel_distance, urgent_checkbox, result_frame, multi_print=False):
    """Genereer een offerte gebaseerd op de invoer."""
    try:
        logging.info("Start van de generate_quote functie.")
        
        # Validatie van invoervelden
        fields_to_validate = [entry_print_hours, entry_print_minutes, entry_print_seconds, combo_filament_type, entry_filament_weight]
        if not validate_fields(*fields_to_validate):
            messagebox.showerror("Fout", "Alle verplichte velden voor 1 print moeten worden ingevuld.")
            return
        
        printing_time_hours = (
            int(entry_print_hours.get() or 0) +
            int(entry_print_minutes.get() or 0) / 60 +
            int(entry_print_seconds.get() or 0) / 3600
        )
        filament_type = combo_filament_type.get()
        filament_weight_grams = float(entry_filament_weight.get().replace(',', '.') or 0)
        number_of_prints = int(entry_number_of_prints.get().replace(',', '.') or 1)  # Standaard naar 1 print
        delivery_type = combo_delivery_type.get()
        design_hours = (
            int(entry_design_hours.get() or 0) +
            int(entry_design_minutes.get() or 0) / 60
        )
        travel_distance_km = float(entry_travel_distance.get().replace(',', '.') or 0) if delivery_type in ["Zelf leveren", "Zelf leveren in spoed"] else 0
        urgent = urgent_checkbox.get() if delivery_type == "Zelf leveren in spoed" else False

        # Offerte data voor 1 print
        single_quote_data = create_quote(printing_time_hours, filament_type, filament_weight_grams, 1, delivery_type, design_hours, travel_distance_km, urgent)
        
        # Offerte data voor meerdere prints
        total_quote_data = None
        if multi_print and number_of_prints > 1:
            total_quote_data = create_quote(printing_time_hours, filament_type, filament_weight_grams, number_of_prints, delivery_type, design_hours, travel_distance_km, urgent)
        
        # Display results
        result_frame.quote_data = {
            "single": single_quote_data,
            "total": total_quote_data
        }
        display_generated_quote(result_frame.quote_data, result_frame)

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

def view_offer(index, frame, frames):
    """Bekijk een specifieke offerte in het hoofdvenster."""
    offers = load_offers_from_app()
    selected_offer = offers[index]

    # Haal de gegevens uit de opgeslagen offerte
    offer_data = selected_offer.get('quote_data', {})

    # Maak het frame voor het bekijken van offertes leeg
    for widget in frame.winfo_children():
        widget.destroy()

    # Voeg een terug knop toe
    ttk.Button(frame, text="Terug", command=lambda: show_frame(frames["history"])).pack(pady=10)

    # Voeg de offerte details toe aan het frame
    details = [
        ("Filament Type", offer_data.get('filament_type', 'Onbekend')),
        ("Prijs Filament / kg", f"€{offer_data.get('filament_price_per_kg', 0)}"),
        ("Droogkosten", f"€{offer_data.get('drying_cost', 0)}"),
        ("Huidige Elektriciteitsprijs", f"€{offer_data.get('electricity_price', 0)} per kWh"),
        ("Prijs van Elektriciteit voor Print", f"€{offer_data.get('electricity_cost', 0)}"),
        ("Gewicht van Print", f"{offer_data.get('filament_weight_grams', 0)} gram"),
        ("Printtijd", f"{offer_data.get('printing_time_hours', 0)} uur"),
        ("Leveringskosten", f"€{offer_data.get('delivery_cost', 0)}"),
        ("Ontwerpkosten", f"€{offer_data.get('design_cost', 0)}"),
        ("Ontwerptijd", f"{offer_data.get('design_hours', 0)} uur"),
        ("Netto Prijs (zonder winst)", f"€{offer_data.get('netto_price', 0)}"),
        ("Winstmarge", f"{settings['profit_margin']*100}%"),
        ("Bedrag met Winst", f"€{offer_data.get('total_price', 0)}"),
        ("BTW Bedrag", f"€{offer_data.get('btw', 0)}"),
        ("Totaal Bedrag", f"€{offer_data.get('total_price_with_btw', 0)}")
    ]

    for i, (label, value) in enumerate(details):
        ttk.Label(frame, text=label, font=("Arial", 10, "bold")).pack(anchor="w", pady=2)
        ttk.Label(frame, text=value, font=("Arial", 10)).pack(anchor="w", pady=2)

    # Toon het offerte detail frame
    show_frame(frame)
    
def show_offer_history(history_frame, show_frame, frames):
    """Toon een lijst van opgeslagen offertes."""
    offers = load_offers_from_app()
    if not offers:
        return

    def view_selected_offer():
        selection = listbox.curselection()
        if selection:
            view_offer(selection[0], history_frame, frames)

    def delete_offer(index):
        del offers[index]
        with open(OFFERS_FILE, 'w') as file:
            json.dump(offers, file, indent=4)
        listbox.delete(index)

    # Zorg ervoor dat je het frame leegmaakt
    for widget in history_frame.winfo_children():
        widget.destroy()

    # Voeg widgets opnieuw toe aan het history frame
    listbox = tk.Listbox(history_frame)
    for i, offer in enumerate(offers):
        customer_name = offer.get('customer_name', 'Onbekende klant')
        date = offer.get('date', 'Geen datum beschikbaar')
        listbox.insert(tk.END, f"{customer_name} - {date}")
    listbox.grid(row=0, column=0, columnspan=2, sticky="nsew")

    view_button = tk.Button(history_frame, text="Bekijk Offerte", command=view_selected_offer)
    view_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    delete_button = tk.Button(history_frame, text="Verwijder Offerte", command=lambda: delete_offer(listbox.curselection()[0]))
    delete_button.grid(row=1, column=1, padx=5, pady=5, sticky="e")

    back_button = ttk.Button(history_frame, text="Terug", command=lambda: show_frame(frames["home"]))
    back_button.grid(row=2, column=1, pady=10, sticky='e')
