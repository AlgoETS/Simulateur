import pandas as pd
import numpy as np
import json

class Strategy:
    def __init__(self, strategy_config, stock_data):
        self.strategy_name = strategy_config['strategy_name']
        self.stocks = strategy_config['stocks']
        self.parameters = strategy_config['parameters']
        self.init_instructions = strategy_config['init']
        self.tick_instructions = strategy_config['ticks']
        self.indicators = {}
        self.positions = []
        self.stock_data = stock_data  # Simulated stock data
        self.current_tick = 0

    def set_indicator(self, name, indicator_type, input_data, period):
        if indicator_type == "SMA":
            # Calculate the Simple Moving Average using pandas
            self.indicators[name] = self.stock_data[input_data].rolling(window=period).mean()

    def get_indicator(self, name):
        # Return the current value of the indicator at the current tick
        return self.indicators.get(name, [None])[self.current_tick]

    def evaluate_condition(self, condition):
        condition_type = condition['type']
        left = self.get_indicator(condition['left'])
        right = self.get_indicator(condition['right'])

        if left is None or right is None:
            return False  # If either indicator is None, skip the action

        if condition_type == "crosses_above":
            # Check for a crossover (simplified)
            if self.current_tick > 0:
                previous_left = self.indicators[condition['left']][self.current_tick - 1]
                previous_right = self.indicators[condition['right']][self.current_tick - 1]
                return previous_left <= previous_right and left > right

        return False

    def execute_init(self):
        for instruction in self.init_instructions:
            if instruction['action'] == "set":
                variable = instruction['variable']
                indicator_type = instruction['indicator']
                input_data = instruction['input']
                period = self.parameters[instruction['period']]
                self.set_indicator(variable, indicator_type, input_data, period)

    def execute_ticks(self):
        for tick in self.tick_instructions:
            condition = tick['condition']
            actions = tick['actions']
            if self.evaluate_condition(condition):
                for action in actions:
                    self.perform_action(action['action'])

    def perform_action(self, action):
        if action == "buy":
            print(f"Tick {self.current_tick}: Executing Buy Order")
            self.positions.append(("Buy", self.stock_data['close'][self.current_tick]))
        elif action == "sell":
            print(f"Tick {self.current_tick}: Executing Sell Order")
            self.positions.append(("Sell", self.stock_data['close'][self.current_tick]))

    def run_strategy(self):
        print(f"Running Strategy: {self.strategy_name}")
        print("Initializing Strategy...")
        self.execute_init()
        print("Executing Ticks...")

        # Simulate each tick in the stock data
        for self.current_tick in range(len(self.stock_data)):
            self.execute_ticks()

        print("Strategy Execution Completed")

# Generate Simulated Stock Data
np.random.seed(42)  # For reproducibility
dates = pd.date_range(start="2024-01-01", periods=100, freq="D")
prices = np.cumsum(np.random.randn(100)) + 100  # Simulated random walk stock prices

stock_data = pd.DataFrame({
    'date': dates,
    'close': prices
})

# Example JSON strategy configuration
strategy_json = '''
{
  "strategy_name": "SmaCross",
  "stocks": ["APPL"],
  "parameters": {
    "n1": 10,
    "n2": 20
  },
  "init": [
    {
      "action": "set",
      "variable": "sma1",
      "indicator": "SMA",
      "input": "close",
      "period": "n1"
    },
    {
      "action": "set",
      "variable": "sma2",
      "indicator": "SMA",
      "input": "close",
      "period": "n2"
    }
  ],
  "ticks": [
    {
      "condition": {
        "type": "crosses_above",
        "left": "sma1",
        "right": "sma2"
      },
      "actions": [
        {
          "action": "buy"
        }
      ]
    },
    {
      "condition": {
        "type": "crosses_above",
        "left": "sma2",
        "right": "sma1"
      },
      "actions": [
        {
          "action": "sell"
        }
      ]
    }
  ]
}
'''

# Load and parse the JSON strategy configuration
strategy_config = json.loads(strategy_json)

# Create an instance of the strategy with simulated stock data
strategy = Strategy(strategy_config, stock_data)

# Run the strategy
strategy.run_strategy()