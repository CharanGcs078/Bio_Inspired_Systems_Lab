import numpy as np
print("CHARAN G 1BM22CS078")
def initialize_grid(grid_size, max_demand):
    """Initialize the grid with random demands and initial allocations."""
    demand = np.random.randint(1, max_demand, (grid_size, grid_size))
    allocation = np.random.randint(0, max_demand, (grid_size, grid_size))
    return demand, allocation

def calculate_cost(demand, allocation):
    """Calculate the total cost as the sum of absolute deviations."""
    return np.sum(np.abs(allocation - demand))

def update_allocation(demand, allocation, max_transfer):
    """Update resource allocation based on neighbor interactions."""
    grid_size = demand.shape[0]
    new_allocation = allocation.copy()
    
    for i in range(grid_size):
        for j in range(grid_size):
            # Skip if allocation matches demand
            if allocation[i, j] == demand[i, j]:
                continue

            # Define neighbors in a Von Neumann neighborhood
            neighbors = [
                (i-1, j), (i+1, j), (i, j-1), (i, j+1)
            ]
            
            for ni, nj in neighbors:
                if 0 <= ni < grid_size and 0 <= nj < grid_size:
                    # Calculate resource transfer
                    transfer = min(max_transfer, abs(demand[i, j] - allocation[i, j]))
                    if allocation[i, j] < demand[i, j]:  # Needs more resources
                        available = max(0, allocation[ni, nj] - demand[ni, nj])
                        actual_transfer = min(transfer, available)
                        new_allocation[i, j] += actual_transfer
                        new_allocation[ni, nj] -= actual_transfer
                    elif allocation[i, j] > demand[i, j]:  # Has surplus
                        needed = max(0, demand[ni, nj] - allocation[ni, nj])
                        actual_transfer = min(transfer, needed)
                        new_allocation[i, j] -= actual_transfer
                        new_allocation[ni, nj] += actual_transfer
    
    return new_allocation

# Parameters
grid_size = 5
max_demand = 20
max_transfer = 5
iterations = 20

# Initialize demand and allocation grids
demand, allocation = initialize_grid(grid_size, max_demand)

# Optimization loop
for _ in range(iterations):
    allocation = update_allocation(demand, allocation, max_transfer)
    cost = calculate_cost(demand, allocation)
    print(f"Iteration Cost: {cost}")

# Final Results

print("\nFinal Demand:")
print(demand)
print("\nFinal Allocation:")
print(allocation)
print(f"\nFinal Cost: {calculate_cost(demand, allocation)}")
