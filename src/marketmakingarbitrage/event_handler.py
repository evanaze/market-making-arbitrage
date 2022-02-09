"""Handles events as they come from the session."""
from ccapi import EventHandler, Session, Subscription, Event


class MyEventHandler(EventHandler):
    def __init__(self, logger, crossExchMM):
        super().__init__()
        self.logger = logger
        self.crossExchMM = crossExchMM

    def parse_ob_update(self):
        """Parses the elements from the message."""
        # Iterate through the list of elements
        for element in self.message.getElementList():
            elementNameValueMap = element.getNameValueMap()
            # Parse bid and ask prices and sizes
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
        print("Received an event:\n" + event.toStringPretty(2, 2))
        # TODO: Add message parsing for order execution
        if event.getType() == Event.Type_SUBSCRIPTION_DATA:
            for self.message in event.getMessageList():
                # Get the correlation ID from the message.
                correlationId = self.message.getCorrelationIdList()[0]
                # Parse the elements from the message
                self.parse_ob_update()
                # Update the order book for the node
                self.crossExchMM.order_book_update(correlationId, self.bidPrice, self.bidSize, self.askPrice, self.askSize)
                # Check for an arbitrage opportunity
                opportunity = self.crossExchMM.check_arbitrage()
                # Submit the order
                # if oppportunity:
                #    session.sendRequest(order)
        if event.getType() != Event.Type_SUBSCRIPTION_DATA:
            print("Received a non-subscription event:\n" + event.toStringPretty(2, 2))
        return True  # This line is needed.