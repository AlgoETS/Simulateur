from simulation.logic import BuySellQueue
from simulation.models import Stock


class Broker:

    def __init__(self, name):
        self.name = name
        self.k = 0.5  # Market maker's risk tolerance and desired profit margin.
        self.c = 0.01  # Fixed costs or other market-specific adjustments.
        self.queues = {}

    def get_queue(self, ticker):
        if ticker not in self.queues:
            self.queues[ticker] = BuySellQueue()
        return self.queues[ticker]

    def adjust_client_price(self, best_bid, best_ask, spread, transaction_type):
        midprice = (best_bid + best_ask) / 2
        if transaction_type == "buy":
            ask_price = midprice + spread / 2
            return ask_price
        else:
            bid_price = midprice - spread / 2
            return bid_price

    def get_best_prices(self, asset):
        stock = Stock.objects.get(ticker=asset)
        best_bid = stock.low_price
        best_ask = stock.high_price
        return best_bid, best_ask

    def add_to_buysell_queue(self, user, asset, amount, price, transaction_type):
        stock_queue = self.get_queue(asset)
        best_bid, best_ask = self.get_best_prices(asset)
        spread = 0.01 * amount  # TODO: Make the spread constant a simulation_settings parameter

        if transaction_type == "buy":
            adjusted_price = self.adjust_client_price(best_bid, best_ask, spread, "buy")
            stock_queue.add_to_buy_queue(user, asset, amount, adjusted_price)
            if adjusted_price > best_ask:
                stock = Stock.objects.get(ticker=asset)
                stock.high_price = adjusted_price
                stock.save()
        else:
            adjusted_price = self.adjust_client_price(best_bid, best_ask, spread, "sell")
            stock_queue.add_to_sell_queue(user, asset, amount, adjusted_price)
            if adjusted_price < best_bid:
                stock = Stock.objects.get(ticker=asset)
                stock.low_price = adjusted_price
                stock.save()

    def process_queues(self):
        for queue in self.queues.values():
            queue.process_queues()


broker = Broker("Algo")
