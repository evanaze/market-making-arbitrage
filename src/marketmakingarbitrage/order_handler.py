"""Handles orders."""
from ccapi import Request
from graph import Node

class OrderHandler:
    def __init__(self, logger):
        self.logger = logger

    def get_base_quote(self):
        """Gets the base/quote pair for the inputted pair and the exchange."""
        if self.exchange in ["coinbase", "kraken"]:
            pair_split = self.pair.split("-")
            self.quote, self.base = pair_split[0], pair_split[1]

    def submit_order(self, node: Node, quantity: float, price: float, buy: bool) -> None:
        """Submit the order."""
        self.pair = node.pair 
        self.exchange = node.exchange
        # Get the base and quote for the pair
        self.get_base_quote()
        if buy:
            self.logger.info(f"Submitting buy order on {self.exchange} for {quantity} {self.quote} at {price} {self.base}.")
            request = Request(Request.Operation_CREATE_ORDER, self.exchange, self.pair)
            request.appendParam({
                'SIDE':'BUY',
                'QUANTITY':quantity,
                'LIMIT_PRICE':price,
            })
        else:
            self.logger.info(f"Submitting sell order on {self.exchange} for {quantity} {self.quote} at {self.offer} {self.base}.")
        # Update the node for the submitted order
        node.new_order()