"""The object that performs the logic of the """
import os
from graph import Graph, Node
from marketmakingarbitrage.market_making_arbitrage import MarketMakingArbitrage
from order_handler import OrderHandler


class CrossExchangeMarketMaker(MarketMakingArbitrage):
    def __init__(self):
        super.__init__()
        self.threshold = self.config["Trading Parameters"]["Threshold"]
        self.ub = 1 + self.threshold
        self.lb = 1 - self.threshold
        self.orderHandler = OrderHandler()
        self.liveTrade = self.config["Default"].getboolean('PaperTrade', fallback=True)

    def check_arbitrage(self, node_1: Node, node_2: Node) -> tuple:
        """Check for arbitrage opportunity between two exchanges.
        
        The logic is as such:
        - If the bid price on exchange 1 is (threshold*100)% lower than the bid price on exchange 2, then buy on exchange 1.
            - I.e. if bidExchange_1 <= bidExchange_2/(1-0.002) -> Buy on exchange 1
        - If the ask price on exchange 1 is (threshold*100)% higher than the ask price on exchange 2, then sell on exchange 1.
            - I.e. if askExchange_1 >= askExchange_2/(1-0.002) -> Sell on exchange 1
        """
        # Check if we are currently suppressed from making an order
        if node_1.check_order_suppression():
            return None
        # Traverse edges checking for arbitrage
        node_1Id = node_1.correlationId
        for node_2Id, activated in node_1.adjacencyList.items():
            node_2 = self.graph[node_2Id]
            # Check if the edge is activated
            if not activated:    
                # If the other node has been updated but we haven't activated the edge yet
                if not node_2.lastUpdated:
                    self.logger.info("Edge not active yet.")
                    continue
                else:
                    # Activate the edge
                    self.logger.info(f"Activating edge between nodes {node_1Id} and {node_2Id}.")
                    self.graph.activate_edge(node_1Id, node_2Id)
            # Check if the second node is suppressed
            if node_2.check_order_suppression():
                return None
        # Get the value of the possible opportunity
        buy_arb_opportunity = abs(node_1.bestBidPrice - node_2.bestBidPrice) - self.threshold
        ask_arb_opportunity = abs(node_1.bestAskPrice - node_2.bestAskPrice) - self.threshold
        # Buy side logic
        if node_1.bestBidPrice / node_2.bestBidPrice <= self.lb:
            self.logger.info(f"Buy side arbitrage opportunity for pair {node_1.pair} between exchange {node_1.exchange} and {node_2.exchange}.")
            self.logger.debug(f"{node_1.exchange} best bid: {node_1.bestBidPrice}, {node_2.exchange} best bid: {node_2.bestBidPrice}. Possible arbitrage={buy_arb_opportunity}.")
            order_node = node_1 
            offer = node_1.bestBidPrice
            buy = True
        elif node_1.bestBidPrice / node_2.bestBidPrice >= self.ub:
            self.logger.info(f"Buy side arbitrage opportunity for pair {node_1.pair} between exchange {node_2.exchange} and {node_1.exchange}.")
            self.logger.debug(f"{node_2.exchange} best bid: {node_2.bestBidPrice}, {node_1.exchange} best bid: {node_1.bestBidPrice}. Possible arbitrage={buy_arb_opportunity}.")
            order_node = node_2 
            offer = node_2.bestBidPrice
            buy = True
        # Ask side logic
        elif node_1.bestAskPrice / node_2.bestAskPrice >= self.ub:
            self.logger.info(f"Sell side arbitrage opportunity for pair {node_1.pair} between exchange {node_1.exchange} and {node_2.exchange}.")
            self.logger.debug(f"{node_1.exchange} best ask: {node_1.bestAskPrice}, {node_2.exchange} best ask: {node_2.bestAskPrice}. Possible arbitrage={ask_arb_opportunity}.")
            order_node = node_1 
            offer = node_1.bestAskPrice
            buy = False
        elif node_1.bestAskPrice / node_2.bestAskPrice <= self.lb:
            self.logger.info(f"Sell side arbitrage opportunity for pair {node_1.pair} between exchange {node_2.exchange} and {node_1.exchange}.")
            self.logger.debug(f"{node_2.exchange} best ask: {node_2.bestAskPrice}, {node_1.exchange} best ask: {node_1.bestAskPrice}. Possible arbitrage={ask_arb_opportunity}.")
            order_node = node_2
            offer = node_2.bestAskPrice
            buy = False
        # Submit an order
        if self.liveTrade:
            try:
                order = self.orderHandler.submit_order(node=order_node, account_balances=self.account_balances, offer=offer, buy=buy)
                return order
            except Exception as e:
                self.logger.error(e)
        return None
