import random

# Updated Network graph (edges with weights)
network = {
    'A': {'B': 1, 'C': 4, 'E': 7},
    'B': {'A': 1, 'C': 2, 'D': 5, 'F': 8},
    'C': {'A': 4, 'B': 2, 'D': 1, 'G': 6},
    'D': {'B': 5, 'C': 1, 'H': 3},
    'E': {'A': 7, 'F': 2, 'I': 4},
    'F': {'B': 8, 'E': 2, 'G': 3, 'J': 6},
    'G': {'C': 6, 'F': 3, 'H': 2},
    'H': {'D': 3, 'G': 2, 'J': 5},
    'I': {'E': 4, 'J': 3},
    'J': {'F': 6, 'H': 5, 'I': 3}
}

# Genetic Algorithm Parameters
POPULATION_SIZE = 10
GENERATIONS = 20
MUTATION_RATE = 0.3

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
end_node = 'H'
print("Start: ", start_node)
print("End: ", end_node)
best_path, best_cost = genetic_algorithm(start_node, end_node)
print(f"Best path found: {best_path} with cost: {best_cost}")
