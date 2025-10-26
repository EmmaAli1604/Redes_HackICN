from .NetworkSolution import NetworkSolution
import random
import numpy as np  
import copy         

class SA:
    def __init__(self, temp: float, cooling_rate : float, current_solution : NetworkSolution, size : int, rnd: random.Random, e : float, lim: int):
        self.initial_temperature = np.float64(temp)
        self.cooling_rate = np.float64(cooling_rate)
        self.e = np.float64(e)

        self.current_solution = current_solution
        
        # La mejor solución DEBE ser una copia profunda (deep copy) para evitar errores de referencia.
        self.best_solution = copy.deepcopy(current_solution)
        
        self.size_lote = size
        self.random = rnd
        self.limit = lim

    def calculate_lote(self):
        cost = np.float64(0.0)
        c = 0
        i = 0
        while c <= self.size_lote:
            if i == self.size_lote * self.limit:
                break
            
            vecino = self.current_solution.neighbour(self.random)
            
            # El vecino inválido se marca con -1 en el índice 0 (ID de nodo)
            if vecino[0] == -1:
                i += 1 # Contar la iteración aunque el vecino sea inválido
                continue
            
            print(vecino[1],self.current_solution.get_cost() + self.initial_temperature)
            if vecino[1] <= self.current_solution.get_cost() + self.initial_temperature:
                self.current_solution.update(vecino)
                c += 1
                cost += self.current_solution.get_cost()

                if self.current_solution.get_cost() < self.best_solution.get_cost():
                    # Guardar una copia profunda de la nueva mejor solución
                    self.best_solution = copy.deepcopy(self.current_solution)
                    print(f"Nuevo mejor costo encontrado: {self.best_solution.get_cost()}")
            i+=1
        
        # Evitar división por cero si 'c' (conteo de aceptados) es 0
        if c == 0:
            return (np.float64(0.0), i) 
            
        # Devolver el costo promedio de los 'c' aceptados
        return (cost / c, i)
    
    def accept_threshold(self):
        print("--- [SA] Iniciando recocido simulado por umbrales ...")
        p = np.float64(0.0)
        total = 0
        while self.initial_temperature > self.e:
            print(f"Temperatura actual: {self.initial_temperature}")
            q = np.inf
            while p <= q:
                q = p
                (new_p,i) = self.calculate_lote()
                p = new_p
                total += i
                if i == self.size_lote * self.limit:
                    print("Límite de iteraciones alcanzado. Terminando.")
                    return total
            self.initial_temperature *= self.cooling_rate
        print("Enfriamiento completado.")
        return total

    def get_best_solution(self):
        return self.best_solution.get_cost()