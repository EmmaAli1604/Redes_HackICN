import random
import numpy as np  # <-- AÑADIDO
from .NetworkSolution import NetworkSolution


class InitialTemperature:
    """
    Traducción de la estructura 'InitialTemperature' de Rust.
    Calcula la temperatura inicial para un algoritmo de Simulated Annealing.
    """

    def __init__(
        self,
        temperature: float,
        percentage: float,
        e_p: float,
        solution : NetworkSolution,
        n: int,
        seed: int
    ):
        """
        Constructor de la clase'.
        """
        # --- CAMBIO: Usar np.float64 ---
        self.temperature = np.float64(temperature)
        self.percentage = np.float64(percentage)
        self.e_p = np.float64(e_p)
        self.solution = solution
        self.n = n  
        
        self.random = random.Random(seed)

    def get_initial_t(self, limit: int) -> np.float64: # <-- CAMBIO
        """
        Calcula la temperatura inicial.
        """
        print("--- [Temp] Iniciando cálculo de Temperatura Inicial...")
        p = self._accept_percentage()
        print("------")
        print(p)
        print(self.percentage)
        print(abs(self.percentage - p),self.e_p)
        if abs(self.percentage - p) <= self.e_p:
            print(self.temperature)
            return self.temperature

    
        t1: np.float64 # <-- CAMBIO (opcional, pero bueno para claridad)
        t2: np.float64 # <-- CAMBIO (opcional)
        
        i = 0 
        
        if p < self.percentage:
            while p < self.percentage:
                if i == limit:
                    break
                self.temperature *= 2.0
                p = self._accept_percentage()
                i += 1
            
            t1 = self.temperature / 2.0
            t2 = self.temperature
        else:
            while p > self.percentage:
                if i == limit:
                    break
                self.temperature /= 2.0
                p = self._accept_percentage()
                i += 1
            
            t1 = self.temperature
            t2 = self.temperature * 2.0

        if i == limit:
            return self.temperature
        print("--- [Temp] Iniciando búsqueda binaria de temperatura...")

        return self._binary_search(t1, t2)

    def _accept_percentage(self) -> np.float64: # <-- CAMBIO
        """
        Método auxiliar "privado".
        """
        # --- CAMBIO: Usar np.float64 ---
        c = np.float64(0.0)
        for _ in range(self.n):
            vecino = self.solution.neighbour(self.random)
            if vecino[0] == -1: # <-- Esto ya estaba correcto
                continue
            if vecino[1] <= self.solution.get_cost() + self.temperature:
                self.solution.update(vecino)
                c += 1.0
        print(c / self.n)
        return c / self.n

    def _binary_search(self, t_1: np.float64, t_2: np.float64) -> np.float64: # <-- CAMBIO
        """
        Método auxiliar "privado".
        """
        # --- CAMBIO: Usar np.float64 ---
        t_m = (t_1 + t_2) / np.float64(2.0)
        if (t_2 - t_1) < self.e_p:
            return t_m

        p = self._accept_percentage()
        if abs(self.percentage - p) < self.e_p:
            return t_m
        
        if p > self.percentage:
            return self._binary_search(t_1, t_m)

        return self._binary_search(t_m, t_2)