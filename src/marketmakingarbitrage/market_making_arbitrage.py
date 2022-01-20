import time
from ccapi import SessionOptions, SessionConfigs, Session, Subscription

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
        self.subscriptions.append(Subscription('coinbase', 'BTC-USD', 'MARKET_DEPTH', "MARKET_DEPTH_MAX=1", "1"))
        self.graph.add_node(exchange="coinbase", pair="BTC-USD", correlationId="1")
        # Kraken subscription
        self.subscriptions.append(Subscription('kraken', 'XBT/USD', 'MARKET_DEPTH', "MARKET_DEPTH_MAX=10", "2"))
        self.graph.add_node(exchange="kraken", pair="BTC-USD", correlationId="2")
        # Add an edge between the instruments
        self.graph.add_edge("1", "2")

    def market_making_arbitrage(self, duration=None):
        "The main process."
        # Make a list of subscriptions
        self.build_graph()
        # Make the market making object
        CrossExchMM = CrossExchangeMarketMaker(logger=self.logger, graph=self.graph)
        # Make the event handler
        eventHandler = MyEventHandler(logger=self.logger, crossExchMM=CrossExchMM)
        # Make the session
        session = Session(self.option, self.config, eventHandler)
        # Subscribe to instruments
        for subscription in self.subscriptions:
            session.subscribe(subscription)
        # Sleep to allow the program to run
        if duration:
            time.sleep(duration)
        session.stop()
        self.logger.info('Bye')

if __name__ == '__main__':
    MarketMakingArbitrage().market_making_arbitrage(60)
