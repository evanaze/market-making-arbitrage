from collections import Counter, defaultdict
from graph import Graph


class CrossExchangeMarketMaker:
    def __init__(self, logger, graph=Graph()):
        self.graph = graph
        self.logger = logger
        self.threshold = 0.002
        self.threshold_mult = 1/(1 - self.threshold)

    def check_arbitrage(self, correlationId_1, correlationId_2) -> tuple:
        """Check for arbitrage opportunity between two exchanges.
        
        The logic is as such:
        - If the bid price on exchange 1 is (threshold*100)% lower than the bid price on exchange 2, then buy on exchange 1.
            - I.e. if bidExchange_1 <= bidExchange_2/(1-0.002) -> Buy on exchange 1
        - If the ask price on exchange 1 is (threshold*100)% higher than the ask price on exchange 2, then sell on exchange 1.
            - I.e. if askExchange_1 >= askExchange_2/(1-0.002) -> Sell on exchange 1
        """
        # Get the nodes we are checking for arbitrage for
        node_1, node_2 = self.graph[correlationId_1], self.graph[correlationId_2]
        # Buy side logic
        if node_1.bestBidPrice <= node_2.bestBidPrice * self.threshold_mult:
            exchange = node_1.exchange
            self.logger.info(f"Arbitrage opportunity between instrument {correlationId_1} and {correlationId_2}. Submitting a buy order on {exchange}.")
            return (correlationId_1, correlationId_2)
        elif node_2.bestBidPrice <=  node_1.bestBidPrice * self.threshold_mult:
            exchange = node_2.exchange
            self.logger.info(f"Arbitrage opportunity between instrument {correlationId_2} and {correlationId_1}. Submitting a buy order on {exchange}.")
            return (correlationId_2, correlationId_1)
        # Ask side logic
        elif node_1.bestAskPrice >= node_2.bestAskPrice * self.threshold_mult:
            exchange = node_1.exchange
            self.logger.info(f"Arbitrage opportunity between instrument {correlationId_1} and {correlationId_2}. Submitting a sell order on {exchange}.")
            return (correlationId_1, correlationId_2)
        elif node_2.bestAskPrice >= node_1.bestAskPrice * self.threshold_mult:
            exchange = node_2.exchange
            self.logger.info(f"Arbitrage opportunity between instrument {correlationId_2} and {correlationId_1}. Submitting a sell order on {exchange}.")
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