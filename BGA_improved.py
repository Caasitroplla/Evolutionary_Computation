import random
from standard import calculate_schedule_cost
import data_loader

def pseudo_random_initialization(flights, attendants):
    # Initialize the population with pseudo-random schedules
    schedule = {}
    uncovered_flights = set(flights)

    while uncovered_flights:
        flight = random.choice(list(uncovered_flights))
        eligible_attendants = [attendant for attendant in attendants if flight in attendants[attendant]['flights']]
        if eligible_attendants:
            assigned_attendant = random.choice(eligible_attendants)
            schedule[flight] = assigned_attendant
            uncovered_flights.remove(flight)
        else:
            uncovered_flights.remove(flight) # If no attendants available, leave uncovered
    return schedule

def heuristic_improvement(schedule, flights, attendants):
    # DROP Procedure: Remove over-assigned attendants 
    attendant_assignments = {a: 0 for a in attendants}
    for flight, assigned_attendant in schedule.items():
        attendant_assignments[assigned_attendant] += 1

    for flight, assigned_attendant in list(schedule.items()):
        if attendant_assignments[assigned_attendant] > len(flights) // len(attendants):
            schedule.pop(flight)
            attendant_assignments[assigned_attendant] -= 1

    # ADD Procedure: Ensure all flights are covered
    uncovered_flights = set(flights) - set(schedule.keys())
    for flight in uncovered_flights:
        eligible_attendants = [attendant for attendant in attendants if flight in attendants[attendant]['flights']]
        if eligible_attendants:
            schedule[flight] = min(eligible_attendants, key=lambda a: attendants[a]['cost'])

    return schedule

def calculate_constraint_violation(individual, flights, attendants):
    # Calculate the constraint violation of an individual
    violation = 0
    assigned_flights = set(individual.keys())
    violation += len(set(flights) - assigned_flights) # Unassigned flights
    attendant_assignment_counts = {crew: list(individual.values()).count(crew) for crew in attendants}
    max_assignments = len(flights) // len(attendants)
    violation += sum(max(0, count - max_assignments) for count in attendant_assignment_counts.values())
    return violation

def stochastic_ranking(population, flights, attendants):
    pf = 0.45
    N = len(population)
    # Fix: Calculate fitness by summing costs of assigned attendants in each schedule
    fitness_values = [-sum(attendants[schedule[flight]]['cost'] for flight in schedule) for schedule in population]
    constraint_violations = [calculate_constraint_violation(p, flights, attendants) for p in population]

    for i in range(N):
        for j in range(N - 1):
            u = random.random()
            if (u < pf and fitness_values[j] < fitness_values[j + 1]) or \
               (u >= pf and constraint_violations[j] > constraint_violations[j + 1]):
                population[j], population[j + 1] = population[j + 1], population[j]
                fitness_values[j], fitness_values[j + 1] = fitness_values[j + 1], fitness_values[j]
                constraint_violations[j], constraint_violations[j + 1] = constraint_violations[j + 1], constraint_violations[j]

    return population


def binary_genetic_algorithm(flights, attendants):
    # Define variables
    population_size = 50
    generations = 1000
    mutation_rate = 0.1
    
    def generate_individual():
        # Generate a random schedule
        return pseudo_random_initialization(flights, attendants)
        
    def mutate(individual):
        # Perform a random mutation
        if random.random() < mutation_rate:
            flight_to_mutate = random.choice(flights)
            eligible_attendants = [attendant for attendant in attendants if flight_to_mutate in attendants[attendant]['flights']]
            if eligible_attendants:
                individual[flight_to_mutate] = random.choice(eligible_attendants)
        return individual
    
    # Initialize the population
    population = [generate_individual() for _ in range(population_size)]
    
    for _ in range(generations):
        population = stochastic_ranking(population, flights, attendants)
        next_generation = population[:10]

        while len(next_generation) < population_size:
            parent1 = random.choice(population[:20])
            parent2 = random.choice(population[:20])
            child1 = parent1.copy()
            child2 = parent2.copy()

            next_generation.extend([mutate(child1), mutate(child2)])

        population = [heuristic_improvement(schedule, flights, attendants) for schedule in next_generation[:population_size]]

    best_solution = min(population, key=lambda x: calculate_constraint_violation(x, flights, attendants))
    best_cost = sum(attendants[best_solution[flight]]['cost'] for flight in best_solution)
    return best_solution, best_cost
            
    
if __name__ == "__main__":
    # Load the data
    num_flights = data_loader.load_flights()
    flights = list(range(1, num_flights))

    attendants = data_loader.load_attendants()

    # Run the binary genetic algorithm
    best_schedule, best_cost = binary_genetic_algorithm(flights, attendants)

    # Print the best schedule and cost
    print(f"Best schedule: {best_schedule}")
    print(f"Best cost: {best_cost}")