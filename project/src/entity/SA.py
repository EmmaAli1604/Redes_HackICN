import entityNetworkSolution
import random

class SA:
    def __init__(self, temp: float, cooling_rate : float, current_solution : entityNetworkSolution, size : int, rnd: random.Random, e : float, lim: int):
        self.initial_temperature = temp
        self.cooling_rate = cooling_rate
        self.best_solution = self.current_solution = current_solution
        self.size_lote = size
        self.random = rnd
        self.e = e 
        self.limit = lim

    def calculate_lote(self):
        cost = 0.0
        c = 0
        i = 0
        while c <= self.size_lote:
            if i == self.size_lote * self.limit:
                break
            
            vecino = self.current_solution.neighbour()
            
            if vecino[1] <= self.current_solution.get_cost() + self.initial_temperature:
                self.currenti_solution.update(vecino);
                c += 1
                cost += self.current_solution.get_cost()

                if self.current_solution.get_cost() < self.best_solution.get_cost():
                    self.best_solution = self.current_solution
            i+=1
        return (cost/self.size_lote,i)
    
    def accept_threshold(self):
        p = 0
        total = 0
        while self.initial_temperature > self.e:
            q = float('inf')
            while p <= q:
                q = p
                (new_p,i) = self.calculate_lote()
                p = new_p
                total += i
                if i == self.size_lote * self.limit:
                    return total
            self.initial_temperature *= self.cooling_rate
        return total

    def get_best_solution(self):
        return self.best_solution
                
