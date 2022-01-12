"""The base data type."""

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
        return self

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
        print("Node list:", self.node_list)
        self.node_list[correlationId_1].add_edge(correlationId_2)
        self.node_list[correlationId_2].add_edge(correlationId_1)

    def update_node(self, correlationId, bestBidPrice=0, bestBidSize=0, bestAskPrice=0, bestAskSize=0):
        try:
            self.node_list[correlationId].update_node(bestBidPrice, bestBidSize, bestAskPrice, bestAskSize)
        except KeyError:
            print("Making new node")
            self.node_list[correlationId] = Node(correlationId).update_node(bestBidPrice, bestBidSize, bestAskPrice, bestAskSize)