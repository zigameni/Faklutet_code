import numpy as np
import matplotlib.pyplot as plt
import random


FILES = [173669, 275487, 1197613, 1549805, 502334, 217684, 1796841, 274708,
         631252, 148665, 150254, 4784408, 344759, 440109, 4198037, 329673, 28602,
         144173, 1461469, 187895, 369313, 959307, 1482335, 2772513, 1313997, 254845,
         486167, 2667146, 264004, 297223, 94694, 1757457, 576203, 8577828, 498382,
         8478177, 123575, 4062389, 3001419, 196884, 617991, 421056, 3017627, 131936,
         1152730, 2676649, 656678, 4519834, 201919, 56080, 2142553, 326263, 8172117,
         2304253, 4761871, 205387, 6148422, 414559, 2893305, 2158562, 465972, 304078,
         1841018, 1915571]


class Organism:
    def __init__(self, array, optfunction):
        self.array = array
        self.optfunction = optfunction

    def __copy__(self):
        return Organism(self.array.copy(), self.optfunction)


def optimization_function(array):
    global FILES

    F = 2 ** 26
    for i in range(0, len(array)):
        F -= array[i] * FILES[i]
    if F >= 0:
        return F
    else:
        return 2 ** 26


GENERATIONS = 50

POPULATION = 2000

ITERATIONS = 20

NUMBER_OF_BITS = 64

K_FACTOR = 0.25
K_BEST = int(2000 * K_FACTOR)

ONE_POINT_CROSSOVER = int(NUMBER_OF_BITS / 2)


def initialize_population():
    global NUMBER_OF_BITS
    population = []
    for i in range(0, POPULATION):
        K = random.randint(5, 45)
        arr = np.zeros(NUMBER_OF_BITS)
        arr[:int(K)] = 1
        np.random.shuffle(arr)
        arr = arr.tolist()

        opt_fun = optimization_function(arr)
        population.append(Organism(arr, opt_fun))
    return population


def genetic_algorithm():
    population = initialize_population()

    cummulative_minimum = []
    cummulative_minimum_maybe = []

    current_generation = 0
    current_minimum = 2 ** 26 + 1
    current_min = Organism([], 2 ** 26 + 1)

    while True:
        current_generation += 1

        for pp in population:
            if pp.optfunction < current_min.optfunction:
                current_min = pp.__copy__()
            cummulative_minimum_maybe.append(current_min)
        population = sorted(population, key=lambda x: x.optfunction)

        if current_minimum > population[0].optfunction:
            current_minimum = population[0].optfunction

        cummulative_minimum.append(current_minimum)

        if current_generation >= GENERATIONS or 32 >= population[0].optfunction >= 0:
            while len(cummulative_minimum) != GENERATIONS:
                cummulative_minimum.append(cummulative_minimum[len(cummulative_minimum) - 1])
            return population[0], cummulative_minimum, cummulative_minimum_maybe
        current_elite = population[0:K_BEST]
        elite_parents = current_elite.copy()

        while len(current_elite) <= POPULATION:
            parent_one = int(random.randint(0, len(elite_parents) - 1))
            parent_two = int(random.randint(0, len(elite_parents) - 1))

            while parent_two == parent_one:
                parent_one = int(random.randint(0, len(elite_parents) - 1))
                parent_two = int(random.randint(0, len(elite_parents) - 1))

            parent_one = elite_parents[parent_one]
            parent_two = elite_parents[parent_two]

            if random.random() < 0.8:
                ONE_POINT_CROSSOVER = random.randint(1, 62)
                offspring_one = parent_two.array[0: ONE_POINT_CROSSOVER] + parent_one.array[ONE_POINT_CROSSOVER:]
                offspring_two = parent_one.array[0: ONE_POINT_CROSSOVER] + parent_two.array[ONE_POINT_CROSSOVER:]

                current_elite.append(Organism(offspring_one, optimization_function(offspring_one)))
                current_elite.append(Organism(offspring_two, optimization_function(offspring_two)))

        while len(current_elite) > POPULATION:
            current_elite.pop()

        for elite_object in current_elite:
            mutation_probability = random.random()
            if mutation_probability < 0.1:
                systemRandom = random.SystemRandom()
                random_mutation_index = systemRandom.randint(0, 63)

                if elite_object.array[random_mutation_index] == 0:
                    elite_object.array[random_mutation_index] = 1
                else:
                    elite_object.array[random_mutation_index] = 0

                elite_object.optfunction = optimization_function(elite_object.array)

        population = current_elite.copy()
        current_elite.clear()


if __name__ == '__main__':
    tuple_data = []
    organisms = []
    the_force = []

    iterations_array = []

    for i in range(0, ITERATIONS):
        minimums = []
        best, cummulative_minimum, disturbance_in_the_force = genetic_algorithm()

        print("======== " + str(i + 1) + " ========")
        print("Best: " + str(best.optfunction))
        print("Array: " + str(best.array))
        print("====================")
        tuple_data.append(cummulative_minimum)
        organisms.append(best)

        while len(disturbance_in_the_force) < (50 * 2000):
            disturbance_in_the_force.append(disturbance_in_the_force[len(disturbance_in_the_force) - 1])

        for j in disturbance_in_the_force:
            minimums.append(
                j.optfunction
            )
        iterations_array.append(minimums)

    iterations = np.arange(1, 50 * 2000 + 1)

    plt.figure(1, dpi=320, figsize=[14.47, 14.47])
    plt.grid(color='lightgray', linestyle='-', linewidth=1)
    plt.axhline(32, linestyle='--', color='lightgreen')
    plt.xscale("log")
    plt.yscale("log")
    for i in range(0, len(iterations_array)):
        plt.plot(iterations, iterations_array[i])
    plt.show()
    fig1 = plt.gcf()
    plt.draw()
    fig1.savefig("kumulativni.png")

    average_value_array = []
    for i in range(0, 2000 * 50):
        average = 0
        for j in iterations_array:
            average += j[i]

        average /= GENERATIONS
        average_value_array.append(average)

    plt.figure(1, dpi=320, figsize=[14.47, 14.47])
    plt.grid(color='lightgray', linestyle='-', linewidth=1)
    plt.axhline(32, linestyle='--', color='lightgreen')
    plt.xscale("log")
    plt.yscale("log")
    plt.plot(iterations, average_value_array)
    plt.show()
    fig2 = plt.gcf()
    plt.draw()
    fig2.savefig("srednji.png")

    min = 2 ** 24 + 1
    index = 0
    for i in range(0, len(tuple_data)):
        if (organisms[i].optfunction < min):
            min = organisms[i].optfunction
            index = i + 1

    print("======== " + str(index) + " ========")
    print("Best: " + str(min))
    print("Array: " + str(organisms[index - 1].array))
    print("====================")
