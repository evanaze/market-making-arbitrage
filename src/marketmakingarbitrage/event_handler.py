from ccapi import EventHandler, Session, Subscription, Event
from cross_exchange_market_maker import CrossExchangeMarketMaker


class MyEventHandler(EventHandler):
    def __init__(self, logger, crossExchMM=CrossExchangeMarketMaker()):
        super().__init__()
        self.logger = logger
        self.crossExchMM = crossExchMM

    def parse_element(self):
        elementNameValueMap = self.element.getNameValueMap()
        for name, value in elementNameValueMap.items():
            if name == "BID_PRICE":
                self.bidPrice = float(value)
            elif name == "BID_SIZE":
                self.bidSize = float(value) 
            elif name == "ASK_PRICE":
                self.askPrice = float(value)
            else:
                self.askSize = float(value)

    def processEvent(self, event: Event, session: Session) -> bool:
        if event.getType() == Event.Type_SUBSCRIPTION_DATA:
            for message in event.getMessageList():
                # Get the correlation ID from the message.
                correlationId = message.getCorrelationIdList()[0]
                # Parse the elements from the message
                for self.element in message.getElementList():
                    # Parse the element
                    self.parse_element()
                # Log the data to the log file
                self.logger.debug(f"CID: {correlationId}, BB: {self.bidPrice}, BA: {self.askPrice}")
                # Update the order book for the node
                self.crossExchMM.order_book_update(correlationId, self.bidPrice, self.bidSize, self.askPrice, self.askSize)
        return True  # This line is needed.