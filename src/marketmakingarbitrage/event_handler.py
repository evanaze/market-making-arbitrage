from ccapi import EventHandler, Session, Subscription, Event


class MyEventHandler(EventHandler):
    def __init__(self, logger, crossExchMM):
        super().__init__()
        self.logger = logger
        self.crossExchMM = crossExchMM

    def parse_element(self):
        """Parses the elements from the message."""
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
                    # TODO: Add message parsing for order execution
                    # Parse the element
                    self.parse_element()
                # Update the order book for the node
                self.crossExchMM.order_book_update(correlationId, self.bidPrice, self.bidSize, self.askPrice, self.askSize)
                # Check for an arbitrage opportunity
                order = self.crossExchMM.check_arbitrage()
                # Submit the order
                # if order:
                #    session.sendRequest(order)
        return True  # This line is needed.