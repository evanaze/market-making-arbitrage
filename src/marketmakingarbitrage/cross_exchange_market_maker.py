from collections import Counter
from log import logger


class CrossExchangeMarketMaker:
    def __init__(self):
        self.bestBidsPrice = Counter()
        self.bestBidsSize = Counter()
        self.bestAsksPrice = Counter()
        self.bestAsksSize = Counter()

    def check_arbitrage(self):
        "Check for arbitrage opportunity."


    def order_book_update(self, correlationId, bidPrice, bidSize, askPrice, askSize):
        # Update best bids and sizes
        self.bestBidsPrice[correlationId] = bidPrice
        self.bestBidsSize[correlationId] = bidSize
        self.bestAsksPrice[correlationId] = askPrice
        self.bestAsksSize[correlationId] = askSize
        # Update bid ask spread
        self.bidAskSpread = self.bestAsksPrice.subtract(self.bestBidsPrice)
        # Check if we have recieved messages from at least two exchanges
        if len(self.bidAskSpread) == 1:
            logger.info("Not enough info on other order books to check for arbitrage.")
        else:
            # Check for arbitrage opportunity
            self.check_arbitrage()
        self.check_arbitrage()