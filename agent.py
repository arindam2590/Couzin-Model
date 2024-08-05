import numpy as np

class Agent:
    def __init__(self, position, direction, speed):
        # Initialize agent's position, direction, and speed
        self.position = np.array(position)
        # Direction is represented as a unit vector
        self.unit_dir_vec = np.array([np.cos(direction), np.sin(direction)])
        # Desired direction for future movement, initially set to zero vector
        self.desire_direction = np.zeros_like(self.unit_dir_vec)
        self.speed = speed  # Movement speed of the agent
        # Color of the agent (assuming some visualization purpose)
        self.color = (0.0, 0.0, 1.0)  # Blue color
        # Maximum angle by which the agent can turn (5 degrees in radians)
        self.theta_max = 0.0872665
        # ZOR (Zone of Repulsion) influence vector
        self.d_r = np.zeros_like(self.unit_dir_vec)
        # ZOO (Zone of Orientation) influence vector
        self.d_o = np.zeros_like(self.unit_dir_vec)
        # ZOA (Zone of Attraction) influence vector
        self.d_a = np.zeros_like(self.unit_dir_vec)
        # Number of neighbors in each zone
        self.n_r = 0
        self.n_o = 0
        self.n_a = 0

    def update(self, space_size, dt):
        # Update the agent's direction towards its desired direction
        self.turn_towards_desire_direction()
        # Update the agent's position based on its current direction and speed
        self.position += self.unit_dir_vec * self.speed * dt

        # Handle boundary conditions to ensure the agent stays within the space
        if self.position[0] > space_size:
            self.position[0] = 0.0
        elif self.position[0] < 0.0:
            self.position[0] = space_size

        if self.position[1] > space_size:
            self.position[1] = 0.0
        elif self.position[1] < 0.0:
            self.position[1] = space_size

    def turn_towards_desire_direction(self):
        # Normalize current and desired direction vectors
        unit_v1 = self.unit_dir_vec / np.linalg.norm(self.unit_dir_vec)
        unit_v2 = self.desire_direction / np.linalg.norm(self.desire_direction)
        # Calculate the cosine of the angle between the current and desired directions
        cos_theta = np.dot(unit_v1, unit_v2)
        # Compute the angle in radians, clipped to handle numerical issues
        angle = np.arccos(np.clip(cos_theta, -1.0, 1.0))

        # Determine the direction of rotation (clockwise or counterclockwise)
        sign = np.sign(np.cross(self.unit_dir_vec, self.desire_direction))
        # Calculate the actual turn angle, limited by theta_max
        turn_angle = sign * min(angle, self.theta_max)
        # Create a rotation matrix for the computed turn angle
        rotation_matrix = np.array([[np.cos(turn_angle), -np.sin(turn_angle)],
                                    [np.sin(turn_angle), np.cos(turn_angle)]])
        # Rotate the current direction vector
        rotated_vec = np.dot(rotation_matrix, self.unit_dir_vec)
        # Normalize the rotated vector to maintain unit length
        self.unit_dir_vec = rotated_vec / np.linalg.norm(rotated_vec)

    def zor_update(self, r_ij):
        # Update Zone of Repulsion (ZOR) vector with the influence of neighbor j
        self.n_r += 1
        self.d_r += r_ij

    def zoo_update(self, v_j):
        # Update Zone of Orientation (ZOO) vector with the influence of neighbor j
        self.n_o += 1
        self.d_o += v_j

    def zoa_update(self, r_ij):
        # Update Zone of Attraction (ZOA) vector with the influence of neighbor j
        self.n_a += 1
        self.d_a += r_ij

    def evaluate_desire_direction(self, noise):
        # Determine the desired direction based on the zones
        if self.n_r > 0:
            # If there are neighbors in ZOR, repel (move away)
            d_i = -self.d_r
        elif self.n_o > 0 and self.n_a > 0:
            # If both ZOO and ZOA have neighbors, average their influences
            d_i = (self.d_o + self.d_a) * 0.5
        elif self.n_o > 0:
            # If only ZOO has neighbors, align with their direction
            d_i = self.d_o
        elif self.n_a > 0:
            # If only ZOA has neighbors, attract (move towards them)
            d_i = self.d_a
        else:
            # If no neighbors, continue in the current direction
            d_i = self.unit_dir_vec

        # Add random noise to the desired direction
        d_i += noise
        # Normalize the desired direction to maintain unit length
        norm = np.linalg.norm(d_i)
        if norm != 0:
            d_i /= norm

        # Update the desired direction
        self.desire_direction = d_i
