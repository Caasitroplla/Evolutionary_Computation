# Simulated Annealing approach to solve the air crew scheduling problems
import data_loader
import math
import random

def generate_initial_schedule(flights, crew):
    # Generate a random schedule for the flights 
    schedule = {}
    for flight in flights:
        eligible_crew = [crew_member for crew_member in crew if flight in crew[crew_member]['flights']]
        schedule[flight] = random.choice(eligible_crew)
    return schedule

def calculate_schedule_cost(schedule, crew):
    return sum(crew[schedule[flight]]['cost'] for flight in schedule if schedule[flight] is not None)

def get_neighbour(schedule, crew):
    # Make a new neighbour by randomly changing an assignment within eligible crew
    neighbour = schedule.copy()
    flight = random.choice(list(schedule.keys()))
    eligible_crew = [crew_member for crew_member in crew if flight in crew[crew_member]['flights']]
    if eligible_crew:
        neighbour[flight] = random.choice(eligible_crew)
    return neighbour

def simulated_annealing(flights, crew, temperature=1000, cooling_rate=0.99, min_temperature=1):
    # Initialize the schedule
    current_schedule = generate_initial_schedule(flights, crew)
    current_cost = calculate_schedule_cost(current_schedule, crew)

    # Setting the best schedule
    best_schedule = current_schedule.copy()
    best_cost = current_cost

    while temperature > min_temperature:
        # Get a neighbour
        neighbour = get_neighbour(current_schedule, crew)
        neighbour_cost = calculate_schedule_cost(neighbour, crew)

        # Accept the neighbour if it's better or with a certain probability
        if neighbour_cost < current_cost or random.random() < math.exp((current_cost - neighbour_cost) / temperature):
            current_schedule = neighbour
            current_cost = neighbour_cost

            # Update the best schedule if the neighbour is better
            if neighbour_cost < best_cost:
                best_schedule = neighbour
                best_cost = neighbour_cost

        # Cool down the temperature
        temperature *= cooling_rate
        # Don't let temperature go below min_temperature
        temperature = max(temperature, min_temperature)

    return best_schedule, best_cost
    

if __name__ == "__main__":
    # Load the data
    num_flights = data_loader.load_flights()
    flights = list(range(1, num_flights))

    attendants = data_loader.load_attendants()

    # Run the simulated annealing algorithm
    best_schedule, best_cost = simulated_annealing(flights, attendants)

    # Print the best schedule and cost
    print(f"Best schedule: {best_schedule}")
    print(f"Best cost: {best_cost}")
    
    