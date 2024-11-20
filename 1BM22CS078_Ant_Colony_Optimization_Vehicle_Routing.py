import numpy as np
import random

# Problem definition
distances = np.array([
    [0, 10, 20, 30, 40],
    [10, 0, 15, 25, 35],
    [20, 15, 0, 18, 28],
    [30, 25, 18, 0, 22],
    [40, 35, 28, 22, 0]
])  # Distance matrix (depot + customers)

demands = [0, 4, 3, 2, 5]  # Demand for each customer (0 = depot)
vehicle_capacity = 6  # Max capacity per vehicle
num_vehicles = 2  # Number of vehicles
num_customers = len(demands) - 1  # Exclude depot

# ACO parameters
NUM_ANTS = 10
NUM_ITERATIONS = 50
ALPHA = 1.0  # Pheromone importance
BETA = 2.0  # Distance importance
EVAPORATION_RATE = 0.5  # Pheromone evaporation rate
Q = 100  # Pheromone deposit factor
INITIAL_PHEROMONE = 1.0

# Initialize pheromones
pheromones = np.full(distances.shape, INITIAL_PHEROMONE)

# ACO main loop
def vehicle_routing_aco():
    global pheromones
    best_routes = None
    best_cost = float('inf')

    for iteration in range(NUM_ITERATIONS):
        all_routes = []
        all_costs = []

        # Each ant constructs a solution
        for _ in range(NUM_ANTS):
            remaining_demand = demands[:]
            routes = []
            total_cost = 0

            for _ in range(num_vehicles):
                route = [0]  # Start at the depot
                capacity = vehicle_capacity

                while True:
                    current_city = route[-1]
                    probabilities = []

                    # Calculate probabilities for next customer
                    for next_city in range(1, len(distances)):
                        if next_city not in route and remaining_demand[next_city] > 0 and capacity >= remaining_demand[next_city]:
                            prob = (pheromones[current_city][next_city] ** ALPHA) * \
                                   ((1 / distances[current_city][next_city]) ** BETA)
                            probabilities.append(prob)
                        else:
                            probabilities.append(0)  # Invalid choices
                    
                    if sum(probabilities) == 0:
                        break  # No more feasible customers
                    probabilities = np.array(probabilities) / np.sum(probabilities)
                    next_city = np.random.choice(range(len(distances)), p=probabilities)
                    
                    # Update route and capacities
                    route.append(next_city)
                    capacity -= remaining_demand[next_city]
                    remaining_demand[next_city] = 0
                
                route.append(0)  # Return to depot
                routes.append(route)
                total_cost += sum(distances[route[i]][route[i + 1]] for i in range(len(route) - 1))

            all_routes.append(routes)
            all_costs.append(total_cost)

        # Update best solution
        for i, cost in enumerate(all_costs):
            if cost < best_cost:
                best_cost = cost
                best_routes = all_routes[i]

        # Update pheromones
        pheromones *= (1 - EVAPORATION_RATE)  # Evaporation
        for i, routes in enumerate(all_routes):
            for route in routes:
                for j in range(len(route) - 1):
                    pheromones[route[j]][route[j + 1]] += Q / all_costs[i]

        print(f"Iteration {iteration + 1}: Best Cost = {best_cost:.2f}")

    return best_routes, best_cost

# Run ACO for VRP
best_routes, best_cost = vehicle_routing_aco()
print("\nOptimal Routes:")
for i, route in enumerate(best_routes):
    print(f"Vehicle {i + 1}: {route}")
print(f"Minimum Cost: {best_cost:.2f}")





'''
Distance Matrix:

Represents the distances between all locations (depot and customers).
Demands and Vehicle Capacity:

demands specifies the amount each customer requires. Vehicles have a fixed capacity (vehicle_capacity).
Route Construction:

Each ant assigns customers to vehicles while ensuring capacity constraints are met.
Probabilities for the next customer are based on pheromones and inverse distance.
Pheromone Update:

Evaporation reduces pheromone levels over time to prevent stagnation.
Successful routes deposit more pheromones, reinforcing good solutions.
Output:

The best set of routes for all vehicles and the minimum cost are displayed.
'''
