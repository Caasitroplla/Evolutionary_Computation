import random
import data_loader

def calculate_schedule_cost(schedule, crew):
    return sum(crew[schedule[flight]]['cost'] for flight in schedule if schedule[flight] is not None)


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
            uncovered_flights -= {flight}
        else:
            uncovered_flights -= {flight}    # If no attendants available, leave uncovered
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
    attendant_assignment_counts = {a: list(individual.values()).count(a) for a in attendants}
    max_assignments = len(flights) // len(attendants)
    violation += sum(max(0, count - max_assignments) for count in attendant_assignment_counts.values())
    return violation

def calculate_fitness(x, attendants):
    return -sum(attendants[x[flight]]['cost'] for flight in x)

def stochastic_ranking(population, flights, attendants):
    # Convert population members to tuples so they can be used as dictionary keys
    population_tuples = [tuple(sorted(x.items())) for x in population]
    constraints_violations = {pop_tuple: calculate_constraint_violation(dict(pop_tuple), flights, attendants) 
                            for pop_tuple in population_tuples}
    
    fitness_values = [calculate_fitness(dict(pop_tuple), attendants) for pop_tuple in population_tuples]
    
    # Create a mapping of population tuples to fitness values
    fitness_dict = dict(zip(population_tuples, fitness_values))
    
    # Sort using both dictionaries
    population_tuples.sort(key=lambda x: (constraints_violations[x], fitness_dict[x]))
    
    # Convert back to dictionaries
    return [dict(x) for x in population_tuples]

def binary_genetic_algorithm(flights, attendants, population_size=30, generations=2, mutation_rate=0.1):
    
    def generate_individual():
        # Use more efficient dictionary comprehension like in standard version
        return {flight: random.choice([a for a in attendants if flight in attendants[a]['flights']]) 
                for flight in flights}
        
    def mutate(individual):
        # Perform a random mutation
        if random.random() < mutation_rate:
            flight_to_mutate = random.choice(flights)
            eligible_attendants = [a for a in attendants if flight_to_mutate in attendants[a]['flights']]
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

        population = [heuristic_improvement(individual, flights, attendants) for individual in next_generation[:population_size]]

    best_solution = max(population, key=lambda x: - sum(attendants[x[flight]]['cost'] for flight in x))
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