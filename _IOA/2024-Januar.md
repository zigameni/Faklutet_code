# ИСПИТ ИЗ ИНЖЕЊЕРСКИХ ОПТИМИЗАЦИОНИХ АЛГОРИТАМА

**24. јануар 2024.**

## Напомене

- Испит траје 180 минута.
- Писати искључиво хемијском оловком.
- Дозвољена је употреба овога листа папира, литературе и рачунара.

Коначне одговоре уписати у одговарајуће кућице, уцртати у дијаграме или заокружити понуђене одговоре. Кодове програма коришћених за решавање питања архивирати преко сајта предмета. Решења питања признају се само уколико садрже извођење, образложење или уколико постоји архивиран одговарајући код. Попунити податке о кандидату у следећој таблици. Сваки задатак носи до 20 поена.

| ПОДАЦИ О КАНДИДАТУ | ЗАДАТАК | Укупно |
| ------------------ | ------- | ------ |
| Индекс (година/број) | Презиме и име | 1. | 2. | / | |
| ПРЕДИСПИТНЕ ОБАВЕЗЕ | ОЦЕНА | | |

---

## 1. Систем за архивирање података има један централни сервер и \( N = 3 \) локалних сервера. На централном серверу чувају се сви подаци, док локални сервери имају ограничени меморијски капацитет од по 64 GB. Постоје 32 различита дигитална податка чије су величине у GB редом записане у следећем низу:

`M = (21, 4, 3, 9, 1, 12, 11, 17, 12, 9, 5, 2, 5, 45, 4, 25, 14, 20, 11, 5, 8, 22, 4, 31, 7, 6, 9, 5, 9, 12, 3, 1)`

Постоји \( K = 7 \) крајњих корисника који су сви повезани са централним сервером и појединим локалним серверима. Подаци о повезаности са серверима, као и времена појединачних приступа одговарајућем серверу дата су у табели I (централни сервер је означен са 0, а локални сервери својим бројем). На пример, корисник K4 повезан је са централним сервером (време приступа 226 ms) и са локалним сервером 2 (време приступа 86 ms).

Крајњи корисници имају 16 захтева за приступом подацима и истим подацима се приступа више пута. Подаци о захтевима дати су у табели II.

Потребно је минимизирати укупно време које је свим корисницима потребно да приступе свим захтеваним подацима. Оптимизациона функција рачуна се као \( f(x) = \sum_{r=1}^{16} p_r t_r(x) \), где је r редни број захтева, \( p_r \) број приступа за захтев r и \( t_r \) је време потребно да се приступи захтеваном дигиталном податку. Конкретно, \( t_r = \min(t_{r0}, t_{r1}, t_{r2}, t_{r3}) \) где је \( t_{rs} \) време потребно да се приступи подацима из захтева r на серверу s ( \( s = 0, 1, 2, 3 \) ) под условом да је одговарајући податак на серверу s и да је корисник повезан са тим сервером.

### Табела I. Повезаност крајњих корисника са серверима и одговарајућа времена приступа.

| Корисници | K1 | K2 | K3 | K4 | K5 | K6 | K7 |
| --------- | -- | -- | -- | -- | -- | -- | -- |
| Сервери | 0 (1012 ms) | 0 (467 ms) | 0 (321 ms) | 0 (226 ms) | 0 (361 ms) | 0 (522 ms) | 0 (1415 ms) |
| | 1 (170 ms) | 1 (28 ms) | 2 (70 ms) | 2 (86 ms) | 1 (26 ms) | 3 (155 ms) | 3 (163 ms) |

### Табела II. Захтеви корисника за подацима.

| Редни број захтева | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
| ------------------ | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| Корисник | 1 | 2 | 5 | 7 | 4 | 3 | 7 | 1 | 6 | 4 | 1 | 5 | 1 | 6 | 2 | 7 |
| Подакак | 9 | 15 | 5 | 12 | 19 | 8 | 1 | 6 | 3 | 8 | 7 | 17 | 23 | 32 | 9 | 11 |
| Број приступа | 850 | 358 | 767 | 693 | 799 | 247 | 552 | 211 | 537 | 589 | 400 | 314 | 409 | 70 | 709 | 301 |

### Задаци:

#### (а) 
Уколико на локалним серверима нема података, израчунати оптимизациону функцију.

#### (б) 
Сматрајући да локални сервери немају ограничење капацитета, одредити минимално копирање са централног сервера на локалне сервере, тако да оптимизациона функција буде минимална. Записати решење тако да сваки ред текстуалног фајла одговара једном локалном серверу: први број у реду је број локалног сервера, а затим следе бројеви података који су копирани на тај локални сервер. Записати и добијену вредност оптимизационе функције.

#### (в) 
Одредити распоред података на локалним серверима уз ограничење капацитета, тако да оптимизациона функција буде минимална. Записати решење тако да сваки ред текстуалног фајла одговара једном локалном серверу: први број у реду је број локалног сервера, а затим следе бројеви података који су копирани на тај локални сервер. Записати и добијену вредност оптимизационе функције.

#### (г) 
Навести оптимизациони алгоритам који је коришћен за решавање претходне тачке, као и његове параметре.

---

## 2. 

Дато је \( N = 12 \) слика правоугаоног облика чије су димензије у cm записане у табели I. Одредити правоугаоник минималне површине у који се могу поставити, без преклапања, све задате слике. Сматрати да је ширина слика паралелна x -оси, а висина y -оси Декартовог координатног система. Ротирање слика није дозвољено. Формални запис решења проблема је \( x = (x_1, y_1, x_2, y_2, ..., x_N, y_N) \) где су \( x_k \) и \( y_k \) одговарајуће координате левог доњег темена k -те слике (правоугаоника), \( k = 1, 2, ..., N \).

### Табела I. Димензије слика.

| Ширина (w) | 1 | 2 | 4 | 5 | 5 | 6 | 7 | 9 | 9 | 10 | 12 | 12 |
| ----------- | - | - | - | - | - | - | - | - | - | -- | -- | -- |
| Висина (h) | 4 | 5 | 6 | 2 | 6 | 4 | 5 | 7 | 4 |  3 |  4 |  6 |

### Задаци:

#### (а) 
Нацртати слике у координатном систему без обзира на међусобне позиције. 

#### (б) 
Израчунати површину правоугаоника у којем могу да се распореде све слике користећи било коју хеуристичку методу.

#### (в) 
Реализовати неки оптимизациони алгоритам за решавање овога проблема. Навести назив алгоритма, његове параметре и добијено решење.

---

## Прилог:

- **М.** - Моделирање оптимизационих проблема
- **Р.** - Решавање оптимизационих проблема

---

This conversion includes all tables, formulas, and instructions as presented in the original PDF. If you need any further adjustments or have any specific formatting preferences, please let me know!




## RESENJE

### **Step-by-Step Implementation Using Genetic Algorithm**

We will implement a genetic algorithm to optimize the server data allocation to minimize the total access time for the users. The steps are as follows:

1. **Define the problem and constraints**:
   - Data sizes and server capacities.
   - User-server connectivity and access times.
   - User access requests and frequencies.

2. **Initialize the population**:
   - Generate random solutions where each solution represents a possible allocation of data to servers.

3. **Evaluate fitness**:
   - Calculate the total access time for each solution.

4. **Selection**:
   - Select the best solutions to be parents for the next generation.

5. **Crossover**:
   - Combine parents to create new solutions (offspring).

6. **Mutation**:
   - Introduce random changes to some solutions to maintain diversity.

7. **Replacement**:
   - Form the new population from the best solutions.

8. **Termination**:
   - Repeat the process for a given number of generations or until convergence.

### **Python Implementation**

Let's implement this step-by-step in Python.

#### **Step 1: Define the Problem and Constraints**

```python
# Define data sizes in GB
M = [21, 4, 3, 9, 1, 12, 11, 17, 12, 9, 5, 2, 5, 45, 4, 25, 14, 20, 11, 5, 8, 22, 4, 31, 7, 6, 9, 5, 9, 12, 3, 1]
N = 3  # Number of local servers
K = 7  # Number of users
local_server_capacity = 64  # Capacity of each local server in GB

# User-server connectivity and access times (in ms)
user_server_times = [
    [1012, 170, float('inf'), float('inf')],
    [467, 28, float('inf'), float('inf')],
    [321, float('inf'), 70, float('inf')],
    [226, float('inf'), 86, float('inf')],
    [361, 26, float('inf'), float('inf')],
    [522, float('inf'), float('inf'), 155],
    [1415, float('inf'), float('inf'), 163]
]

# User requests (user, data, access frequency)
requests = [
    (1, 9, 850), (2, 15, 358), (5, 5, 767), (7, 12, 693),
    (4, 19, 799), (3, 8, 247), (7, 1, 552), (1, 6, 211),
    (6, 3, 537), (4, 8, 589), (1, 7, 400), (5, 17, 314),
    (1, 23, 409), (6, 32, 70), (2, 9, 709), (7, 11, 301)
]
```

#### **Step 2: Initialize the Population**

```python
import random

def initialize_population(pop_size, data_count, server_count):
    population = []
    for _ in range(pop_size):
        individual = [random.randint(0, server_count) for _ in range(data_count)]
        population.append(individual)
    return population
```

#### **Step 3: Evaluate Fitness**

```python
def evaluate_fitness(individual, M, requests, user_server_times):
    total_time = 0
    for req in requests:
        user, data_idx, access_count = req
        server_times = [user_server_times[user-1][s] if individual[data_idx] == s else float('inf') for s in range(len(user_server_times[0]))]
        min_time = min(server_times)
        total_time += access_count * min_time
    return total_time
```

#### **Step 4: Selection**

```python
def select_parents(population, fitness, num_parents):
    selected_parents = sorted(zip(population, fitness), key=lambda x: x[1])[:num_parents]
    return [parent for parent, fit in selected_parents]
```

#### **Step 5: Crossover**

```python
def crossover(parent1, parent2, crossover_rate):
    if random.random() < crossover_rate:
        point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    return parent1, parent2
```

#### **Step 6: Mutation**

```python
def mutate(individual, mutation_rate, server_count):
    if random.random() < mutation_rate:
        idx = random.randint(0, len(individual) - 1)
        individual[idx] = random.randint(0, server_count)
    return individual
```

#### **Step 7: Replacement**

```python
def replacement(population, new_population, fitness, new_fitness):
    combined = sorted(zip(population + new_population, fitness + new_fitness), key=lambda x: x[1])
    new_population = [individual for individual, fit in combined[:len(population)]]
    new_fitness = [fit for individual, fit in combined[:len(population)]]
    return new_population, new_fitness
```

#### **Step 8: Termination**

```python
def genetic_algorithm(M, requests, user_server_times, pop_size, generations, crossover_rate, mutation_rate, num_parents):
    population = initialize_population(pop_size, len(M), len(user_server_times[0])-1)
    fitness = [evaluate_fitness(ind, M, requests, user_server_times) for ind in population]
    
    for generation in range(generations):
        parents = select_parents(population, fitness, num_parents)
        new_population = []
        
        for i in range(0, len(parents), 2):
            parent1 = parents[i]
            parent2 = parents[(i + 1) % len(parents)]
            child1, child2 = crossover(parent1, parent2, crossover_rate)
            new_population.append(mutate(child1, mutation_rate, len(user_server_times[0])-1))
            new_population.append(mutate(child2, mutation_rate, len(user_server_times[0])-1))
        
        new_fitness = [evaluate_fitness(ind, M, requests, user_server_times) for ind in new_population]
        population, fitness = replacement(population, new_population, fitness, new_fitness)
        
        best_fitness = min(fitness)
        best_solution = population[fitness.index(best_fitness)]
        print(f"Generation {generation}: Best Fitness = {best_fitness}")
    
    return best_solution, best_fitness

# Example usage
best_solution, best_fitness = genetic_algorithm(
    M, requests, user_server_times,
    pop_size=50, generations=100, crossover_rate=0.7, mutation_rate=0.1, num_parents=20
)

print(f"Best solution: {best_solution}, Fitness: {best_fitness}")
```

This implementation provides a basic genetic algorithm template for optimizing the allocation of data to servers. You can adjust the parameters such as population size, number of generations, crossover rate, and mutation rate based on your specific requirements and computational resources.



### **Solution for Tasks (б), (в), and (г)**

#### **Task (б): Minimal Copying Without Capacity Constraints**

To solve this task, we need to determine the minimal copying of data from the central server to the local servers such that the optimization function is minimized. Here, we assume that local servers have no capacity constraints.

#### **Step-by-Step Implementation**

1. **Define the Problem and Constraints**:
   - Data sizes and server capacities.
   - User-server connectivity and access times.
   - User access requests and frequencies.

2. **Initialize the Population**:
   - Generate random solutions where each solution represents a possible allocation of data to servers.

3. **Evaluate Fitness**:
   - Calculate the total access time for each solution.

4. **Selection**:
   - Select the best solutions to be parents for the next generation.

5. **Crossover**:
   - Combine parents to create new solutions (offspring).

6. **Mutation**:
   - Introduce random changes to some solutions to maintain diversity.

7. **Replacement**:
   - Form the new population from the best solutions.

8. **Termination**:
   - Repeat the process for a given number of generations or until convergence.

#### **Python Implementation**

```python
import random
import numpy as np

# Define data sizes in GB
M = [21, 4, 3, 9, 1, 12, 11, 17, 12, 9, 5, 2, 5, 45, 4, 25, 14, 20, 11, 5, 8, 22, 4, 31, 7, 6, 9, 5, 9, 12, 3, 1]
N = 3  # Number of local servers
K = 7  # Number of users
local_server_capacity = 64  # Capacity of each local server in GB

# User-server connectivity and access times (in ms)
user_server_times = [
    [1012, 170, float('inf'), float('inf')],
    [467, 28, float('inf'), float('inf')],
    [321, float('inf'), 70, float('inf')],
    [226, float('inf'), 86, float('inf')],
    [361, 26, float('inf'), float('inf')],
    [522, float('inf'), float('inf'), 155],
    [1415, float('inf'), float('inf'), 163]
]

# User requests (user, data, access frequency)
requests = [
    (1, 9, 850), (2, 15, 358), (5, 5, 767), (7, 12, 693),
    (4, 19, 799), (3, 8, 247), (7, 1, 552), (1, 6, 211),
    (6, 3, 537), (4, 8, 589), (1, 7, 400), (5, 17, 314),
    (1, 23, 409), (6, 32, 70), (2, 9, 709), (7, 11, 301)
]

# Initialize the population
def initialize_population(pop_size, data_count, server_count):
    population = []
    for _ in range(pop_size):
        individual = [random.randint(0, server_count) for _ in range(data_count)]
        population.append(individual)
    return population

# Evaluate fitness
def evaluate_fitness(individual, M, requests, user_server_times):
    total_time = 0
    for req in requests:
        user, data_idx, access_count = req
        server_times = [user_server_times[user-1][s] if individual[data_idx] == s else float('inf') for s in range(len(user_server_times[0]))]
        min_time = min(server_times)
        total_time += access_count * min_time
    return total_time

# Select parents using tournament selection
def select_parents(population, fitness, num_parents):
    selected_parents = sorted(zip(population, fitness), key=lambda x: x[1])[:num_parents]
    return [parent for parent, fit in selected_parents]

# Apply crossover (single point)
def crossover(parent1, parent2, crossover_rate):
    if random.random() < crossover_rate:
        point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    return parent1, parent2

# Apply mutation (uniform)
def mutate(individual, mutation_rate, server_count):
    if random.random() < mutation_rate:
        idx = random.randint(0, len(individual) - 1)
        individual[idx] = random.randint(0, server_count)
    return individual

# Replacement
def replacement(population, new_population, fitness, new_fitness):
    combined = sorted(zip(population + new_population, fitness + new_fitness), key=lambda x: x[1])
    new_population = [individual for individual, fit in combined[:len(population)]]
    new_fitness = [fit for individual, fit in combined[:len(population)]]
    return new_population, new_fitness

# Genetic Algorithm
def genetic_algorithm(M, requests, user_server_times, pop_size, generations, crossover_rate, mutation_rate, num_parents):
    population = initialize_population(pop_size, len(M), len(user_server_times[0])-1)
    fitness = [evaluate_fitness(ind, M, requests, user_server_times) for ind in population]
    
    for generation in range(generations):
        parents = select_parents(population, fitness, num_parents)
        new_population = []
        
        for i in range(0, len(parents), 2):
            parent1 = parents[i]
            parent2 = parents[(i + 1) % len(parents)]
            child1, child2 = crossover(parent1, parent2, crossover_rate)
            new_population.append(mutate(child1, mutation_rate, len(user_server_times[0])-1))
            new_population.append(mutate(child2, mutation_rate, len(user_server_times[0])-1))
        
        new_fitness = [evaluate_fitness(ind, M, requests, user_server_times) for ind in new_population]
        population, fitness = replacement(population, new_population, fitness, new_fitness)
        
        best_fitness = min(fitness)
        best_solution = population[fitness.index(best_fitness)]
        print(f"Generation {generation}: Best Fitness = {best_fitness}")
    
    return best_solution, best_fitness

# Example usage
best_solution, best_fitness = genetic_algorithm(
    M, requests, user_server_times,
    pop_size=50, generations=100, crossover_rate=0.7, mutation_rate=0.1, num_parents=20
)

print(f"Best solution: {best_solution}, Fitness: {best_fitness}")

# Write the solution to a file
with open("solution_b.txt", "w") as f:
    for server in range(1, N+1):
        data_on_server = [i+1 for i, s in enumerate(best_solution) if s == server]
        f.write(f"{server} {' '.join(map(str, data_on_server))}\n")
    f.write(f"Optimization function value: {best_fitness}\n")
```

#### **Task (в): Data Allocation with Capacity Constraints**

To solve this task, we need to determine the data allocation to local servers with a capacity constraint of 64 GB per server, such that the optimization function is minimized.

#### **Python Implementation**

```python
# Evaluate fitness with capacity constraints
def evaluate_fitness_with_capacity(individual, M, requests, user_server_times, local_server_capacity):
    total_time = 0
    server_loads = [0] * (len(user_server_times[0]) - 1)
    
    for i, server in enumerate(individual):
        if server > 0:
            server_loads[server - 1] += M[i]
    
    if any(load > local_server_capacity for load in server_loads):
        return float('inf')
    
    for req in requests:
        user, data_idx, access_count = req
        server_times = [user_server_times[user-1][s] if individual[data_idx] == s else float('inf') for s in range(len(user_server_times[0]))]
        min_time = min(server_times)
        total_time += access_count * min_time
    
    return total_time

# Genetic Algorithm with capacity constraints
def genetic_algorithm_with_capacity(M, requests, user_server_times, local_server_capacity, pop_size, generations, crossover_rate, mutation_rate, num_parents):
    population = initialize_population(pop_size, len(M), len(user_server_times[0])-1)
    fitness = [evaluate_fitness_with_capacity(ind, M, requests, user_server_times, local_server_capacity) for ind in population]
    
    for generation in range(generations):
        parents = select_parents(population, fitness, num_parents)
        new_population = []
        
        for i in range(0, len(parents), 2):
            parent1 = parents[i]
            parent2 = parents[(i + 1) % len(parents)]
            child1, child2 = crossover(parent1, parent2, crossover_rate)
            new_population.append(mutate(child1, mutation_rate, len(user_server_times[0])-1))