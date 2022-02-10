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
        # Get the base and quote of the node
        if self.exchange in ["coinbase", "kraken"]:
            pair_split = self.pair.split("-")
            self.quote, self.base = pair_split[0], pair_split[1]
        
    def update(self, bestBidPrice: float, bestBidSize: float, bestAskPrice: float, bestAskSize: float):
        """Update the information on a node."""
        # Update the order book details
        self.bestBidPrice = bestBidPrice
        self.bestBidSize = bestBidSize
        self.bestAskPrice = bestAskPrice
        self.bestAskSize = bestAskSize
        # Record the current time as last time updated
        self.lastUpdated = dt.datetime.now(tz=dt.timezone.utc)
        return self

    def add_edge_to_node(self, correlationId: str):
        """Add a new deactivated edge to the adjacency list."""
        self.adjacencyList[correlationId]

    def activate_edge_node(self, correlationId: str):
        """Activate the edge between two nodes on the adjacency list."""
        self.adjacencyList[correlationId] = 1

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
        self.nodeList = defaultdict(Node)
        self.exchanges = set()

    def __len__(self):
        return len(self.nodeList)

    def __getitem__(self, correlationId):
        return self.nodeList[correlationId]

    def add_node(self, correlationId, exchange, pair):
        self.nodeList[correlationId] = Node(exchange=exchange, pair=pair, correlationId=correlationId)
        self.exchanges.add(exchange)

    def add_edge(self, correlationId_1, correlationId_2):
        """Adds a deactivated edge between two nodes."""
        self.nodeList[correlationId_1].add_edge_to_node(correlationId_2)
        self.nodeList[correlationId_2].add_edge_to_node(correlationId_1)

    def activate_edge(self, correlationId_1, correlationId_2):
        """Activates an edge between two nodes."""
        self.nodeList[correlationId_1].activate_edge_node(correlationId_2)
        self.nodeList[correlationId_2].activate_edge_node(correlationId_1)

    def update_node(self, correlationId, bestBidPrice=None, bestBidSize=None, bestAskPrice=None, bestAskSize=None):
        """Updates the node with the new information."""
        return self.nodeList[correlationId].update(bestBidPrice, bestBidSize, bestAskPrice, bestAskSize)