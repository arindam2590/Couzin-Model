# Couzin Model Swarm Simulation

This repository contains a Python implementation of the Couzin Model for simulating and visualizing swarm behavior. The Couzin Model is a well-known framework used to study collective motion in biological systems, such as schools of fish, flocks of birds, and herds of animals. The implementation visualizes how agents interact within a swarm based on local rules of repulsion, alignment, and attraction.

### Features

- Swarm Simulation: Simulate a group of agents (robots, animals, etc.) interacting based on the Couzin Model.
- Visualization: Real-time animation of the swarm behavior using Matplotlib's quiver plot.
- Modular Design: Easy-to-understand code structure with separate classes for the agent, swarm, and simulation.
- Configurable Parameters: Adjust parameters like the number of agents, speed, interaction radii, and noise to explore different swarm dynamics.

#### Dependencies
- ```'numpy'
- ```'matplotlib'
- ```'scipy'

#### Usage
1. ##### Run the simulation:
   ``` python3 couzin_main.py
2. ##### Adjust parameters:
   You can modify the parameters in the Simulation class within simulation.py to explore different behaviors. Key parameters include:
   - ``` 'num_agent': Number of agents in the swarm.
   - ``` 'speed': Speed of each agent.
   - ``` 'space_size': Size of the 2D simulation space.
   - ``` 'sigma': Standard deviation of the noise applied to agent movement.
   - ``` 'rep_r': Repulsion radius.
   - ``` 'orien_r': Orientation radius.
   - ``` 'attr_r': Attraction radius.
   - ``` 'dt': Time step for the simulation.
