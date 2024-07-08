from collections import deque
from django.db import transaction
from django.utils import timezone
from simulation.models import TransactionHistory

class BuySellQueue:
    def __init__(self):
        self.buy_queue = deque()
        self.sell_queue = deque()

    def add_to_buy_queue(self, user, asset, amount, price):
        self.buy_queue.append((user, asset, amount, price))

    def add_to_sell_queue(self, user, asset, amount, price):
        self.sell_queue.append((user, asset, amount, price))

    def process_queues(self):
        transactions = []
        while self.buy_queue and self.sell_queue:
            buy_order = self.buy_queue.popleft()
            sell_order = self.sell_queue.popleft()

            if buy_order[3] >= sell_order[3]:  # Buy price >= Sell price
                matched_price = (buy_order[3] + sell_order[3]) / 2
                transactions.append(self.execute_transaction(buy_order, sell_order, matched_price))
        return transactions

    @transaction.atomic
    def execute_transaction(self, buy_order, sell_order, price):
        buyer, asset, amount, buy_price = buy_order
        seller, _, sell_amount, sell_price = sell_order

        if sell_amount >= amount:
            self.complete_transaction(buyer, seller, asset, amount, price)
            if sell_amount > amount:
                self.add_to_sell_queue(seller, asset, sell_amount - amount, sell_price)
        else:
            self.partial_transaction(buyer, seller, asset, sell_amount, price)
            self.add_to_buy_queue(buyer, asset, amount - sell_amount, buy_price)

        return {
            'buyer': buyer.user.username,
            'seller': seller.user.username,
            'asset': asset.name,
            'amount': amount,
            'price': price,
            'timestamp': timezone.now().isoformat()
        }

    def complete_transaction(self, buyer, seller, asset, amount, price):
        seller.portfolio.stocks.remove(asset)
        buyer.portfolio.stocks.add(asset)
        seller.balance += price * amount
        buyer.balance -= price * amount
        seller.save()
        buyer.save()
        self.log_transaction(buyer, asset, 'buy', amount, price)
        self.log_transaction(seller, asset, 'sell', amount, price)

    def partial_transaction(self, buyer, seller, asset, sell_amount, price):
        seller.portfolio.stocks.remove(asset)
        buyer.portfolio.stocks.add(asset)
        seller.balance += price * sell_amount
        buyer.balance -= price * sell_amount
        seller.save()
        buyer.save()
        self.log_transaction(buyer, asset, 'buy', sell_amount, price)
        self.log_transaction(seller, asset, 'sell', sell_amount, price)

    def log_transaction(self, user, asset, transaction_type, amount, price):
        TransactionHistory.objects.create(
            portfolio=user.portfolio,
            asset=asset.name,
            transaction_type=transaction_type,
            amount=amount,
            price=price
        )

# buy_sell_queue = BuySellQueue()