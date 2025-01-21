from collections import defaultdict
import gymnasium as gym
import numpy as np

class BlackjackAgent:
    def __init__(
        self,
        env: gym.Env,
        learning_rate: float,
        initial_epsilon: float,
        epsilon_decay: float,
        final_epsilon: float,
        discount_factor: float = 0.95,
    ):
        """
        Inicializa un agente de aprendizaje por refuerzo con un diccionario vacío
        de valores de estado-acción (q_values), una tasa de aprendizaje y un epsilon.
        
        Args:
            env: El entorno de gym
            learning_rate: La tasa de aprendizaje para actualizar los valores-Q
            initial_epsilon: El valor inicial de epsilon
            epsilon_decay: La tasa de decaimiento de epsilon
            final_epsilon: El valor final de epsilon
            discount_factor: El factor de descuento para las recompensas futuras
        """
        self.env = env
        self.q_values = defaultdict(lambda: np.zeros(env.action_space.n))

        self.lr = learning_rate
        self.discount_factor = discount_factor

        self.epsilon = initial_epsilon
        self.epsilon_decay = epsilon_decay
        self.final_epsilon = final_epsilon

        self.training_error = []

    def get_action(self, obs: tuple[int, int, bool]) -> int:
        """
        Devuelve la mejor acción con probabilidad (1 - epsilon)
        de lo contrario, una acción aleatoria con probabilidad epsilon para garantizar la exploración.
        """
        # with probability epsilon return a random action to explore the environment
        if np.random.random() < self.epsilon:
            return self.env.action_space.sample()
        # with probability (1 - epsilon) act greedily (exploit)
        else:
            return int(np.argmax(self.q_values[obs]))

    def update(
        self,
        obs: tuple[int, int, bool],
        action: int,
        reward: float,
        terminated: bool,
        next_obs: tuple[int, int, bool],
    ):
        """Actualiza el valor-Q de una acción."""
        future_q_value = (not terminated) * np.max(self.q_values[next_obs])
        temporal_difference = (
            reward + self.discount_factor * future_q_value - self.q_values[obs][action]
        )

        self.q_values[obs][action] = (
            self.q_values[obs][action] + self.lr * temporal_difference
        )
        self.training_error.append(temporal_difference)

    def decay_epsilon(self):
        self.epsilon = max(self.final_epsilon, self.epsilon - self.epsilon_decay)
        