import random

# Network graph (edges with weights)
network = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

# Genetic Algorithm Parameters
POPULATION_SIZE = 6
GENERATIONS = 10
MUTATION_RATE = 0.2

# Fitness function: calculate the cost of a path
def fitness(path):
    cost = 0
    for i in range(len(path) - 1):
        if path[i + 1] in network[path[i]]:
            cost += network[path[i]][path[i + 1]]
        else:
            return float('inf')  # Invalid path
    return cost

# Generate a random path
def random_path(start, end):
    path = [start]
    while path[-1] != end:
        next_hop = random.choice(list(network[path[-1]].keys()))
        if next_hop in path:  # Avoid cycles
            continue
        path.append(next_hop)
    return path

# Crossover: combine two parent paths
def crossover(parent1, parent2):
    split = random.randint(1, min(len(parent1), len(parent2)) - 2)
    child = parent1[:split] + [node for node in parent2 if node not in parent1[:split]]
    return child

# Mutation: randomly modify a path
def mutate(path):
    if random.random() < MUTATION_RATE:
        index = random.randint(1, len(path) - 2)  # Avoid mutating start/end
        new_node = random.choice(list(network[path[index - 1]].keys()))
        path[index] = new_node
    return path

# Initialize population
def initialize_population(start, end):
    return [random_path(start, end) for _ in range(POPULATION_SIZE)]

# Genetic Algorithm
def genetic_algorithm(start, end):
    population = initialize_population(start, end)
    
    for generation in range(GENERATIONS):
        # Evaluate fitness
        population = sorted(population, key=fitness)
        print(f"Generation {generation}: Best path {population[0]} with cost {fitness(population[0])}")
        
        # Selection: keep the top 50% of the population
        top_half = population[:len(population) // 2]
        
        # Crossover and mutation to produce new population
        new_population = top_half[:]
        while len(new_population) < POPULATION_SIZE:
            parent1, parent2 = random.sample(top_half, 2)
            child = crossover(parent1, parent2)
            new_population.append(mutate(child))
        
        population = new_population

    # Return the best solution
    best_path = min(population, key=fitness)
    return best_path, fitness(best_path)

# Example usage
start_node = 'A'
end_node = 'D'
best_path, best_cost = genetic_algorithm(start_node, end_node)
print(f"Best path found: {best_path} with cost: {best_cost}")







'''
Network Graph:
Represented as a dictionary where keys are nodes and values are neighbors with edge weights.

Fitness Function:
Calculates the total cost of a path. Invalid paths get a fitness of infinity to exclude them from selection.

Population Initialization:
Random paths are generated from the start node to the end node.

Crossover and Mutation:
Crossover: Combines two parent paths by slicing and merging.
Mutation: Randomly alters a node in the path to introduce diversity.

Selection and Evolution:
The top 50% of the population (based on fitness) is selected for reproduction.
New paths are created through crossover and mutation.

Output:

The algorithm outputs the best path and its cost after a fixed number of generations.
'''
