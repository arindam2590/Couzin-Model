import numpy as np
from agent import Agent  # Importing the Agent class from a separate file named agent.py
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Swarm:
    def __init__(self, N, speed, space_size, sigma, rep_r, orien_r, attr_r, dt):
        # Initialize swarm parameters
        self.num_agents = N  # Number of agents in the swarm
        self.dt = dt  # Time step for the simulation
        self.space_size = space_size  # Size of the space in which the swarm operates
        self.sigma = sigma  # Standard deviation of the noise applied to agents' movement

        # Initialize agents
        self.agents = Swarm.__initialize_agent(N, speed)

        # Define radii for different zones of interaction
        self.repul_radius = rep_r  # Repulsion radius
        self.orien_radius = orien_r  # Orientation radius
        self.attrac_radius = attr_r  # Attraction radius

    def __initialize_agent(N, speed):
        # Initialize each agent at a random position near a source point with random direction
        source = (30, 30)  # Starting point for the swarm
        return [Agent(np.random.uniform(source[0] - 10, source[1] + 10, 2), np.random.rand() * 2 * np.pi, speed) for _ in range(N)]

    def reset_swarm(self):
        # Reset the forces and neighbor counts for each agent
        for agent in self.agents:
            agent.d_r = np.zeros_like(agent.unit_dir_vec)  # Reset repulsion force vector
            agent.d_o = np.zeros_like(agent.unit_dir_vec)  # Reset orientation force vector
            agent.d_a = np.zeros_like(agent.unit_dir_vec)  # Reset attraction force vector
            agent.n_r = 0  # Reset repulsion neighbors count
            agent.n_a = 0  # Reset attraction neighbors count
            agent.n_o = 0  # Reset orientation neighbors count

    def generate_noise(self, sigma):
        # Generate noise for the agent's direction, based on the provided sigma (standard deviation)
        return np.random.normal(0, sigma)

    def simulate(self):
        # Simulate one time step for all agents
        self.reset_swarm()  # Reset the forces and neighbor counts

        for agent in self.agents:
            c_i = agent.position  # Current position of the agent
            for other_agent in self.agents:
                c_j = other_agent.position  # Position of another agent
                r_ij = (c_j - c_i)  # Vector from agent to another agent
                distance = np.linalg.norm(r_ij)  # Euclidean distance between the two agents
                distances = np.minimum(distance, self.space_size - distance)  # Handle edge cases by wrapping around

                if distance != 0:  # If distance is not zero (to avoid division by zero)
                    r_ij /= distance  # Normalize the distance vector
                    if distance < self.repul_radius:
                        agent.zor_update(r_ij)  # Update agent behavior if within the repulsion radius
                    else:
                        v_j = other_agent.unit_dir_vec  # Direction vector of the other agent
                        if distance >= self.repul_radius and distance < self.orien_radius:
                            agent.zoo_update(v_j)  # Update agent behavior if within the orientation radius
                        elif distance >= self.orien_radius and distance < self.attrac_radius:
                            agent.zoa_update(r_ij)  # Update agent behavior if within the attraction radius

            if agent.n_o > 0:
                agent.d_o /= (agent.n_o + 1)  # Average orientation direction if there are orientation neighbors

            noise = self.generate_noise(self.sigma)  # Generate noise to add to the agent's direction
            agent.evaluate_desire_direction(noise)  # Calculate the desired direction considering all forces

        for agent in self.agents:
            agent.update(self.space_size, self.dt)  # Update the agent's position based on its desired direction


class Simulation:
    def __init__(self, num_agent=100, speed=2.0, space_size=100, sigma=0.1, rep_r=3, orien_r=7, attr_r=12, dt=1.0):
        # Initialize the simulation environment
        self.fig, self.ax = plt.subplots(figsize=(10, 10))  # Create a figure and axis for the animation
        self.ax.set_xlim(0, space_size)  # Set the limits for the x-axis
        self.ax.set_ylim(0, space_size)  # Set the limits for the y-axis

        # Initialize the swarm with given parameters
        self.swarm = Swarm(num_agent, speed, space_size, sigma, rep_r, orien_r, attr_r, dt)
        self.scat = self.ax.quiver([agent.position[0] for agent in self.swarm.agents],
                                   [agent.position[1] for agent in self.swarm.agents],
                                   [agent.unit_dir_vec[0] for agent in self.swarm.agents],
                                   [agent.unit_dir_vec[1] for agent in self.swarm.agents],
                                   color=[agent.color for agent in self.swarm.agents])  # Initialize the quiver plot for visualization

    def animate(self, frame):
        # Animation function that updates the swarm visualization for each frame
        self.swarm.simulate()  # Simulate the swarm's behavior for one time step
        self.scat.set_offsets([agent.position for agent in self.swarm.agents])  # Update agent positions
        self.scat.set_UVC([agent.unit_dir_vec[0] for agent in self.swarm.agents],
                          [agent.unit_dir_vec[1] for agent in self.swarm.agents])  # Update agent directions

        return self.scat,

    def run(self):
        # Run the animation
        ani = animation.FuncAnimation(self.fig, self.animate, frames=100, interval=10, blit=True)  # Animate the swarm
        plt.show()  # Display the animation
