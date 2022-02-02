"""Handles orders."""
from ccapi import Request
from graph import Node

class OrderHandler:
    def __init__(self, logger, account_balances):
        self.logger = logger
        self.account_balances = account_balances

    def submit_order(self, node: Node, account_balances: dict, price: float, buy: bool, quantity=None) -> Request:
        """Submit the order."""
        if buy:
            self.logger.info(f"Submitting buy order on {node.exchange} for {quantity} {node.quote} at {price} {node.base}.")
            request = Request(Request.Operation_CREATE_ORDER, node.exchange, node.pair)
            request.appendParam({
                'SIDE':'BUY',
                'QUANTITY':quantity,
                'LIMIT_PRICE':price,
            })
        else:
            self.logger.info(f"Submitting sell order on {node.exchange} for {quantity} {node.quote} at {node.offer} {node.base}.")
            request = Request(Request.Operation_CREATE_ORDER, node.exchange, node.pair)
            request.appendParam({
                'SIDE':'SELL',
                'QUANTITY':quantity,
                'LIMIT_PRICE':price,
            })
        # Update the node for the submitted order
        node.new_order()
        # Return the request to submit
        return request