import logging

# Configuratie voor logging
logging.basicConfig(
    filename="app_errors.log",  # Logbestand
    filemode="a",               # "a" voor append-modus, zodat logs worden toegevoegd aan het bestaande bestand
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.ERROR         # Log alleen fouten
)

from gui import create_main_window

if __name__ == "__main__":
    create_main_window()
