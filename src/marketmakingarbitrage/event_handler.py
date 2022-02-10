"""Handles events as they come from the session."""
import configparser
from decimal import Decimal
from ccapi import EventHandler, Session, Event, Message, RequestList, Request, SessionOptions, SessionConfigs
from log import logger

class MyEventHandler(EventHandler):
    def __init__(self):
        super().__init__()
        self.logger = logger
        self.openOrders = {}
        self.balances = {}
        self.config = configparser().ConfigParser()
        self.sessionOption = SessionOptions()
        self.sessionConfig = SessionConfigs()

    def send_request(self, requestList):
        for request in requestList:
            self.logger.info(f"sending request: {request.toString()}")
        self.session.sendRequest(requestList)

    def process_ob_update(self):
        """Parses the elements from the message."""
        # Iterate through the list of elements
        for element in self.message.getElementList():
            elementNameValueMap = element.getNameValueMap()
            # Parse bid and ask prices and sizes
            for name, value in elementNameValueMap.items():
                if name == "BID_PRICE":
                    bidPrice = float(value)
                elif name == "BID_SIZE":
                    bidSize = float(value) 
                elif name == "ASK_PRICE":
                    askPrice = float(value)
                else:
                    askSize = float(value)
        return bidPrice, bidSize, askPrice, askSize
    
    def process_open_orders(self):
        # TODO fix this
        requestList = RequestList()
        for element in self.message.getElementList():
            elementNameValueMap = element.getNameValueMap()
            pair = self.altnameToPair[elementNameValueMap["INSTRUMENT"]]
            clientOrderId = elementNameValueMap["CLIENT_ORDER_ID"]
            found = False
            for _, v1 in self.openOrders[pair].items():
                for _, v2 in v1.items():
                    if clientOrderId == v2["clientOrderId"]:
                        found = True
            if not found:
                side = elementNameValueMap["SIDE"]
                orderPrice = Decimal(elementNameValueMap["LIMIT_PRICE"])
                self.openOrders[pair]["b" if side == "BUY" else "s"][orderPrice] = {
                    "quantity": elementNameValueMap["QUANTITY"],
                    "clientOrderId": elementNameValueMap["CLIENT_ORDER_ID"],
                }
        self.logger.debug(f"self.openOrders = {self.openOrders}")
        self.logger.info("Get account balances")
        requestList = RequestList()
        request = Request(Request.Operation_GET_ACCOUNT_BALANCES, "kraken")
        requestList.append(request)
        self.send_request(self.session, requestList)

    def process_account_balances(self):
        """Parses account balances."""
        # TODO fix this
        for element in self.message.getElementList():
            elementNameValueMap = element.getNameValueMap()
            self.logger.info("Asset:", elementNameValueMap["ASSET"])
            self.balances[elementNameValueMap["ASSET"]] = float(elementNameValueMap["QUANTITY_AVAILABLE_FOR_TRADING"])
        self.logger.debug(f"self.balances = {self.balances}")
        self.logger.debug(f"self.openOrders = {self.openOrders}")
        for pair, v1 in self.openOrders.items():
            for s, v2 in v1.items():
                for orderPrice, v3 in v2.items():
                    if s == "b":
                        self.balances[self.pairs["kraken"][pair]["quoteAsset"]] -= float(orderPrice) * float(v3["quantity"])
                    else:
                        self.balances[self.pairs["kraken"][pair]["baseAsset"]] -= float(v3["quantity"])
        self.logger.debug(f"self.balances = {self.balances}")
        self.ready = True

    def processEvent(self, event: Event, session: Session) -> bool:
        # TODO: Add message parsing for order execution
        if event.getType() == Event.Type_SUBSCRIPTION_DATA:
            for self.message in event.getMessageList():
                # Get the correlation ID from the message.
                correlationId = self.message.getCorrelationIdList()[0]
                # Parse the elements from the message
                self.process_ob_update()
                # Update the order book for the node
                self.crossExchMM.order_book_update(correlationId, self.bidPrice, self.bidSize, self.askPrice, self.askSize)
                # Check for an arbitrage opportunity
                opportunity = self.crossExchMM.check_arbitrage()
                # Submit the order
                # if oppportunity:
                #    session.sendRequest(order)
        elif event.getType() == Event.Type_RESPONSE:
            for self.message in event.getMessageList():
                messageType = self.message.getType()
                if messageType == Message.Type_GET_ACCOUNT_BALANCES:
                    self.process_account_balances()
                elif messageType == Message.Type_GET_OPEN_ORDERS:
                    self.process_open_orders()
                elif messageType == Message.Type_RESPONSE_ERROR:
                    self.logger.error(event.toStringPretty())
        return True  # This line is needed.

