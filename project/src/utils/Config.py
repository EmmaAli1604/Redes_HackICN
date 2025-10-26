import os
from dotenv import load_dotenv

class Config:
    """
    Carga la configuración del proyecto desde un archivo .env.
    
    Lee las variables de entorno y las castea al tipo numérico correcto
    (float o int) como atributos de la clase.
    """
    
    def __init__(self):
        # Carga las variables del archivo .env en el entorno de os.environ
        load_dotenv() 
        
        try:
            # Leemos las variables de os.environ y las casteamos al tipo correcto
            
            # Floats
            self.initial_temperature = float(os.environ['INITIAL_TEMPERATURE'])
            self.cooling_rate = float(os.environ['COOLING_RATE'])
            self.e_s = float(os.environ['E_S'])
            self.e_p = float(os.environ['E_P'])
            self.percentage = float(os.environ['PERCENTAGE'])
            
            # Integers
            self.size_lote = int(os.environ['SIZE_LOTE'])
            self.limit = int(os.environ['LIMIT'])
            self.n = int(os.environ['N'])
        
        except KeyError as e:
            # Se produce si una variable clave no se encuentra en el .env
            print(f"Error: La variable de entorno {e} no está definida en tu .env")
            # Detenemos la ejecución si falta configuración crítica
            raise SystemExit(f"Configuración faltante: {e}") 
        
        except ValueError as e:
            # Se produce si el valor no se puede convertir (ej. "abc" en lugar de 1000)
            print(f"Error: El valor de una variable en .env tiene el tipo incorrecto.")
            print(f"Detalle: {e}")
            raise SystemExit("Error de tipo en .env")