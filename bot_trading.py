import numpy as np
import pandas as pd

def load_csv_to_pd(file_path):
    return pd.read_csv(file_path)

class TradingAgent():
    def __init__(self, initial_cash=100000):
        self.market_data_MERI = load_csv_to_pd('data/MERI.csv')
        self.market_data_TIS = load_csv_to_pd('data/TIS.csv')
        self.n_steps = len(self.market_data_MERI)  # Assuming both have the same length
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions = {'MERI': 0, 'TIS': 0}
        self.current_step = 0

    def get_state(self):
        meri_data = self.market_data_MERI.iloc[self.current_step]
        tis_data = self.market_data_TIS.iloc[self.current_step]

        obs = np.array([
            meri_data['open'], meri_data['high'], meri_data['low'], meri_data['close'], meri_data['volume'],
            tis_data['open'], tis_data['high'], tis_data['low'], tis_data['close'], tis_data['volume'],
            self.cash / 100000,  # Normalize cash
            self.positions['MERI'],
            self.positions['TIS']
        ])
        return obs

    def execute_action(self, actions):
        """action = [MERI, TIS]"""
        # action = [nbMERI, nbTIS]
        nb_MERI, nb_TIS = actions
        nb_MERI = int(np.round(nb_MERI))
        nb_TIS = int(np.round(nb_TIS))

        self.trade(nb_MERI, "MERI")
        self.trade(nb_TIS, "TIS")

    def trade(self, request, asset):

        if asset == "MERI":
            current_price = self.market_data_MERI.iloc[self.current_step]['close']
        elif asset == "TIS":
            current_price = self.market_data_TIS.iloc[self.current_step]['close']
        
        if request < 0:  # Sell
            qty_sell = min(-request, self.positions[asset])  # Can't sell more than we have
            self.positions[asset] -= qty_sell
            self.cash += qty_sell * current_price
        elif request > 0:  # Buy
            max_buy = int(self.cash // current_price)
            qty_buy = min(request, max_buy)

            self.positions[asset] += qty_buy
            self.cash -= qty_buy * current_price

    def step(self, action):
        self.execute_action(action)
        self.current_step += 1
        done = self.current_step >= self.n_steps -1 
        
        if done:
            reward = self.calculate_reward()
        else:
            reward = 0
        
        obs = self.get_state()
        return obs, reward, done, {}

    def get_valuation(self):
        price_meri = self.market_data_MERI.iloc[self.current_step]['close']
        price_tis = self.market_data_TIS.iloc[self.current_step]['close']
        return self.cash + (self.positions['MERI'] * price_meri) + (self.positions['TIS'] * price_tis)

    def calculate_reward(self):
        valuation = self.get_valuation()
        
        return ((valuation - self.initial_cash)/ self.initial_cash)*100  # Reward is the profit/loss compared to initial cash

    def reset(self):
        self.cash = self.initial_cash
        self.positions = {'MERI': 0, 'TIS': 0}
        self.current_step = 0
        return self.get_state()
        
