import random
import numpy as np

# Function to calculate the total distance of a route
def calculate_total_distance(route, distance_matrix):
    total_distance = 0
    num_cities = len(route)
    for i in range(num_cities):
        total_distance += distance_matrix[route[i % num_cities], route[(i + 1) % num_cities]]
    return total_distance

# Genetic Algorithm parameters
num_cities = 20  # Number of cities
population_size = 1000
num_generations = 500
crossover_rate = 0.8
mutation_rate = 0.2
tournament_size = 3

# Generate random distance matrix
# distance_matrix = np.random.rand(num_cities, num_cities) * 100

# Static distance matrix for 20 cities (example distances)
distance_matrix = np.array([
    [0, 12, 23, 17, 5, 36, 27, 8, 19, 10, 11, 25, 14, 16, 28, 21, 9, 33, 15, 7],
    [12, 0, 18, 30, 25, 9, 16, 24, 14, 22, 27, 8, 20, 31, 13, 26, 29, 4, 32, 6],
    [23, 18, 0, 35, 16, 14, 29, 26, 32, 21, 7, 34, 15, 25, 19, 31, 10, 3, 28, 22],
    [17, 30, 35, 0, 31, 20, 12, 22, 4, 33, 27, 6, 34, 21, 32, 9, 14, 11, 2, 24],
    [5, 25, 16, 31, 0, 30, 13, 29, 27, 4, 14, 22, 3, 18, 7, 26, 20, 17, 10, 1],
    [36, 9, 14, 20, 30, 0, 19, 33, 21, 34, 3, 28, 12, 35, 32, 1, 15, 23, 5, 24],
    [27, 16, 29, 12, 13, 19, 0, 11, 30, 25, 18, 21, 24, 4, 6, 35, 17, 31, 26, 8],
    [8, 24, 26, 22, 29, 33, 11, 0, 10, 28, 5, 15, 32, 23, 21, 7, 18, 34, 2, 31],
    [19, 14, 32, 4, 27, 21, 30, 10, 0, 36, 9, 20, 25, 11, 35, 3, 33, 8, 1, 15],
    [10, 22, 21, 33, 4, 34, 25, 28, 36, 0, 13, 19, 32, 6, 24, 29, 12, 17, 35, 31],
    [11, 27, 7, 27, 14, 3, 18, 5, 9, 13, 0, 26, 2, 23, 15, 20, 16, 19, 36, 4],
    [25, 8, 34, 6, 22, 28, 21, 15, 20, 19, 26, 0, 10, 31, 12, 23, 18, 35, 33, 16],
    [14, 20, 15, 34, 3, 12, 24, 32, 25, 32, 2, 10, 0, 29, 18, 1, 5, 7, 36, 9],
    [16, 31, 25, 21, 18, 35, 4, 23, 11, 6, 23, 31, 29, 0, 2, 8, 36, 14, 33, 26],
    [28, 13, 19, 32, 7, 32, 6, 21, 35, 24, 15, 12, 18, 2, 0, 9, 30, 11, 1, 17],
    [21, 26, 31, 9, 26, 1, 35, 7, 3, 29, 20, 23, 1, 8, 9, 0, 2, 6, 4, 12],
    [9, 29, 10, 14, 20, 15, 17, 18, 33, 12, 16, 18, 5, 36, 30, 2, 0, 27, 35, 3],
    [33, 4, 3, 11, 17, 23, 31, 34, 8, 17, 19, 35, 7, 14, 11, 6, 27, 0, 36, 9],
    [15, 32, 28, 2, 10, 5, 26, 2, 1, 35, 36, 33, 36, 33, 1, 4, 35, 36, 0, 10],
    [7, 6, 22, 24, 1, 24, 8, 31, 15, 31, 4, 16, 9, 26, 17, 12, 3, 9, 10, 0]
])


np.fill_diagonal(distance_matrix, 0)  # Set diagonal (self-distances) to 0

# Genetic Algorithm main function
def genetic_algorithm(num_generations, population_size, crossover_rate, mutation_rate, tournament_size, distance_matrix):
    # Initialize population
    population = [list(np.random.permutation(num_cities)) for _ in range(population_size)]

    # Main loop
    for generation in range(num_generations):
        # Evaluate fitness of each individual
        fitness_values = [1 / calculate_total_distance(individual, distance_matrix) for individual in population]

        # Selection (tournament selection)
        selected_parents = []
        for _ in range(population_size):
            tournament = random.sample(range(population_size), tournament_size)
            tournament_fitness = [fitness_values[i] for i in tournament]
            winner = tournament[np.argmax(tournament_fitness)]
            selected_parents.append(population[winner])

        # Crossover (ordered crossover)
        offspring_population = []
        for i in range(0, population_size, 2):
            if random.random() < crossover_rate:
                parent1, parent2 = selected_parents[i], selected_parents[i + 1]
                # Perform ordered crossover (OX)
                child1, child2 = ordered_crossover(parent1, parent2)
                offspring_population.append(child1)
                offspring_population.append(child2)
            else:
                offspring_population.append(selected_parents[i])
                offspring_population.append(selected_parents[i + 1])

        # Mutation (swap mutation)
        mutated_population = [swap_mutation(individual, mutation_rate) for individual in offspring_population]

        # Elitism: Select best individuals for the next generation
        combined_population = list(zip(population, fitness_values)) + list(zip(mutated_population, [1 / calculate_total_distance(individual, distance_matrix) for individual in mutated_population]))
        combined_population.sort(key=lambda x: x[1], reverse=True)
        population = [ind for ind, _ in combined_population[:population_size]]

        # Print best individual in the current generation
        best_individual = max(population, key=lambda x: 1 / calculate_total_distance(x, distance_matrix))
        print(f"Generation {generation + 1}: Best distance = {calculate_total_distance(best_individual, distance_matrix)}")

    # Return the best route found
    return max(population, key=lambda x: 1 / calculate_total_distance(x, distance_matrix))

# Ordered crossover (OX)
def ordered_crossover(parent1, parent2):
    size = len(parent1)
    child1, child2 = [-1] * size, [-1] * size

    # Select a subset of parent1's genes to be copied to the child
    start, end = sorted(random.sample(range(size), 2))
    child1[start:end] = parent1[start:end]
    child2[start:end] = parent2[start:end]

    # Fill remaining positions with genes from parent2
    for i in range(size):
        if child1[i] == -1:
            for gene in parent2:
                if gene not in child1:
                    child1[i] = gene
                    break
        if child2[i] == -1:
            for gene in parent1:
                if gene not in child2:
                    child2[i] = gene
                    break

    return child1, child2

# Swap mutation
def swap_mutation(individual, mutation_rate):
    if random.random() < mutation_rate:
        idx1, idx2 = random.sample(range(len(individual)), 2)
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual

# Run the genetic algorithm
best_route = genetic_algorithm(num_generations, population_size, crossover_rate, mutation_rate, tournament_size, distance_matrix)
best_distance = calculate_total_distance(best_route, distance_matrix)
print(f"\nBest route found: {best_route}")
print(f"Best distance found: {best_distance}")
