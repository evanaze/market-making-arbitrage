from collections import Counter, defaultdict
from graph import Graph
from log import logger


class CrossExchangeMarketMaker:
    def __init__(self, graph=Graph()):
        self.graph = graph

    def check_arbitrage(self, correlationId_1, correlationId_2) -> tuple:
        "Check for arbitrage opportunity between two exchanges."
        # Check if we have recieved messages from at least two exchanges
        if len(self.graph) == 1:
            logger.info("Not enough info on other order books to check for arbitrage.")
            return ()
        node_1, node_2 = self.graph[correlationId_1], self.graph[correlationId_2]
        if node_1.bestAskPrice > node_2.bestBidPrice:
            logger.info(f"Arbitrage opportunity between instrument {correlationId_1} and {correlationId_2}.")
            return (correlationId_1, correlationId_2)
        elif node_2.bestAskPrice > node_1.bestBidPrice:
            logger.info(f"Arbitrage opportunity between instrument {correlationId_2} and {correlationId_1}.")
            return (correlationId_2, correlationId_1)
        else:
            return ()

    def order_book_update(self, correlationId: str, bidPrice: float, bidSize: float, askPrice: float, askSize: float):
        """Update the order book of a given instrument."""
        # Update node
        self.graph.update_node(correlationId, bidPrice, bidSize, askPrice, askSize)
        # Traverse edges checking for arbitrage
        for nodeId in self.graph[correlationId].adjacency_list:
            # Check for arbitrage opportunity
            self.check_arbitrage(correlationId, nodeId)