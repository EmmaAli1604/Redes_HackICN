import random
import NetworkSolution


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
        solution : NetworkSolution.NetworkSolution,
        n: int,
        seed: int
    ):
        """
        Constructor de la clase'.
        """
        self.temperature = temperature
        self.percentage = percentage
        self.e_p = e_p 
        self.solution = solution
        self.n = n  
        
        self.random = random.Random(seed)

    def get_initial_t(self, limit: int) -> float:
        """
        Calcula la temperatura inicial.
        """
        p = self._accept_percentage()
        if abs(self.percentage - p) <= self.e_p:
            return self.temperature

        t1: float
        t2: float
        
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

        return self._binary_search(t1, t2)

    def _accept_percentage(self) -> float:
        """
        Método auxiliar "privado".
        """
        c = 0.0
        for _ in range(self.n):
            vecino = self.solution.neighbour()
            
            if vecino[1] <= self.path.get_cost() + self.temperature:
                self.solution.update(vecino)
                c += 1.0
        
        return c / self.n

    def _binary_search(self, t_1: float, t_2: float) -> float:
        """
        Método auxiliar "privado".
        Equivalente a 'binary_search'.
        """
        t_m = (t_1 + t_2) / 2.0
        if (t_2 - t_1) < self.e_p:
            return t_m

        p = self._accept_percentage()
        if abs(self.percentage - p) < self.e_p:
            return t_m
        
        if p > self.percentage:
            return self._binary_search(t_1, t_m)

        return self._binary_search(t_m, t_2)
