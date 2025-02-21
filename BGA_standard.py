import random
import math
import data_loader
from standard import generate_initial_schedule, calculate_schedule_cost

def binary_genertic_algorithm(flights, crew, population_size=30, generations=10, mutation_rate=0.1):
    # Define variables 

    def generate_individual():
        # Generate a random schedule
        return {flight: random.choice([crew_member for crew_member in crew if flight in crew[crew_member]['flights']]) for flight in flights}

    def calculate_fitness(schedule):
        return -calculate_schedule_cost(schedule, crew)
    
    def crossover(parent1, parent2):
        # Perform a single point crossover
        crossover_point = random.randint(0, len(flights) - 1)
        child1 = {**dict(list(parent1.items())[:crossover_point]), **dict(list(parent2.items())[crossover_point:])}
        child2 = {**dict(list(parent2.items())[:crossover_point]), **dict(list(parent1.items())[crossover_point:])}
        return child1, child2
    
    def mutate(individual):
        # Perform a random mutation
        if random.random() < mutation_rate:
            flight_to_mutate = random.choice(flights)
            eligible_crew = [crew_member for crew_member in crew if flight_to_mutate in crew[crew_member]['flights']]
            if eligible_crew:
                individual[flight_to_mutate] = random.choice(eligible_crew)
        return individual
    
    # Initialize the population
    population = [generate_individual() for _ in range(population_size)]

    for _ in range(generations):
        population = sorted(population, key=calculate_fitness, reverse=True)
        next_population = population[:10]

        while len(next_population) < population_size:
            parent1 = random.choice(population[:20])
            parent2 = random.choice(population[:20])
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            next_population.append(child1)
            next_population.append(child2)

        population = next_population

    best_solution = max(population, key=calculate_fitness)
    best_cost = -calculate_fitness(best_solution)
    return best_solution, best_cost


if __name__ == "__main__":
    # Load the data
    num_flights = data_loader.load_flights()
    flights = list(range(1, num_flights))

    attendants = data_loader.load_attendants()
    
    # Run the binary genetic algorithm
    best_schedule, best_cost = binary_genertic_algorithm(flights, attendants)

    # Print the best schedule and cost
    print(f"Best schedule: {best_schedule}")
    print(f"Best cost: {best_cost}")
    