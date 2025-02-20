# Running this script will run all algorithms then compare the results

import BGA_improved
import BGA_standard
import simulated_annealing
import data_loader
import numpy as np
import matplotlib.pyplot as plt 

if __name__ == "__main__":
    # Load the data sets 
    num_data_sets = len(data_loader.file_paths)

    results = []

    # Run the algorithm for each data set and add to results 
    results = {
        'BGA Improved' : [],
        'BGA Standard' : [],
        'Simulated Annealing' : []
    }

    for i in range(num_data_sets):
        # Load the data sets 
        num_flights = data_loader.load_flights(data_loader.file_paths[i])
        flights = list(range(1, num_flights))
        attendants = data_loader.load_attendants(data_loader.file_paths[i])

        # Run the algorithms 
        BGA_improved_results = BGA_improved.binary_genetic_algorithm(flights, attendants)
        BGA_standard_results = BGA_standard.binary_genertic_algorithm(flights, attendants)
        simulated_annealing_results = simulated_annealing.simulated_annealing(flights, attendants)

        results['BGA Improved'].append(BGA_improved_results[1])
        results['BGA Standard'].append(BGA_standard_results[1])
        results['Simulated Annealing'].append(simulated_annealing_results[1])

    # Plot the results

    print(results)

    algorithm = ("BGA Improved", "BGA Standard", "Simulated Annealing")

    data_set_names = data_loader.file_paths

    # the label locations
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
    ax.set_xticks(x + width, algorithm)
    ax.legend(loc='upper left', ncols=3)

    plt.show()  
    

        