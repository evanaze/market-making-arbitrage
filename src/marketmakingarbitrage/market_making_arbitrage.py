"""The main process script for market making arbitrage."""
import time
import configparser
from event_handler import MyEventHandler
from ccapi import Subscription, Request
from log import logger


class MarketMakingArbitrage(MyEventHandler):
    def __init__(self, duration=None):
        self.logger = logger
        self.config = configparser().ConfigParser()

    def build_graph(self):
        "Creates the graph of instruments."
        # Create subscriptions
        subscriptions = []
        # Coinbase subscription
        #self.subscriptions.append(Subscription('coinbase', 'BTC-USD', 'MARKET_DEPTH', "MARKET_DEPTH_MAX=1", "1"))
        subscriptions.append(Subscription('coinbase', 'BTC-USD', "MARKET_DEPTH,ORDER_UPDATE,PRIVATE_TRADE", "MARKET_DEPTH_MAX=1", "1"))
        self.graph.add_node(exchange="coinbase", pair="BTC-USD", correlationId="1")
        # Kraken subscription
        subscriptions.append(Subscription('kraken', 'XBT/USD', 'MARKET_DEPTH,ORDER_UPDATE,PRIVATE_TRADE', "MARKET_DEPTH_MAX=10", "2"))
        self.graph.add_node(exchange="kraken", pair="BTC-USD", correlationId="2")
        # Subscribe to instruments
        self.subscribe_ws(subscriptions)
        # Add an edge between the instruments
        self.graph.add_edge("1", "2")
    
    def get_account_balances(self):
        """Gets account balances for each of the exchanges."""
        requests = []
        for exchange in self.graph.exchanges:
            if exchange == "coinbase":
                request = Request(Request.Operation_GET_ACCOUNTS, exchange)
                requests.append(request)
            elif exchange == "kraken":
                request = Request(Request.Operation_GET_ACCOUNT_BALANCES, exchange)
                requests.append(request)
        # Query for account balances
        for request in requests:
            self.session.sendRequest(request)

    def market_making_arbitrage(self, duration=None):
        "The main process."
        # Build the graph and make a list of subscriptions
        self.build_graph()
        # Get the initial account balances
        self.get_account_balances()
        # Get initial account balances
        self.get_account_balances()
        # Sleep to allow the program to run
        if duration:
            time.sleep(duration)
        self.session.stop()
        self.logger.info('Bye')

if __name__ == '__main__':
    MarketMakingArbitrage().market_making_arbitrage(600)
