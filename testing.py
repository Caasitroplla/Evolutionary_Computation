'''For each solution run 30 tests and calcualte the average cost, time taken and the standard deviation of the cost and time taken'''

import timeit
import statistics
import json
from matplotlib import pyplot as plt

from data_loader import get_random_dataset

from BGA_improved import binary_genetic_algorithm as BGA_improved
from BGA_standard import binary_genertic_algorithm as BGA_standard
from simulated_annealing import simulated_annealing

global RESULTS
RESULTS = {
    'BGA_improved': {
        'costs': [],
        'times': []
    },
    'BGA_standard': {
        'costs': [],
        'times': []
    },
    'simulated_annealing': {
        'costs': [],
        'times': []
    }
}

def run_test(solution, n, reference_name):
    for _ in range(n):
        attendants, flights = get_random_dataset()
        flight_list = list(range(1, flights))
        start_time = timeit.default_timer()
        results = solution(flight_list, attendants)
        end_time = timeit.default_timer()
        RESULTS[reference_name]['costs'].append(results[1])
        RESULTS[reference_name]['times'].append(end_time - start_time)

def calcualte_averages_and_standard_deviations():
    for solution in RESULTS:
        RESULTS[solution]['average_cost'] = statistics.mean(RESULTS[solution]['costs'])
        RESULTS[solution]['standard_deviation_cost'] = statistics.stdev(RESULTS[solution]['costs'])
        RESULTS[solution]['average_time'] = statistics.mean(RESULTS[solution]['times'])
        RESULTS[solution]['standard_deviation_time'] = statistics.stdev(RESULTS[solution]['times'])

def plot_results():
    # For each algorithm plot the average cost and the standard deviation of the cost
    # and the average time and the standard deviation of the time

    algorithms = list(RESULTS.keys())
    average_costs = [RESULTS[algorithm]['average_cost'] for algorithm in algorithms]
    standard_deviations_cost = [RESULTS[algorithm]['standard_deviation_cost'] for algorithm in algorithms]
    average_times = [RESULTS[algorithm]['average_time'] for algorithm in algorithms]
    standard_deviations_time = [RESULTS[algorithm]['standard_deviation_time'] for algorithm in algorithms]

    # Plot the averages and standard deviations of the costs
    plt.figure(figsize=(10, 5))
    plt.bar(algorithms, average_costs, yerr=standard_deviations_cost, capsize=5)
    plt.title('Average Cost and Standard Deviation of Cost')
    plt.xlabel('Algorithm')
    plt.ylabel('Cost')
    plt.show()

    # Plot the averages and standard deviations of the times
    plt.figure(figsize=(10, 5))
    plt.bar(algorithms, average_times, yerr=standard_deviations_time, capsize=5)
    plt.title('Average Time and Standard Deviation of Time')
    plt.xlabel('Algorithm')
    plt.ylabel('Time')
    plt.show()

def save_results():
    with open('results.json', 'w') as f:
        json.dump(RESULTS, f)


def main():
    tests = 30
    run_test(BGA_improved, tests, 'BGA_improved')
    run_test(BGA_standard, tests, 'BGA_standard')
    run_test(simulated_annealing, tests, 'simulated_annealing')

    calcualte_averages_and_standard_deviations()

    plot_results()

    save_results()


if __name__ == '__main__':
    main()