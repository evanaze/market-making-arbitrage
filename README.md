# Market Making Arbitrage
The goal is to work in stages, with the final result being a cross exchange maker-maker market making bot.

### Stage 1
Stage 1 of the project is just looking for arbitrage opportunities for a single pair on two exchanges.
For this stage, I used Kraken and Coinbase as the exchanges.
We expect Kraken to have a wider bid-ask spread than Coinbase, so we look for when the highest bid on Coinbase is higher than the lowest ask on Kraken.