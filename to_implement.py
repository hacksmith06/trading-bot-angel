"""
Input Params:
1. Trade Type - NIFTY
2. Strike Price - 20,000
3. Option Type - CE/PE
4. Premium - 65.5

System Flow:
1. Create an entry in the database
2. Create a order placement async task for each incoming order  

Ordering Placement System:
1. Monitor the first 5 candles
2. Calculate the high using the candles from 9.16 to 9.19
3. Add 1 to the high price
4. Place an order at 9.20 using the calculated price
5. Update the status of the order in the order management system
6. Create a order monitoring async task for each order after it's placement
7. Do this for each order present in the ordering system (async)
8. Orders will only be accepted between 9.00 to 9.15

Order Monitor Async Task:
# For each tick, evaluate whether we have hit the target price or have gone above it, if yes, square off
# If we go below and hit the stoploss anyways we'll square off


Order Model:
1. Trade Type - NIFTY
2. Strike Price - 20,000
3. Option Type - CE/PE
4. Premium - 65.5
5. Target Delta - 17
6. Stoploss Delta - 7
7. Status - CREATED, BOT_PENDING, MARKET_PENDING, MARKET_LIVE, MARKET_SQOFF, BOT_REJECTED
8. Creation Datetime - Timestamp
9. Exit Datetime - Timestamp
10. Unique Order ID - System Generated
"""



