# Simulated Annealing approach to solve the air crew scheduling problems
import data_loader
import math
import random

data = data_loader.load_data(data_loader.file_paths[0])

# We want to minimise the cost of the solution or the total column cost
# We need to forfill 1 through to 17 crew members

def generate_initial_solution(data):
    # Initialize empty solution
    solution = []
    crew_coverage = [0] * 17  # Track coverage for crew positions 1-17
    
    # Randomly select columns (flight combinations) until all crew positions are covered
    available_columns = list(range(len(data)))
    
    while any(coverage < 1 for coverage in crew_coverage):
        if not available_columns:
            break  # Break if we run out of columns to choose from
            
        # Randomly select a column
        col_idx = random.choice(available_columns)
        available_columns.remove(col_idx)
        
        # Check if this column helps cover any uncovered positions
        column = data[col_idx]
        adds_coverage = False
        
        for pos in range(17):
            if column[pos] == 1 and crew_coverage[pos] < 1:
                adds_coverage = True
                crew_coverage[pos] += 1
        
        # Add column to solution if it helps coverage
        if adds_coverage:
            solution.append(col_idx)
    
    return solution

def simulated_annealing(data):
    # Initialize the solution
    solution = []
    # Initialize the temperature
    temperature = 1000
    # Initialize the cooling rate
    cooling_rate = 0.99
    # Initialize the number of iterations
    num_iterations = 1000
    # Initialize the best solution
    best_solution = None
    # Initialize the best cost
    best_cost = float('inf')
    
    # Generate an initial solution
    for _ in range(num_iterations):
        # Generate a new solution
        new_solution = generate_new_solution(solution)
        # Calculate the cost of the new solution
        new_cost = calculate_cost(new_solution)
        




if __name__ == "__main__":
    solution, cost = simulated_annealing(data)
    print(solution)
    print(cost)
