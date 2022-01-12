from ccapi import EventHandler, Session, Subscription, Event
from cross_exchange_market_maker import CrossExchangeMarketMaker


class MyEventHandler(EventHandler):
    def __init__(self, crossExchMM=CrossExchangeMarketMaker()):
        super().__init__()
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
                correlationId = message.getCorrelationIdList()[0]
                for self.element in message.getElementList():
                    self.parse_element()
                    try:
                        self.crossExchMM.order_book_update(correlationId, self.bidPrice, self.bidSize, self.askPrice, self.askSize)
                    except Exception as e:
                        print(e)
        return True  # This line is needed.