from BuySellQueue import BuySellQueue
from simulation.models import Stock


class Broker:

    def __init__(self, name):

        self.name = name
        self.k = 0.5  # A constant factor representing the market maker's risk tolerance and desired profit margin.
        self.c = 0.01  # A constant representing fixed costs or other market-specific adjustments.
        self.queues : dict[str,BuySellQueue]= {}


    def get_queue(self, ticker):
        if ticker not in self.queues:
            self.queues[ticker] = BuySellQueue()
        return self.queues[ticker]


    def adjustClientPrice(self, best_bid, best_ask, spread, transaction_type):

        midprice = (best_bid + best_ask) / 2

        if transaction_type == "buy":
            ask_price = midprice + spread / 2
            return ask_price
        else:
            bid_price = midprice - spread / 2
            return bid_price


    def getBestPrices(self, asset):

        stock = Stock.objects.get(ticker=asset)
        best_bid = stock.low_price
        best_ask = stock.high_price

        return best_bid, best_ask

    # Missing limit order logic
    def add_to_buysell_queue(self, user, asset, amount, price, transaction_type):

        stock_queue = self.get_queue(asset)
        best_bid, best_ask = self.getBestPrices(asset)
        #TODO make the spread constant a simulation_settings parameter
        spread = 0.01 * amount

        if transaction_type == "buy":
            adjusted_price = self.adjustClientPrice(best_bid, best_ask, spread, "buy")
            stock_queue.add_to_buy_queue(user, asset, amount, adjusted_price)
            if adjusted_price > best_ask:
                stock = Stock.objects.get(ticker=asset)
                stock.high_price = adjusted_price
                stock.save()
        else:
            adjusted_price = self.adjustClientPrice(best_bid, best_ask, spread, "sell")
            stock_queue.add_to_sell_queue(user, asset, amount, adjusted_price)
            if adjusted_price < best_bid:
                stock = Stock.objects.get(ticker=asset)
                stock.low_price = adjusted_price
                stock.save()

    #Define a frequency to call this method
    def processQueues(self):
        for queue in self.queues.values() :
            queue.process_queues()

        

broker = Broker("Algo")