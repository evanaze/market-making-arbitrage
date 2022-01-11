import time
from ccapi import SessionOptions, SessionConfigs, Session, Subscription
from event_handler import MyEventHandler
from log import logger


def market_making_arbitrage():
    "The main process."
    cb_subscription = Subscription('coinbase', 'BTC-USD', 'MARKET_DEPTH', "MARKET_DEPTH_MAX=1", "1")
    kr_subscription = Subscription('kraken', 'XXBTZUSD', 'MARKET_DEPTH', "MARKET_DEPTH_MAX=10", "2")
    eventHandler = MyEventHandler()
    option = SessionOptions()
    config = SessionConfigs()
    session = Session(option, config, eventHandler)
    session.subscribe(cb_subscription)
    session.subscribe(kr_subscription)
    time.sleep(10)
    session.stop()
    logger.info('Bye')

if __name__ == '__main__':
    market_making_arbitrage()
