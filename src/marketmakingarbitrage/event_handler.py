from ccapi import EventHandler, Session, Subscription, Event
from cross_exchange_market_maker import CrossExchangeMarketMaker


class MyEventHandler(EventHandler):
    def __init__(self):
        super().__init__()
        #self.crossExchMM = CrossExchangeMarketMaker()

    def parse_element(self):
        elementNameValueMap = self.element.getNameValueMap()
        for name, value in elementNameValueMap.items():
            if name == "BID_PRICE":
                self.bidPrice = value
            elif name == "BID_SIZE":
                self.bidSize = value 
            elif name == "ASK_PRICE":
                self.askPrice = value
            else:
                self.askSize = value

    def processEvent(self, event: Event, session: Session) -> bool:
        if event.getType() == Event.Type_SUBSCRIPTION_DATA:
            for message in event.getMessageList():
                correlationId = message.getCorrelationIdList()[0]
                for self.element in message.getElementList():
                    self.parse_element()
                    #self.crossExchMM.order_book_update(correlationId, self.bidPrice, 
                    # self.bidSize, self.askPrice, self.askSize)
        return True  # This line is needed.