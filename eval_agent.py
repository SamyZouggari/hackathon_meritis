from stable_baselines3 import PPO
from bot_env import TradingEnvironment as TradingEnv


def main():
    env = TradingEnv()
    model = PPO.load("ppo_trading", env=env)

    obs, _ = env.reset()
    terminated = False
    truncated = False
    reward = 0.0

    while not (terminated or truncated):
        action, _ = model.predict(obs, deterministic=False)
        obs, reward, terminated, truncated, info = env.step(action)

    print(f"Reward final: {reward:.2f}%")
    print(f"Valuation finale: {env.agent.get_valuation():,.2f}€")
    print(f"Cash: {env.agent.cash:,.2f}€")
    print(f"Positions: {env.agent.positions}")


if __name__ == "__main__":
    main()