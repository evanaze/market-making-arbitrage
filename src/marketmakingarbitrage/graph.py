"""The base data type."""
from collections import defaultdict
import datetime as dt

class Node:
    "A node on the graph of exchanges and instruments."
    def __init__(self, exchange: str, pair: str, correlationId=0, suppress_duration=600):
        self.pair = pair
        self.exchange = exchange
        self.lastUpdated = None
        self.correlationId = correlationId
        self.adjacencyList = defaultdict(int)
        self.suppress_orders_flag = False
        self.suppress_duration = suppress_duration

    def update_node(self, bestBidPrice: float, bestBidSize: float, bestAskPrice: float, bestAskSize: float):
        """Update the information on a node."""
        # Update the order book details
        self.bestBidPrice = bestBidPrice
        self.bestBidSize = bestBidSize
        self.bestAskPrice = bestAskPrice
        self.bestAskSize = bestAskSize
        # Record the current time as last time updated
        self.lastUpdated = dt.datetime.now(tz=dt.timezone.utc)
        return self

    def add_edge(self, correlationId: str):
        """Add a new deactivated edge to the adjacency list."""
        self.adjacencyList[correlationId]

    def activate_edge(self, correlationId: str):
        """Activate the edge between two nodes on the adjacency list."""
        self.adjacencyList[correlationId] = 1

    def new_order(self):
        """Updates the node status for a new order"""
        self.suppress_orders()

    def suppress_orders(self):
        """Suppresses future orders for the specified duration."""
        self.reactivate_orders_timestamp = dt.datetime.now(tz=dt.timezone.utc) + dt.timedelta(seconds=self.suppress_duration)
        self.suppress_orders_flag = True

    def check_order_suppression(self) -> bool:
        """Checks whether we can submit a new order."""
        if not self.suppress_orders_flag:
            return True
        elif dt.datetime.now(tz=dt.timezone.utc) < self.reactivate_orders_timestamp:
            return False 
        else:
            self.suppress_orders_flag = False 
            return True

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
        node = self.node_list[correlationId]
        return node.update_node(bestBidPrice, bestBidSize, bestAskPrice, bestAskSize)