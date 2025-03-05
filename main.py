# Running this script will run all algorithms then compare the results

import BGA_improved
import BGA_standard
import simulated_annealing
import data_loader
import numpy as np
import matplotlib.pyplot as plt
import timeit
import logging


if __name__ == "__main__":
    logging.basicConfig(
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%H:%M:%S",
        level=logging.INFO,
        filename="app.log",
        encoding="utf-8",
        filemode="w"
    )

    # Load the data sets
    num_data_sets = len(data_loader.file_paths)

    results = []

    # Run the algorithm for each data set and add to results
    results = {
        'BGA Improved' : [],
        'BGA Standard' : [],
        'Simulated Annealing' : []
    }

    timings = {
        'BGA Improved' : [],
        'BGA Standard' : [],
        'Simulated Annealing' : []
    }

    # For simulated annealing and BGA to be doing the same ammounr of runs:
    SA_RUNS = 10000
    BGA_POPULATION_SIZE = 10
    BGA_GENERATIONS = 990

    for i in range(num_data_sets):
        # Load the data sets
        num_flights = data_loader.load_flights(data_loader.file_paths[i])
        flights = list(range(1, num_flights))
        attendants = data_loader.load_attendants(data_loader.file_paths[i])

        # Run the algorithms
        logging.info(f"Running BGA Improved for {data_loader.file_paths[i]}")
        start_time = timeit.default_timer()
        BGA_improved_results = BGA_improved.binary_genetic_algorithm(flights, attendants, BGA_POPULATION_SIZE, BGA_GENERATIONS)
        end_time = timeit.default_timer()
        timings['BGA Improved'].append(end_time - start_time)

        logging.info(f"Running BGA Standard for {data_loader.file_paths[i]}")
        start_time = timeit.default_timer()
        BGA_standard_results = BGA_standard.binary_genertic_algorithm(flights, attendants, BGA_POPULATION_SIZE, BGA_GENERATIONS)
        end_time = timeit.default_timer()
        timings['BGA Standard'].append(end_time - start_time)

        logging.info(f"Running Simulated Annealing for {data_loader.file_paths[i]}")
        start_time = timeit.default_timer()
        simulated_annealing_results = simulated_annealing.simulated_annealing(flights, attendants, temperature=SA_RUNS)
        end_time = timeit.default_timer()
        timings['Simulated Annealing'].append(end_time - start_time)

        results['BGA Improved'].append(BGA_improved_results[1])
        results['BGA Standard'].append(BGA_standard_results[1])
        results['Simulated Annealing'].append(simulated_annealing_results[1])


    # Plot the cost of each algorithms results

    algorithm = ("BGA Improved", "BGA Standard", "Simulated Annealing")

    data_set_names = data_loader.file_paths
    data_set_names = [name.split('/')[-1] for name in data_set_names]

    # the label locations
    logging.info(f"Plotting the cost of each algorithms results")

    x = np.arange(len(data_set_names))
    width = 0.25
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurements in results.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurements, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    ax.set_ylabel('Cost')
    ax.set_title('Cost of each algorithm')
    ax.set_xticks(x + width, data_set_names)
    ax.legend(loc='upper left', ncols=3)

    plt.show()

    # Plot the time taken for each algorithm

    logging.info(f"Plotting the time taken for each algorithm")

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurements in timings.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurements, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    ax.set_ylabel('Time')
    ax.set_title('Time taken for each algorithm')
    ax.set_xticks(x + width, data_set_names)
    ax.legend(loc='upper left', ncols=3)

    plt.show()

