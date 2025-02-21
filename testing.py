'''For each solution run 30 tests and calcualte the average cost, time taken and the standard deviation of the cost and time taken'''

import timeit
import statistics
import json
from matplotlib import pyplot as plt
import numpy as np

from data_loader import load_attendants, load_flights, file_paths

from BGA_improved import binary_genetic_algorithm as BGA_improved
from BGA_standard import binary_genertic_algorithm as BGA_standard
from simulated_annealing import simulated_annealing

global RESULTS
RESULTS = {
    'data/sppnw41.txt' : {
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
    },
    'data/sppnw42.txt' : {
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
    },
    'data/sppnw43.txt' : {
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
}

def run_test(solution, n, reference_name):
    for dataset in RESULTS:
        for _ in range(n):
            attendants = load_attendants(dataset)
            flights = load_flights(dataset)
            flight_list = list(range(1, flights))
            start_time = timeit.default_timer()
            results = solution(flight_list, attendants)
            end_time = timeit.default_timer()
            RESULTS[dataset][reference_name]['costs'].append(results[1])
            RESULTS[dataset][reference_name]['times'].append(end_time - start_time)

def calcualte_averages_and_standard_deviations():
    for dataset in RESULTS:
        for solution in RESULTS[dataset]:
            RESULTS[dataset][solution]['average_cost'] = statistics.mean(RESULTS[dataset][solution]['costs'])
            RESULTS[dataset][solution]['standard_deviation_cost'] = statistics.stdev(RESULTS[dataset][solution]['costs'])
            RESULTS[dataset][solution]['average_time'] = statistics.mean(RESULTS[dataset][solution]['times'])
            RESULTS[dataset][solution]['standard_deviation_time'] = statistics.stdev(RESULTS[dataset][solution]['times'])

def plot_results():
    # For each algorithm plot the average cost and the standard deviation of the cost
    # and the average time and the standard deviation of the time
    algorithms = []
    average_costs = []
    standard_deviations_cost = []
    average_times = []
    standard_deviations_time = []
  
    algorithms = list(RESULTS['data/sppnw41.txt'].keys())
    average_costs = [RESULTS['data/sppnw41.txt'][algorithm]['average_cost'] for algorithm in algorithms]
    standard_deviations_cost = [RESULTS['data/sppnw41.txt'][algorithm]['standard_deviation_cost'] for algorithm in algorithms]
    average_times = [RESULTS['data/sppnw41.txt'][algorithm]['average_time'] for algorithm in algorithms]
    standard_deviations_time = [RESULTS['data/sppnw41.txt'][algorithm]['standard_deviation_time'] for algorithm in algorithms]

    X = file_paths
    X = [name.split('/')[-1] for name in X]

    x = np.arange(len(X))

    plt.bar(x - 0.2, average_costs[0], width=0.2, label='BGA Improved', yerr=standard_deviations_cost[0])
    plt.bar(x, average_costs[1], width=0.2, label='BGA Standard', yerr=standard_deviations_cost[1])
    plt.bar(x + 0.2, average_costs[2], width=0.2, label='Simulated Annealing', yerr=standard_deviations_cost[2])

    plt.xticks(x, X)
    plt.xlabel('Dataset')
    plt.ylabel('Average Cost')
    plt.title('Average Cost of Each Algorithm')
    plt.legend()
    plt.show()

    # Now for the time
    plt.bar(x - 0.2, average_times[0], width=0.2, label='BGA Improved', yerr=standard_deviations_time[0])
    plt.bar(x, average_times[1], width=0.2, label='BGA Standard', yerr=standard_deviations_time[1])
    plt.bar(x + 0.2, average_times[2], width=0.2, label='Simulated Annealing', yerr=standard_deviations_time[2])

    plt.xticks(x, X)
    plt.xlabel('Dataset')
    plt.ylabel('Average Time')
    plt.title('Average Time of Each Algorithm')
    plt.legend()
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