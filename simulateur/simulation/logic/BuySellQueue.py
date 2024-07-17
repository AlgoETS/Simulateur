from collections import deque
from django.db import transaction
from django.utils import timezone
from simulation.models import TransactionHistory
from simulation.models import Stock, Order, SimulationSettings


class BuySellQueue:
    def __init__(self):
        self.buy_queue = deque()
        self.sell_queue = deque()

    def add_to_buy_queue(self, user, asset, amount, price, scenario):
        self.buy_queue.append((user, asset, amount, price, scenario))

    def add_to_sell_queue(self, user, asset, amount, price, scenario):
        self.sell_queue.append((user, asset, amount, price, scenario))

    def process_queues(self):
        transactions = []
        while self.buy_queue and self.sell_queue:
            buy_order = self.buy_queue.popleft()
            sell_order = self.sell_queue.popleft()

            # check current price
            # if the

            if buy_order[3] >= sell_order[3]:  # Buy price >= Sell price
                matched_price = (buy_order[3] + sell_order[3]) / 2
                transactions.append(
                    self.execute_transaction(buy_order, sell_order, matched_price)
                )
        return transactions

    @transaction.atomic
    def execute_transaction(self, buy_order, sell_order, price):
        buyer, asset, amount, buy_price, scenario = buy_order
        seller, _, sell_amount, sell_price, scenario = sell_order

        if sell_amount >= amount:
            self.complete_transaction(buyer, seller, asset, amount, price, scenario)
            if sell_amount > amount:
                self.add_to_sell_queue(
                    seller, asset, sell_amount - amount, sell_price, scenario
                )
        else:
            self.partial_transaction(buyer, seller, asset, sell_amount, price, scenario)
            self.add_to_buy_queue(
                buyer, asset, amount - sell_amount, buy_price, scenario
            )

        return {
            "buyer": buyer.user.username,
            "seller": seller.user.username,
            "asset": asset.name,
            "amount": amount,
            "price": price,
            "timestamp": timezone.now().isoformat(),
        }

    def complete_transaction(self, buyer, seller, asset, amount, price, scenario):
        if scenario.simulation_settings.stock_trading_logic == "dynamic":
            # Modify stock price based on most recent transaction
            # scenario.stocks.get(ticker=asset)
            stock = Stock.objects.get(ticker=asset)
            stock.price = price
            stock.save()

        # Exchange the assets between seller and buyer
        seller.portfolio.stocks.remove(asset)
        buyer.portfolio.stocks.add(asset)
        # Add the amount to the user's balance
        seller.portfolio.balance += price * amount
        buyer.portfolio.balance -= price * amount
        seller.save()
        buyer.save()
        self.log_transaction(buyer, asset, "buy", amount, price)
        self.log_transaction(seller, asset, "sell", amount, price)

    def partial_transaction(self, buyer, seller, asset, sell_amount, price, scenario):
        if scenario.simulation_settings.stock_trading_logic == "dynamic":
            # Modify stock price based on most recent transaction
            # scenario.stocks.get(ticker=asset)
            stock = Stock.objects.get(ticker=asset)
            stock.price = price
            stock.save()
        # Exchange the assets between seller and buyer
        seller.portfolio.stocks.remove(asset)
        buyer.portfolio.stocks.add(asset)
        # Add the amount to the user's balance
        seller.portfolio.balance += price * sell_amount
        buyer.portfolio.balance -= price * sell_amount
        seller.save()
        buyer.save()
        self.log_transaction(buyer, asset, "buy", sell_amount, price)
        self.log_transaction(seller, asset, "sell", sell_amount, price)

    def log_transaction(self, user, asset, transaction_type, amount, price):
        # Create an order
        order = Order.objects.create(
            user=user,
            stock=asset,
            quantity=amount,
            price=price,
            transaction_type=transaction_type,
        )
        # Create a transaction history record
        transaction_history = TransactionHistory.objects.get_or_create(
            scenario_id=user.portfolio.scenario.id
        )
        transaction_history.orders.set([order])


buy_sell_queue = BuySellQueue()
