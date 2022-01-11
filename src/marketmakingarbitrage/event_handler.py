from ccapi import EventHandler, Session, Subscription, Event
from cross_exchange_market_maker import CrossExchangeMarketMaker

class MyEventHandler(EventHandler):
    def __init__(self):
        super().__init__()
        self.crossExchMM = CrossExchangeMarketMaker()

    def processEvent(self, event: Event, session: Session) -> bool:
        if event.getType() == Event.Type_SUBSCRIPTION_DATA:
            for message in event.getMessageList():
                correlationId = message.getCorrelationIdList()[0]
                for element in message.getElementList():
                    print(event.toStringPretty())
                    elementNameValueMap = element.getNameValueMap()
                    for name, value in elementNameValueMap.items():
                        if name == "BID_PRICE":
                            bidPrice = value
                        elif name == "BID_SIZE":
                            bidSize = value 
                        elif name == "ASK_PRICE":
                            askPrice = value
                        else:
                            askSize = value
                        self.crossExchMM.order_book_update(correlationId, bidPrice, bidSize, askPrice, askSize)
        return True  # This line is needed.