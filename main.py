import gymnasium as gym
import ale_py

gym.register_envs(ale_py)
env = gym.make("ALE/Breakout-v5")
observation, info = env.reset()

episode_over = False
while not episode_over:
    action = env.action_space.sample()  # agent policy that uses the observation and info
    print(action)
    observation, reward, terminated, truncated, info = env.step(action)
    print(observation, reward, terminated, truncated, info)

    episode_over = terminated or truncated

env.close()