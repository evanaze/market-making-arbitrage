"""The base data type."""
from collections import defaultdict
import datetime as dt

class Node:
    "A node on the graph of exchanges and instruments."
    def __init__(self, correlationId=0):
        self.correlationId = correlationId
        self.adjacencyList = defaultdict(int)
        self.lastUpdated = None

    def update_node(self, bestBidPrice, bestBidSize, bestAskPrice, bestAskSize):
        self.bestBidPrice = bestBidPrice
        self.bestBidSize = bestBidSize
        self.bestAskPrice = bestAskPrice
        self.bestAskSize = bestAskSize
        self.lastUpdated = dt.datetime.now(tz=dt.timezone.utc)
        return self

    def add_edge(self, correlationId):
        self.adjacencyList[correlationId]

    def activate_edge(self, correlationId):
        self.adjacencyList[correlationId] = 1

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

    def update_node(self, correlationId, bestBidPrice=None, bestBidSize=None, bestAskPrice=None, bestAskSize=None):
        try:
            self.node_list[correlationId].update_node(bestBidPrice, bestBidSize, bestAskPrice, bestAskSize)
        except KeyError:
            self.node_list[correlationId] = Node(correlationId).update_node(bestBidPrice, bestBidSize, bestAskPrice, bestAskSize)