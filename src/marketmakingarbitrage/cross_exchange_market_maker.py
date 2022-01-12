from collections import Counter, defaultdict
from log import logger


class Node:
    "A node on the graph of exchanges and instruments."
    def __init__(self, correlationId=0):
        self.correlationId = correlationId
        self.adjacency_list = set()

    def update_node(self, bestBidPrice, bestBidSize, bestAskPrice, bestAskSize):
        self.bestBidPrice = bestBidPrice
        self.bestBidSize = bestBidSize
        self.bestAskPrice = bestAskPrice
        self.bestAskSize = bestAskSize

    def add_edge(self, correlationId):
        self.adjacency_list.add(correlationId)

class Graph:
    def __init__(self):
        self.node_list = {}

    def __len__(self):
        return len(self.node_list)

    def __getitem__(self, correlationId):
        return self.node_list[correlationId]

    def add_edge(self, correlationId_1, correlationId_2):
        self.node_list[correlationId_1].add_edge(correlationId_2)
        self.node_list[correlationId_2].add_edge(correlationId_1)

    def update_node(self, correlationId, bestBidPrice, bestBidSize, bestAskPrice, bestAskSize):
        try:
            self.node_list[correlationId].update_node(bestBidPrice, bestBidSize, bestAskPrice, bestAskSize)
        except KeyError:
            self.node_list[correlationId] = Node(correlationId).update_node(bestBidPrice, bestBidSize, bestAskPrice, bestAskSize)


class CrossExchangeMarketMaker:
    def __init__(self):
        self.graph = Graph()

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
        # Check for arbitrage opportunity
        self.check_arbitrage()