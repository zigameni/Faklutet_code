### Explanation

**Genetic Optimization Algorithm Overview:**

Genetic algorithms (GAs) are heuristic search algorithms inspired by the process of natural selection. They are particularly useful for optimization problems where traditional methods may struggle due to complex search spaces or non-linearity.

**Key Concepts:**

1. **Population Initialization:**
   - Start with a population of candidate solutions (individuals). Each individual represents a potential solution to the problem and is typically encoded as a string (binary, integer, or real-valued).

2. **Fitness Evaluation:**
   - Evaluate each individual's fitness or objective function value. This function determines how good each individual is in terms of solving the problem (e.g., maximizing or minimizing an objective).

3. **Selection:**
   - Select individuals from the current population to become parents for the next generation. The probability of selection is usually proportional to an individual's fitness — fitter individuals have a higher chance of being selected.

4. **Crossover:**
   - Perform crossover (recombination) on selected parents to create offspring. This is done to exchange genetic information between parents to potentially produce better offspring solutions.

5. **Mutation:**
   - Apply mutation to offspring with a low probability. Mutation introduces random changes in offspring solutions to maintain genetic diversity and prevent premature convergence to suboptimal solutions.

6. **Termination:**
   - Repeat the selection, crossover, and mutation process for a fixed number of iterations (generations) or until a termination criterion is met (e.g., convergence criteria).

**Finding Minimum and Maximum:**
- **Minimum:** To find the minimum of a function, maximize the negative of the function.
- **Maximum:** Simply maximize the function directly.

### Step-by-Step Implementation

Here's a Python implementation of a genetic algorithm to find both the minimum and maximum of a function. This example uses real-valued encoding for simplicity.

```python
import random
import numpy as np

# Define the objective function (you can replace this with any function you want to optimize)
def objective_function(x):
    return x**2  # Example function: x^2

def genetic_algorithm(population_size, num_generations, crossover_rate, mutation_rate):
    # Initialize population
    population = np.random.uniform(low=-10.0, high=10.0, size=(population_size,))
    
    for generation in range(num_generations):
        # Evaluate fitness
        fitness = [objective_function(x) for x in population]
        
        # Find the best and worst fitness (for monitoring purposes)
        best_fitness = np.min(fitness)
        worst_fitness = np.max(fitness)
        
        # Selection: Roulette wheel selection (fitness proportionate selection)
        probabilities = [(max_fit - fit) / (max_fit - min_fit) for fit in fitness]
        parents = np.random.choice(population, size=population_size, p=probabilities, replace=True)
        
        # Crossover
        offspring = []
        for i in range(0, population_size, 2):
            if random.random() < crossover_rate:
                crossover_point = random.randint(1, len(parents[i])-2)
                offspring1 = np.concatenate((parents[i][:crossover_point], parents[i+1][crossover_point:]))
                offspring2 = np.concatenate((parents[i+1][:crossover_point], parents[i][crossover_point:]))
                offspring.append(offspring1)
                offspring.append(offspring2)
            else:
                offspring.append(parents[i])
                offspring.append(parents[i+1])
        
        # Mutation
        for i in range(len(offspring)):
            if random.random() < mutation_rate:
                mutation_point = random.randint(0, len(offspring[i])-1)
                offspring[i][mutation_point] = np.random.uniform(low=-10.0, high=10.0)
        
        # Replace population with offspring
        population = np.array(offspring)
    
    # Final population evaluation
    final_fitness = [objective_function(x) for x in population]
    best_solution = population[np.argmin(final_fitness)]  # For minimum
    worst_solution = population[np.argmax(final_fitness)]  # For maximum
    
    return best_solution, worst_solution

# Example usage
population_size = 50
num_generations = 100
crossover_rate = 0.8
mutation_rate = 0.03

best_solution, worst_solution = genetic_algorithm(population_size, num_generations, crossover_rate, mutation_rate)

print(f"Minimum solution found: {best_solution} with fitness: {objective_function(best_solution)}")
print(f"Maximum solution found: {worst_solution} with fitness: {objective_function(worst_solution)}")
```

### Template

Use this template to apply the genetic algorithm to different functions:

```python
def genetic_algorithm_template(objective_function, population_size, num_generations, crossover_rate, mutation_rate):
    # Initialize population
    population = initialize_population(population_size)  # Implement based on your encoding

    for generation in range(num_generations):
        # Evaluate fitness
        fitness = [objective_function(individual) for individual in population]
        
        # Selection, crossover, mutation steps (implement as shown in the detailed implementation)
        
        # Termination criteria (based on convergence or number of generations)
    
    # Return best_solution and/or worst_solution based on your objective (minimize or maximize)
    return best_solution, worst_solution
```

This template allows you to plug in different objective functions and adjust parameters as needed for your specific problem.

### Conclusion

The genetic algorithm provides a powerful approach to optimization, suitable for a wide range of problems including finding both the minimum and maximum of functions. By carefully tuning parameters like population size, crossover rate, and mutation rate, you can effectively apply this algorithm to various optimization tasks.