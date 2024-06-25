import numpy as np
import random
import matplotlib.pyplot as plt

# Optimization functions
def opt_fun_1(x1, x2):
    return np.sin(4 * np.pi * x1) + np.cos(2 * np.pi * x2)

def opt_fun_2(x1, x2):
    return x1 ** 2 + x2 ** 2

MAX_ELEM = 100000

def generate_points(max_elem):
    points = []
    for _ in range(max_elem):
        x1 = random.uniform(0, 1)
        x2 = random.uniform(0, 1)
        points.append((x1, x2))
    return points

def evaluate_points(points, opt_fun_1, opt_fun_2):
    evaluated_points = []
    for x1, x2 in points:
        f1 = opt_fun_1(x1, x2)
        f2 = opt_fun_2(x1, x2)
        evaluated_points.append((f1, f2))
    return evaluated_points

def find_pareto_front(points, maximize_f1, maximize_f2):
    pareto_points = []
    for i, (f1_i, f2_i) in enumerate(points):
        dominated = False
        for j, (f1_j, f2_j) in enumerate(points):
            if (maximize_f1 and f1_j > f1_i) or (not maximize_f1 and f1_j < f1_i):
                if (maximize_f2 and f2_j > f2_i) or (not maximize_f2 and f2_j < f2_i):
                    dominated = True
                    break
        if not dominated:
            pareto_points.append((f1_i, f2_i))
    return pareto_points

if __name__ == '__main__':
    points = generate_points(MAX_ELEM)
    evaluated_points = evaluate_points(points, opt_fun_1, opt_fun_2)

    # All points
    all_f1 = [p[0] for p in evaluated_points]
    all_f2 = [p[1] for p in evaluated_points]

    # Pareto front when maximizing both functions
    pareto_max_max = find_pareto_front(evaluated_points, maximize_f1=True, maximize_f2=True)
    pareto_max_max_f1 = [p[0] for p in pareto_max_max]
    pareto_max_max_f2 = [p[1] for p in pareto_max_max]

    # Pareto front when minimizing f1 and maximizing f2
    pareto_min_max = find_pareto_front(evaluated_points, maximize_f1=False, maximize_f2=True)
    pareto_min_max_f1 = [p[0] for p in pareto_min_max]
    pareto_min_max_f2 = [p[1] for p in pareto_min_max]

    # Plotting
    plt.figure(dpi=320, figsize=[13.35, 7.5])
    plt.grid()
    plt.scatter(all_f1, all_f2, marker='o', s=1, c='blue', label='Randomly generated points')
    plt.scatter(pareto_max_max_f1, pareto_max_max_f2, marker='x', s=5, c='red', label='Pareto front (max f1, max f2)')
    plt.scatter(pareto_min_max_f1, pareto_min_max_f2, marker='x', s=5, c='black', label='Pareto front (min f1, max f2)')
    plt.xlabel('$f_1(x)$')
    plt.ylabel('$f_2(x)$')
    plt.legend()
    plt.show()

    print("Plots generated and displayed.")
