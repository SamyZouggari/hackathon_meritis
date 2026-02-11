from stable_baselines3 import PPO

from bot_env import TradingEnvironment as TradingEnv

EPISODES = 10

env = TradingEnv()
timesteps = env.agent.n_steps * EPISODES

model = PPO("MlpPolicy", env, verbose=1, device="cuda")
model.learn(total_timesteps=timesteps)
model.save("ppo_trading")
