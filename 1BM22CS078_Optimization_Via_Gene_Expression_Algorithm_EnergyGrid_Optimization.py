import numpy as np
import random
print("Charan G 1BM22CS078")
# Define the smart grid problem
def create_smart_grid(num_nodes, max_supply, max_demand):
    """
    Initialize a smart grid with supply and demand values.
    """
    supply = np.random.randint(0, max_supply + 1, size=num_nodes)
    demand = np.random.randint(0, max_demand + 1, size=num_nodes)
    return supply, demand

# Fitness function: evaluate energy distribution
def evaluate_fitness(chromosome, supply, demand, transmission_efficiency):
    """
    Fitness is calculated as the negative of total energy loss.
    Chromosome represents the energy distribution matrix.
    """
    losses = 0
    for i in range(len(supply)):
        for j in range(len(demand)):
            # Calculate energy loss: E_loss = transmitted_energy * (1 - efficiency)
            energy_transmitted = chromosome[i][j]
            losses += energy_transmitted * (1 - transmission_efficiency[i][j])
    
    # Check supply/demand constraints
    supply_used = np.sum(chromosome, axis=1)
    demand_met = np.sum(chromosome, axis=0)
    
    # Penalty for exceeding supply or not meeting demand
    penalty = (
        np.sum(np.maximum(0, supply_used - supply)) +  # Exceeding supply
        np.sum(np.maximum(0, demand - demand_met))     # Unmet demand
    )
    
    return -(losses + penalty)  # Negative because we minimize losses

# Genetic operators
def mutate(chromosome, mutation_rate, max_supply):
    """
    Randomly mutate some elements in the chromosome.
    """
    new_chromosome = chromosome.copy()
    for i in range(new_chromosome.shape[0]):
        for j in range(new_chromosome.shape[1]):
            if random.random() < mutation_rate:
                new_chromosome[i][j] = random.uniform(0, max_supply)
    return new_chromosome

def crossover(parent1, parent2):
    """
    Perform crossover between two parents to generate offspring.
    """
    crossover_point = random.randint(0, parent1.shape[1] - 1)
    offspring = parent1.copy()
    offspring[:, crossover_point:] = parent2[:, crossover_point:]
    return offspring

# Initialize population
def initialize_population(pop_size, num_nodes, max_supply):
    """
    Create an initial population of chromosomes.
    Each chromosome is a 2D array representing energy distribution.
    """
    population = []
    for _ in range(pop_size):
        chromosome = np.random.uniform(0, max_supply, size=(num_nodes, num_nodes))
        population.append(chromosome)
    return population

# Main optimization loop
def optimize_energy_distribution(num_nodes, max_supply, max_demand, num_generations, pop_size, mutation_rate):
    """
    Optimize energy distribution using Gene Expression Algorithm.
    """
    # Initialize smart grid
    supply, demand = create_smart_grid(num_nodes, max_supply, max_demand)
    transmission_efficiency = np.random.uniform(0.8, 1.0, size=(num_nodes, num_nodes))  # Efficiency matrix
    
    # Initialize population
    population = initialize_population(pop_size, num_nodes, max_supply)
    
    # Evolution loop
    for generation in range(num_generations):
        # Evaluate fitness for each chromosome
        fitness_scores = [
            evaluate_fitness(chromosome, supply, demand, transmission_efficiency)
            for chromosome in population
        ]
        
        # Selection: choose top individuals
        sorted_population = [chrom for _, chrom in sorted(zip(fitness_scores, population), key=lambda x: x[0], reverse=True)]
        population = sorted_population[:pop_size // 2]  # Top 50%
        
        # Crossover: generate new offspring
        offspring = []
        while len(offspring) < pop_size // 2:
            parent1, parent2 = random.sample(population, 2)
            child = crossover(parent1, parent2)
            offspring.append(child)
        
        # Mutation
        offspring = [mutate(child, mutation_rate, max_supply) for child in offspring]
        
        # Combine old population with offspring
        population.extend(offspring)
    
    # Get the best solution
    best_chromosome = max(population, key=lambda chrom: evaluate_fitness(chrom, supply, demand, transmission_efficiency))
    best_fitness = evaluate_fitness(best_chromosome, supply, demand, transmission_efficiency)
    
    return best_chromosome, best_fitness, supply, demand

# Example usage
if __name__ == "__main__":
    num_nodes = 5  # Number of supply/demand nodes
    max_supply = 100
    max_demand = 80
    num_generations = 50
    pop_size = 20
    mutation_rate = 0.1

    best_solution, best_fitness, supply, demand = optimize_energy_distribution(
        num_nodes, max_supply, max_demand, num_generations, pop_size, mutation_rate
    )
    
    print("Best solution (energy distribution):")
    print(best_solution)
    print("Best fitness (negative of losses):", best_fitness)
    print("Supply:", supply)
    print("Demand:", demand)
