from collections import Counter, defaultdict
from graph import Graph


class CrossExchangeMarketMaker:
    def __init__(self, logger, graph=Graph()):
        self.graph = graph
        self.logger = logger
        self.tolerance = 0.002

    def check_arbitrage(self, correlationId_1, correlationId_2) -> tuple:
        "Check for arbitrage opportunity between two exchanges."
        # Get the nodes we are checking for arbitrage for
        node_1, node_2 = self.graph[correlationId_1], self.graph[correlationId_2]
        # Try to look for arbitrage opportunity
        if node_1.bestBidPrice > (1 + self.tolerance) * node_2.bestBidPrice:
            exchange = node_1.exchange
            self.logger.info(f"Arbitrage opportunity between instrument {correlationId_1} and {correlationId_2}. Submitting a buy order on {exchange}.")
            return (correlationId_1, correlationId_2)
        elif node_2.bestBidPrice > (1 + self.tolerance) * node_1.bestBidPrice:
            exchange = node_2.exchange
            self.logger.info(f"Arbitrage opportunity between instrument {correlationId_2} and {correlationId_1}. Submitting a buy order on {exchange}.")
            return (correlationId_2, correlationId_1)
        else:
            return ()

    def order_book_update(self, correlationId: str, bidPrice: float, bidSize: float, askPrice: float, askSize: float):
        """Update the order book of a given instrument."""
        # Update node
        self.graph.update_node(correlationId, bidPrice, bidSize, askPrice, askSize)
        # Traverse edges checking for arbitrage
        for nodeId, activated in self.graph[correlationId].adjacencyList.items():
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