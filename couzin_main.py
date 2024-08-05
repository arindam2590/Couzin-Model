# Import the Simulation class from the couzinmodel module
from couzinmodel import Simulation


def main():
    # Set the parameters for the simulation
    N = 30       # Number of agents in the swarm
    r_rep = 5    # Radius of repulsion (agents will try to avoid being within this distance of each other)
    r_ori = 30   # Radius of orientation (agents align their direction with others within this distance)
    r_att = 32   # Radius of attraction (agents are attracted to others within this distance)
    speed = 1.0  # Speed at which agents move
    sigma = 0.1  # Noise factor for randomness in movement
    dt = 0.1     # Time step for simulation updates
    space_size = 150  # Size of the 2D space in which the agents move

    # Initialize the simulation with the specified parameters
    sim = Simulation(N, speed, space_size, sigma, r_rep, r_ori, r_att, dt)

    # Run the simulation
    sim.run()


if __name__ == "__main__":
    main()
