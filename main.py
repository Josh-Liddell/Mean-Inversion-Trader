import pandas as pd

data = pd.read_csv('TSLAdata.csv')
prices = data[['Close/Last']].rename(columns={'Close/Last': 'Price'})
prices['5dayAvg'] = prices['Price'].rolling(window=5).mean()

firstBuy = None
buyprice = None
isbought = False
totalprofit = 0
profitAmts = [] 

buyThreshold = 0.98
sellThreshold = 1.02

for index, row in prices.iterrows():
    price = row['Price']
    avg = row['5dayAvg']
        
    if firstBuy is None and price < (avg*buyThreshold):
        firstBuy = price
        print(f"Buying at: {price}")
        buyprice = price
        isbought = True
    
    elif price < (avg*buyThreshold) and isbought == False:
        print(f"Buying at: {price}")
        buyprice = price
        isbought = True
        
    elif isbought and price > (avg*sellThreshold):
        print(f"Selling at: {price}")
        tprofit = round((price-buyprice), 2)
        totalprofit += tprofit
        print(f"Trade profit: {tprofit}")
        isbought = False
        profitAmts.append(tprofit)


avgt = sum(profitAmts)/len(profitAmts)
print()
print(f'------- {len(profitAmts)} Trades Complete -------')
print(f'Total profit: {round(totalprofit,2)}')
print(f'Average trade profit: {round(avgt,2)}')
print(f'First buy: {firstBuy}')
print(f'Percent return: {round((totalprofit/firstBuy)*100,2)}'+'%')

