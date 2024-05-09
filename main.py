import random
import math
from copy import deepcopy
import time
import matplotlib.pyplot as plt
import numpy as np

import requirements
from sklearn.metrics import r2_score


def plot_and_save_bin_packing_waste(testN, wastes, algorithm_name):
    """
    Plots and saves the best-fit lines for the waste produced by a bin-packing algorithm.
    
    Args:
        testN (list or np.ndarray): List of input sizes.
        wastes (np.ndarray): 2D array where each column contains multiple waste data points for each input size.
        algorithm_name (str): The name of the bin-packing algorithm.
    """
    plt.figure(figsize=(10, 7))
    x_log = np.log(testN)

    # Calculate the mean waste across tests for each input size
    mean_waste = np.mean(wastes, axis=1)
    y_log = np.log(mean_waste)

    # Fit a line to the log-transformed data
    slope, intercept = np.polyfit(x_log, y_log, 1)
    best_fit_y_log = slope * x_log + intercept  # Logarithm of predicted values
    best_fit_y = np.exp(best_fit_y_log)  # Convert back to the original scale

    # Plot the actual mean waste data points
    plt.loglog(testN, mean_waste, 'o', color='b', label=f"{algorithm_name} Actual Mean")

    # Plot the best-fit line as a dashed line
    plt.loglog(testN, best_fit_y, '--', color='r', label=f"{algorithm_name} Best Fit")

    # Calculate R^2 for the fit
    r2 = r2_score(y_log, best_fit_y_log)

    # Create equation and metrics string
    metrics_str = f"y = {np.exp(intercept):.2e}x^({slope:.2f}), R² = {r2:.4f}"

    # Place text on the plot
    plt.text(
        0.05,  # Adjust horizontal position to be slightly away from the y-axis
        1.11,  # Adjust y position for better visibility
        metrics_str,
        transform=plt.gca().transAxes,
        color='b'
    )

    plt.xlabel("Number of Items (n)")
    plt.ylabel("Waste")
    plt.title(f"Mean Waste and Best-fit Line for {algorithm_name} on Log-Log Scale")
    plt.legend()

    # Save the plot with a unique name based on the algorithm
    plt.savefig(f"{algorithm_name}_Mean_Waste_Performance.png")
    plt.close()  # Close the plot to free up memory and prevent unwanted inline display

def plot_and_save_all_bin_packing_waste(testN, wastes_dict):
    """
    Plots and saves the average waste produced by multiple bin-packing algorithms on the same graph.

    Args:
        testN (list or np.ndarray): List of input sizes.
        wastes_dict (dict): Dictionary where the key is the algorithm name and the value is a 2D array
                            containing waste data for each input size.
    """
    plt.figure(figsize=(10, 7))

    # Iterate through each algorithm and plot their mean waste
    for algorithm_name, wastes in wastes_dict.items():
        # Calculate the mean waste across tests for each input size
        mean_waste = np.mean(wastes, axis=1)

        # Plot the actual mean waste data points
        plt.loglog(testN, mean_waste, 'o', label=f"{algorithm_name} Mean Waste", ls = '-')

    plt.xlabel("Number of Items (n)")
    plt.ylabel("Waste")
    if len(wastes_dict) > 2:
        plt.title("Mean Waste for Various Bin-Packing Algorithms on Log-Log Scale")
    else:
        plt.title("Mean Waste for FFD and BFD on Log-Log Scale")
    plt.legend()

    # Save the plot with a generic name
    if len(wastes_dict) > 2:
        plt.savefig("All_Algorithms_Mean_Waste_Performance.png")
    else:
        plt.savefig("FFD_BFD_Mean_Waste_Performance.png")
    plt.close()  # Close the plot to free up memory and prevent unwanted inline display
    
def generate_test_data(num_items: int, roundNum: int):
    data = []
    for i in range(num_items):
        data.append(round(random.uniform(0.1, 1.0), roundNum))
    return data

def calculate_waste(packing_function, items, bin_size=1.0):
    # Initialize assignment and free_space lists
    assignment = [0] * len(items)  # Initially, no items are assigned to bins
    free_space = []

    # Call the packing function with these lists
    packing_function(items, assignment, free_space)

    # The number of bins is equal to the number of entries in `free_space`
    num_bins = len(free_space)

    # Calculate the total size of the items
    total_size = sum(items)

    # Calculate waste as (number of bins) - (total size of all items)
    waste = num_bins - total_size
    return waste

def main():
    packing_algorithms = [
        ("Next Fit", requirements.next_fit),
        ("First Fit", requirements.first_fit),
        ("Best Fit", requirements.best_fit),
        ("First Fit Decreasing", requirements.first_fit_decreasing),
        ("Best Fit Decreasing", requirements.best_fit_decreasing)
    ]

    num_algorithms = len(packing_algorithms)  # Number of algorithms being tested
    num_tests_per_algorithm = 20  # Number of lists to generate per algorithm
    list_sizes = [500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000]  # Example input sizes to test
    random_seed = 42  # Seed for reproducibility
    np.random.seed(random_seed)
    wastes = np.zeros((len(list_sizes), num_algorithms, num_tests_per_algorithm))
    wastes_dict = {name: np.zeros((len(list_sizes), num_tests_per_algorithm)) for name, _ in packing_algorithms}

    for i, n in enumerate(list_sizes):
        for j in range(num_tests_per_algorithm):
            
            # Loop through each packing algorithm to calculate waste
            for k, (algorithm_name, algorithm_function) in enumerate(packing_algorithms):
                # Generate a random list of items between 0.0 and 1.0
                items = np.random.uniform(0.0, 1.0, n)
                # Dynamically print which function is being tested
                print(f"Testing {algorithm_name} with input size {n} (Test {j + 1}/{num_tests_per_algorithm})")

                # Initialize empty assignment and free_space lists
                assignment = [0] * len(items)
                free_space = []

                # Calculate waste using the specified algorithm
                algorithm_function(items, assignment, free_space)
                waste = len(free_space) - sum(items)
                wastes[i, k, j] = waste  # Store the waste value
                wastes_dict[algorithm_name][i, j] = waste

    # Plot and save the best-fit lines for each algorithm
    for k, (algorithm_name, _) in enumerate(packing_algorithms):
        plot_and_save_bin_packing_waste(list_sizes, wastes[:, k, :], algorithm_name)
    plot_and_save_all_bin_packing_waste(list_sizes, wastes_dict)
    
    filtered_wastes_dict = {
        "First Fit Decreasing": wastes_dict["First Fit Decreasing"],
        "Best Fit Decreasing": wastes_dict["Best Fit Decreasing"]
    }
    plot_and_save_all_bin_packing_waste(list_sizes, filtered_wastes_dict)

if __name__ == "__main__":
    main()
