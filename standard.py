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
