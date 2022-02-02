import time
from ccapi import SessionOptions, SessionConfigs, Session, Subscription, Request

from graph import Graph
from event_handler import MyEventHandler
from cross_exchange_market_maker import CrossExchangeMarketMaker
from log import logger


class MarketMakingArbitrage:
    def __init__(self, duration=None):
        self.logger = logger
        self.graph = Graph()
        self.option = SessionOptions()
        self.config = SessionConfigs()

    def build_graph(self):
        "Creates the graph of instruments."
        # Create subscriptions
        self.subscriptions = []
        # Coinbase subscription
        #self.subscriptions.append(Subscription('coinbase', 'BTC-USD', 'MARKET_DEPTH', "MARKET_DEPTH_MAX=1", "1"))
        self.subscriptions.append(Subscription('coinbase', 'BTC-USD', "MARKET_DEPTH,ORDER_UPDATE,PRIVATE_TRADE", "MARKET_DEPTH_MAX=1", "1"))
        self.graph.add_node(exchange="coinbase", pair="BTC-USD", correlationId="1")
        # Kraken subscription
        self.subscriptions.append(Subscription('kraken', 'XBT/USD', 'MARKET_DEPTH,ORDER_UPDATE,PRIVATE_TRADE', "MARKET_DEPTH_MAX=10", "2"))
        self.graph.add_node(exchange="kraken", pair="BTC-USD", correlationId="2")
        # Add an edge between the instruments
        self.graph.add_edge("1", "2")
    
    def get_account_balances(self):
        """Gets account balances for each of the exchanges."""
        requests = []
        for exchange in self.graph.exchanges:
            if exchange == "coinbase":
                request = Request(Request.Operation_GET_ACCOUNTS)
                requests.append(request)
            elif exchange == "kraken":
                request = Request(Request.Operation_GET_ACCOUNT_BALANCES)
                requests.append(request)
        # Query for account balances
        self.session.sendRequest()

    def market_making_arbitrage(self, duration=None):
        "The main process."
        # Build the graph and make a list of subscriptions
        self.build_graph()
        # Get the initial account balances
        # Make the market making object
        CrossExchMM = CrossExchangeMarketMaker(logger=self.logger, graph=self.graph)
        # Make the event handler
        eventHandler = MyEventHandler(logger=self.logger, crossExchMM=CrossExchMM)
        # Make the session
        self.session = Session(self.option, self.config, eventHandler)
        # Get initial account balances
        self.get_account_balances()
        # Subscribe to instruments
        for subscription in self.subscriptions:
            self.session.subscribe(subscription)
        # Sleep to allow the program to run
        if duration:
            time.sleep(duration)
        self.session.stop()
        self.logger.info('Bye')

if __name__ == '__main__':
    MarketMakingArbitrage().market_making_arbitrage(600)
