from settings import settings
import logging

def calculate_drying_cost(filament_type, number_of_prints):
    if filament_type in ["TPU", "PLA Wood", "PETG"]:
        hours = 8 if filament_type != "PLA Wood" else 4
        drying_cost = (hours * 0.145 * 0.07) * number_of_prints + 5  # Aanname van 5€ toeslag
        return drying_cost
    return 0

def create_quote(printing_time_hours, filament_type, filament_weight_grams, number_of_prints, delivery_type, design_hours, travel_distance_km, urgent):
    # Prijsberekeningen
    filament_cost_per_gram = settings["pla_prices"][filament_type] / 1000
    material_cost = filament_weight_grams * filament_cost_per_gram * number_of_prints
    drying_cost = calculate_drying_cost(filament_type, number_of_prints)

    # Berekening van elektriciteitskosten voor drogen
    drying_electricity_cost = 0
    if filament_type in ["TPU", "PLA Wood", "PETG"]:
        hours = 8 if filament_type != "PLA Wood" else 4
        drying_electricity_cost = hours * settings["electricity_price"] * 1.0 * number_of_prints

    # Netto prijs (zonder droogkosten)
    netto_price = material_cost + drying_electricity_cost

    # Elektriciteitskosten voor het printen
    electricity_cost = printing_time_hours * settings["electricity_price"] * 1.0  # Aanname: 1 kWh per uur printen

    if delivery_type == "Per post":
        delivery_cost = settings["delivery_costs"]["Per post"]
    elif delivery_type in ["Zelf leveren", "Zelf leveren in spoed"]:
        delivery_cost = settings["delivery_costs"]["Zelf leveren"]["spoed"] if urgent else settings["delivery_costs"]["Zelf leveren"]["normaal"]
        travel_cost = travel_distance_km * settings["travel_cost_per_km"]
        delivery_cost += travel_cost
    else:
        delivery_cost = 0
    
    design_cost = design_hours * settings["design_cost_per_hour"]

    # Totale kosten inclusief droogkosten
    total_cost = netto_price + electricity_cost + delivery_cost + design_cost + drying_cost
    total_price = total_cost * settings["profit_margin"]

    # Berekening van de BTW (21%)
    btw = total_price * 0.21
    total_price_with_btw = total_price + btw

    # Offerte data voor opslag
    return {
        "filament_type": filament_type,
        "filament_price_per_kg": settings["pla_prices"][filament_type],
        "drying_cost": drying_cost,
        "drying_electricity_cost": drying_electricity_cost,
        "electricity_price": settings["electricity_price"],
        "electricity_cost": electricity_cost,
        "filament_weight_grams": filament_weight_grams,
        "printing_time_hours": printing_time_hours,
        "delivery_cost": delivery_cost,
        "design_cost": design_cost,
        "design_hours": design_hours,
        "netto_price": netto_price,
        "total_price": total_price,
        "btw": btw,
        "total_price_with_btw": total_price_with_btw
    }
