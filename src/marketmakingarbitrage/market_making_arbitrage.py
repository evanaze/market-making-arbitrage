import time
from ccapi import SessionOptions, SessionConfigs, Session, Subscription

from cross_exchange_market_maker import CrossExchangeMarketMaker
from event_handler import MyEventHandler
from graph import Graph
from log import logger


class MarketMakingArbitrage:
    def __init__(self):
        self.option = SessionOptions()
        self.config = SessionConfigs()
        self.logger = logger

    def make_subscriptions(self):
        "Creates the graph of instruments."
        # Create subscriptions
        self.subscriptions = []
        # Create the graph 
        self.graph = Graph()
        # Coinbase subscription
        self.graph.update_node("1")
        self.subscriptions.append(Subscription('coinbase', 'BTC-USD', 'MARKET_DEPTH', "MARKET_DEPTH_MAX=1", "1"))
        # Kraken subscription
        self.graph.update_node("2")
        self.subscriptions.append(Subscription('kraken', 'XXBTZUSD', 'MARKET_DEPTH', "MARKET_DEPTH_MAX=10", "2"))
        self.graph.add_edge("1", "2")

    def market_making_arbitrage(self):
        "The main process."
        # Make a list of subscriptions
        self.make_subscriptions()
        # Make the cross exchange market maker
        self.crossExchangeMarketMaker = CrossExchangeMarketMaker(self.graph)
        # Make the event handler
        eventHandler = MyEventHandler(self.crossExchangeMarketMaker)
        # Make the session
        session = Session(self.option, self.config, eventHandler)
        for subscription in self.subscriptions:
            session.subscribe(subscription)
        time.sleep(10)
        session.stop()
        self.logger.info('Bye')

if __name__ == '__main__':
    MarketMakingArbitrage().market_making_arbitrage()
