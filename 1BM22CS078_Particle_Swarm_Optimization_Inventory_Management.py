import random

# Define the cost function: Total inventory cost
def inventory_cost(Q, R, demand, holding_cost, ordering_cost, shortage_cost):
    """
    Calculate the total cost for given order quantity (Q) and reorder point (R).
    """
    if Q <= 0 or R < 0:
        return float('inf')  # Invalid values result in high cost
    
    # Simulate inventory system for a year
    total_holding_cost = Q / 2 * holding_cost  # Average inventory
    total_ordering_cost = (demand / Q) * ordering_cost  # Orders per year
    total_shortage_cost = max(0, (demand - Q - R)) * shortage_cost  # Shortage penalty
    
    return total_holding_cost + total_ordering_cost + total_shortage_cost

# PSO parameters
NUM_PARTICLES = 30  # Number of particles in the swarm
MAX_ITERATIONS = 45  # Number of iterations
W = 0.5  # Inertia weight
C1 = 1.5  # Cognitive constant
C2 = 1.5  # Social constant

# Problem parameters
demand = 500  # Annual demand
holding_cost = 2  # Cost to hold one unit per year
ordering_cost = 50  # Cost to place one order
shortage_cost = 20  # Cost per unit of unmet demand
Q_bounds = (1, 200)  # Bounds for order quantity
R_bounds = (0, 100)  # Bounds for reorder point

# Initialize the swarm
particles = []
velocities = []
pbest = []  # Personal best positions
pbest_cost = []  # Personal best costs
gbest = None  # Global best position
gbest_cost = float('inf')  # Global best cost

# Random initialization
for _ in range(NUM_PARTICLES):
    Q = random.uniform(*Q_bounds)
    R = random.uniform(*R_bounds)
    particles.append([Q, R])
    velocities.append([random.uniform(-1, 1), random.uniform(-1, 1)])
    cost = inventory_cost(Q, R, demand, holding_cost, ordering_cost, shortage_cost)
    pbest.append([Q, R])
    pbest_cost.append(cost)
    if cost < gbest_cost:
        gbest = [Q, R]
        gbest_cost = cost

# PSO main loop
for iteration in range(MAX_ITERATIONS):
    for i in range(NUM_PARTICLES):
        # Update velocity
        velocities[i][0] = (
            W * velocities[i][0] +
            C1 * random.random() * (pbest[i][0] - particles[i][0]) +
            C2 * random.random() * (gbest[0] - particles[i][0])
        )
        velocities[i][1] = (
            W * velocities[i][1] +
            C1 * random.random() * (pbest[i][1] - particles[i][1]) +
            C2 * random.random() * (gbest[1] - particles[i][1])
        )
        
        # Update position
        particles[i][0] += velocities[i][0]
        particles[i][1] += velocities[i][1]
        
        # Enforce bounds
        particles[i][0] = max(Q_bounds[0], min(Q_bounds[1], particles[i][0]))
        particles[i][1] = max(R_bounds[0], min(R_bounds[1], particles[i][1]))
        
        # Evaluate fitness
        cost = inventory_cost(particles[i][0], particles[i][1], demand, holding_cost, ordering_cost, shortage_cost)
        if cost < pbest_cost[i]:
            pbest[i] = particles[i][:]
            pbest_cost[i] = cost
        if cost < gbest_cost:
            gbest = particles[i][:]
            gbest_cost = cost
    
    print(f"Iteration {iteration + 1}: Best Cost = {gbest_cost:.2f}")

# Final result
print(f"Optimal Order Quantity (Q): {gbest[0]:.2f}")
print(f"Optimal Reorder Point (R): {gbest[1]:.2f}")
print(f"Minimum Cost: {gbest_cost:.2f}")
