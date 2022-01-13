# Market Making Arbitrage
The goal is to work in stages, with the final result being a cross exchange maker-maker market making bot.

### Usage
Build the docker container and then run it using docker compose.

```shell
docker compose build
docker compose up
```

The results of the program will be available in the logs.

### Stage 1
Stage 1 of the project is just looking for arbitrage opportunities for a single pair on two exchanges.
For this stage, I used Kraken and Coinbase as the exchanges.
We expect Kraken to have a wider bid-ask spread than Coinbase, so we look for opportunities when the highest bid on one exchange is higher than the lowest ask on the other exchange.

### Phase 2
*TBD*