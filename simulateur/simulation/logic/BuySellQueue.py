from collections import deque
from django.db import transaction
from django.utils import timezone
from simulation.models import Stock, Order, TransactionHistory


class BuySellQueue:
    def __init__(self):
        self.buy_queue = deque()
        self.sell_queue = deque()

    def add_to_buy_queue(self, user, asset, amount, price, simulation_manager):
        self.buy_queue.append((user, asset, amount, price, simulation_manager))

    def add_to_sell_queue(self, user, asset, amount, price, simulation_manager):
        self.sell_queue.append((user, asset, amount, price, simulation_manager))

    def process_queues(self):
        transactions = []
        while self.buy_queue and self.sell_queue:
            buy_order = self.buy_queue.popleft()
            sell_order = self.sell_queue.popleft()

            if buy_order[3] >= sell_order[3]:  # Buy price >= Sell price
                matched_price = (buy_order[3] + sell_order[3]) / 2
                transactions.append(
                    self.execute_transaction(buy_order, sell_order, matched_price)
                )
        return transactions

    @transaction.atomic
    def execute_transaction(self, buy_order, sell_order, price):
        buyer, asset, amount, buy_price, simulation_manager = buy_order
        seller, _, sell_amount, sell_price, simulation_manager = sell_order

        if sell_amount >= amount:
            self.complete_transaction(buyer, seller, asset, amount, price, simulation_manager)
            if sell_amount > amount:
                self.add_to_sell_queue(
                    seller, asset, sell_amount - amount, sell_price, simulation_manager
                )
        else:
            self.partial_transaction(buyer, seller, asset, sell_amount, price, simulation_manager)
            self.add_to_buy_queue(
                buyer, asset, amount - sell_amount, buy_price, simulation_manager
            )

        return {
            "buyer": buyer.user.username,
            "seller": seller.user.username,
            "asset": asset.ticker,
            "amount": amount,
            "price": price,
            "timestamp": timezone.now().isoformat(),
        }

    def complete_transaction(self, buyer, seller, asset, amount, price, simulation_manager):
        if simulation_manager.simulation_settings.stock_trading_logic == "dynamic":
            stock = Stock.objects.get(ticker=asset.ticker)
            stock.price = price
            stock.save()

        # Exchange the assets between seller and buyer
        seller.portfolio.stocks.remove(asset)
        buyer.portfolio.stocks.add(asset)

        # Adjust the users' balances
        seller.portfolio.balance += price * amount
        buyer.portfolio.balance -= price * amount
        seller.save()
        buyer.save()

        self.log_transaction(buyer, asset, "BUY", amount, price, simulation_manager)
        self.log_transaction(seller, asset, "SELL", amount, price, simulation_manager)

    def partial_transaction(self, buyer, seller, asset, sell_amount, price, simulation_manager):
        if simulation_manager.simulation_settings.stock_trading_logic == "dynamic":
            stock = Stock.objects.get(ticker=asset.ticker)
            stock.price = price
            stock.save()

        # Exchange the assets between seller and buyer
        seller.portfolio.stocks.remove(asset)
        buyer.portfolio.stocks.add(asset)

        # Adjust the users' balances
        seller.portfolio.balance += price * sell_amount
        buyer.portfolio.balance -= price * sell_amount
        seller.save()
        buyer.save()

        self.log_transaction(buyer, asset, "BUY", sell_amount, price, simulation_manager)
        self.log_transaction(seller, asset, "SELL", sell_amount, price, simulation_manager)

    def log_transaction(self, user, asset, transaction_type, amount, price, simulation_manager):
        order = Order.objects.create(
            user=user,
            stock=asset,
            quantity=amount,
            price=price,
            transaction_type=transaction_type,
        )

        transaction_history, _ = TransactionHistory.objects.get_or_create(
            simulation_manager=simulation_manager
        )
        transaction_history.orders.add(order)


buy_sell_queue = BuySellQueue()
