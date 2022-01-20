"""Handles orders."""
from graph import Node

class OrderHandler:
    def __init__(self, logger):
        self.logger = logger

    def submit_order(self, node: Node, quantity: float, offer: float, buy: bool) -> None:
        """Submit the order."""
        exchange = node.exchange
        pair = node.pair 
        pair_split = pair.split("/")
        base, quote = pair_split[0], pair_split[1]
        if buy:
            self.logger.info(f"Submitting buy order on {exchange} for {quantity} {quote} at {offer} {base}.")
        else:
            self.logger.info(f"Submitting sell order on {exchange} for {quantity} {quote} at {offer} {base}.")