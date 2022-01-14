"""The base data type."""
from collections import defaultdict
import datetime as dt

class Node:
    "A node on the graph of exchanges and instruments."
    def __init__(self, exchange, pair, correlationId=0):
        self.lastUpdated = None
        self.pair = pair
        self.exchange = exchange
        self.correlationId = correlationId
        self.adjacencyList = defaultdict(int)

    def update_node(self, bestBidPrice, bestBidSize, bestAskPrice, bestAskSize):
        """Update the information on a node."""
        # Update the order book details
        self.bestBidPrice = bestBidPrice
        self.bestBidSize = bestBidSize
        self.bestAskPrice = bestAskPrice
        self.bestAskSize = bestAskSize
        # Record the current time as last time updated
        self.lastUpdated = dt.datetime.now(tz=dt.timezone.utc)
        return self

    def add_edge(self, correlationId):
        """Add a new deactivated edge to the adjacency list."""
        self.adjacencyList[correlationId]

    def activate_edge(self, correlationId):
        """Activate the edge between two nodes on the adjacency list."""
        self.adjacencyList[correlationId] = 1

class Graph:
    """A graph of instruments on exchanges and possible trade pairs."""
    def __init__(self):
        self.node_list = defaultdict(Node)

    def __len__(self):
        return len(self.node_list)

    def __getitem__(self, correlationId):
        return self.node_list[correlationId]

    def add_node(self, correlationId, exchange, pair):
        self.node_list[correlationId] = Node(exchange=exchange, pair=pair, correlationId=correlationId)

    def add_edge(self, correlationId_1, correlationId_2):
        """Adds a deactivated edge between two nodes."""
        self.node_list[correlationId_1].add_edge(correlationId_2)
        self.node_list[correlationId_2].add_edge(correlationId_1)

    def activate_edge(self, correlationId_1, correlationId_2):
        """Activates an edge between two nodes."""
        self.node_list[correlationId_1].activate_edge(correlationId_2)
        self.node_list[correlationId_2].activate_edge(correlationId_1)

    def update_node(self, correlationId, bestBidPrice=None, bestBidSize=None, bestAskPrice=None, bestAskSize=None):
        """Updates the node with the new information."""
        self.node_list[correlationId].update_node(bestBidPrice, bestBidSize, bestAskPrice, bestAskSize)