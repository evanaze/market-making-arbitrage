import os
from collections import Counter, defaultdict
from graph import Graph
from order_handler import OrderHandler


class CrossExchangeMarketMaker:
    def __init__(self, logger, graph=Graph()):
        self.graph = graph
        self.logger = logger
        self.threshold = 0.002
        self.ub = 1 + self.threshold
        self.lb = 1 - self.threshold
        self.orderHandler = OrderHandler(logger)
        self.suppress_orders = False
        self.logger.info(f"Paper trade: {os.getenv('PAPER_TRADE')}")

    def check_arbitrage(self, correlationId_1: str, correlationId_2: str) -> None:
        """Check for arbitrage opportunity between two exchanges.
        
        The logic is as such:
        - If the bid price on exchange 1 is (threshold*100)% lower than the bid price on exchange 2, then buy on exchange 1.
            - I.e. if bidExchange_1 <= bidExchange_2/(1-0.002) -> Buy on exchange 1
        - If the ask price on exchange 1 is (threshold*100)% higher than the ask price on exchange 2, then sell on exchange 1.
            - I.e. if askExchange_1 >= askExchange_2/(1-0.002) -> Sell on exchange 1
        """
        # Get the nodes we are checking for arbitrage for
        node_1, node_2 = self.graph[correlationId_1], self.graph[correlationId_2]
        buy_arb_opportunity = abs(node_1.bestBidPrice - node_2.bestBidPrice) - self.threshold
        ask_arb_opportunity = abs(node_1.bestAskPrice - node_2.bestAskPrice) - self.threshold
        # Buy side logic
        if node_1.bestBidPrice / node_2.bestBidPrice <= self.lb:
            self.logger.info(f"Buy side arbitrage opportunity for pair {node_1.pair} between exchange {node_1.exchange} and {node_2.exchange}.")
            self.logger.debug(f"{node_1.exchange} best bid: {node_1.bestBidPrice}, {node_2.exchange} best bid: {node_2.bestBidPrice}. Possible arbitrage={buy_arb_opportunity}.")
            self.orderHandler.submit_order(node=node_1, quantity=0, offer=node_1.bestBidPrice, buy=True)
        elif node_1.bestBidPrice / node_2.bestBidPrice >= self.ub:
            self.logger.info(f"Buy side arbitrage opportunity for pair {node_1.pair} between exchange {node_2.exchange} and {node_1.exchange}.")
            self.logger.debug(f"{node_2.exchange} best bid: {node_2.bestBidPrice}, {node_1.exchange} best bid: {node_1.bestBidPrice}. Possible arbitrage={buy_arb_opportunity}.")
            self.orderHandler.submit_order(node=node_2, quantity=0, offer=node_2.bestBidPrice, buy=True)
        # Ask side logic
        elif node_1.bestAskPrice / node_2.bestAskPrice >= self.ub:
            self.logger.info(f"Sell side arbitrage opportunity for pair {node_1.pair} between exchange {node_1.exchange} and {node_2.exchange}.")
            self.logger.debug(f"{node_1.exchange} best ask: {node_1.bestAskPrice}, {node_2.exchange} best ask: {node_2.bestAskPrice}. Possible arbitrage={ask_arb_opportunity}.")
            self.orderHandler.submit_order(node=node_1, quantity=0, offer=node_1.bestAskPrice, buy=False)
        elif node_1.bestAskPrice / node_2.bestAskPrice <= self.lb:
            self.logger.info(f"Sell side arbitrage opportunity for pair {node_1.pair} between exchange {node_2.exchange} and {node_1.exchange}.")
            self.logger.debug(f"{node_2.exchange} best ask: {node_2.bestAskPrice}, {node_1.exchange} best ask: {node_1.bestAskPrice}. Possible arbitrage={ask_arb_opportunity}.")
            self.orderHandler.submit_order(node=node_2, quantity=0, offer=node_2.bestAskPrice, buy=False)

    def order_book_update(self, correlationId: str, bidPrice: float, bidSize: float, askPrice: float, askSize: float):
        """Update the order book of a given instrument."""
        # Update node
        node = self.graph[correlationId].update_node(bidPrice, bidSize, askPrice, askSize)
        # Log the data to the log file
        self.logger.debug(f"Order book update for {node.pair} on {node.exchange}. BB: {bidPrice}, BA: {askPrice}")
        # Traverse edges checking for arbitrage
        for nodeId, activated in node.adjacencyList.items():
            # Check if the edge is activated
            if not activated:    
                # If the other node has been updated but we haven't activated the edge yet
                if not self.graph[nodeId].lastUpdated:
                    self.logger.info("Edge not active yet.")
                    continue
                else:
                    # Activate the edge
                    self.logger.info(f"Activating edge between nodes {correlationId} and {nodeId}.")
                    self.graph.activate_edge(correlationId, nodeId)
            # Check for arbitrage opportunity
            self.check_arbitrage(correlationId, nodeId)