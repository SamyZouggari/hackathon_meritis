from gymnasium import spaces
from gymnasium import Env
import numpy as np
from bot_trading import TradingAgent


class TradingEnvironment(Env):
    def __init__(self):
        super().__init__()
        self.agent = TradingAgent()
        self.action_space = spaces.Box(low=-1000, high=1000, shape=(2,), dtype=np.float32)
        self.observation_space = spaces.Box(low=0, high=np.inf, shape=(19,), dtype=np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        obs = self.agent.reset()
        return obs.astype(np.float32), {}

    def step(self, action):
        action = np.array(action, dtype=np.float32)
        obs, reward, done, info = self.agent.step(action)
        terminated = bool(done)
        truncated = False
        return obs.astype(np.float32), float(reward), terminated, truncated, info
