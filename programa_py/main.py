# Importació de les llibreries necessàries
import bloc_logging
from dotenv import load_dotenv

def main():
    """Funció principal que inicia l'aplicació"""
    # Crida a la funció logger per iniciar el sistema d'autenticació
    bloc_logging.logger()

# Punt d'entrada del programa
if __name__ == "__main__":
    main()
