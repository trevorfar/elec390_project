import random
import matplotlib.pyplot as plt

def simulate_queue(lambda_val, mu=0.75, num_slots=10**6):
    queue = []
    server_busy = False
    total_queue_length = 0
    
    for _ in range(num_slots):
        # Service completion phase
        if server_busy:
            if random.random() < mu:
                server_busy = False
        
        # Arrival phase
        if random.random() < lambda_val:
            queue.append(1)  # Add packet to the queue
        
        # Service start phase
        if not server_busy and queue:
            queue.pop(0)
            server_busy = True
        
        # Update total queue length
        total_queue_length += len(queue)
    
    average_queue_length = total_queue_length / num_slots
    average_delay = average_queue_length / lambda_val
    return average_delay

# Parameters
mu = 0.75
lambdas = [0.2, 0.4, 0.5, 0.6, 0.65, 0.7, 0.72, 0.74, 0.745]

# Simulation
sim_delays = []
for lam in lambdas:
    print(f"Simulating λ={lam:.3f}...")
    delay = simulate_queue(lam, mu)
    sim_delays.append(delay)
    print(f"  Average delay: {delay:.2f}")

# Theoretical calculation
theoretical_delays = [lam / (mu * (mu - lam)) for lam in lambdas]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(lambdas, sim_delays, 'bo-', label='Simulation')
plt.plot(lambdas, theoretical_delays, 'r--', label='Theoretical')
plt.xlabel('Arrival Rate (λ)')
plt.ylabel('Average Queueing Delay')
plt.title('Simulation vs Theoretical Queueing Delay')
plt.legend()
plt.grid(True)

# Save the plot to a file
plt.savefig('queueing_delay_plot.png')
print("Plot saved as 'queueing_delay_plot.png'")
