import pandas as pd
import os
import json

folderpath = os.path.join(os.getcwd(), 'Data')

def meanReversionStrategy(prices):
    firstBuy = None
    buyprice = None
    isbought = False
    totalprofit = 0

    buyThreshold = 0.98
    sellThreshold = 1.02

    # Loops through each row and decides whether to buy, sell, otherwise it holds.
    for index, row in prices.iterrows():
        price = row['Price']
        avg = row['5dayAvg']
            
        if firstBuy is None and price < (avg*buyThreshold):
            firstBuy = price
            # print(f"Buying at: {price}")
            buyprice = price
            isbought = True
        
        elif isbought == False and price < (avg*buyThreshold):
            # print(f"Buying at: {price}")
            buyprice = price
            isbought = True
            
        elif isbought and price > (avg*sellThreshold):
            # print(f"Selling at: {price}")
            tprofit = round((price-buyprice), 2)
            totalprofit += tprofit
            # print(f"Trade profit: {tprofit}")
            isbought = False

    if isbought == True:
        # print(f"Selling at: {price}")
        tprofit = round((prices.iloc[-1]['Price']-buyprice), 2)
        totalprofit += tprofit
        # print(f"Trade profit: {tprofit}")
        isbought = False

    return round(totalprofit,2), round((totalprofit/firstBuy)*100,2)


def simpleMovingAverageStrategy(prices):
    firstBuy = None
    buyprice = None
    isbought = False
    totalprofit = 0


    for index, row in prices.iterrows():
        price = row['Price']
        avg = row['5dayAvg']
            
        if firstBuy is None and price < avg:
            firstBuy = price
            # print(f"Buying at: {price}")
            buyprice = price
            isbought = True
        
        elif isbought == False and price < avg:
            # print(f"Buying at: {price}")
            buyprice = price
            isbought = True
            
        elif isbought and price > avg:
            # print(f"Selling at: {price}")
            tprofit = round((price-buyprice), 2)
            totalprofit += tprofit
            # print(f"Trade profit: {tprofit}")
            isbought = False
        
    if isbought == True:
        # print(f"Selling at: {price}")
        tprofit = round((prices.iloc[-1]['Price']-buyprice), 2)
        totalprofit += tprofit
        # print(f"Trade profit: {tprofit}")
        isbought = False
    
    return round(totalprofit,2), round((totalprofit/firstBuy)*100,2)


dataDict = {}

for filename in os.listdir(folderpath):
    if filename.endswith('.csv'):
        ticker = filename[:-4]
        filepath = os.path.join(folderpath, filename)  
        data = pd.read_csv(filepath)  
        data = data.sort_values(by='Date', ascending=True, inplace=False)
        prices = data[['Close/Last']].rename(columns={'Close/Last': 'Price'})
        prices['Price'] = prices['Price'].replace('[\$,]', '', regex=True).astype(float)
        prices['5dayAvg'] = prices['Price'].rolling(window=5).mean()


        totalprofit, preturn = simpleMovingAverageStrategy(prices)
        mtotalprofit, mpreturn = meanReversionStrategy(prices)

        plist = prices['Price'].tolist()
        dataDict[filename[:-4]+'_prices'] = plist
        dataDict[ticker+'_sma_profit'] = totalprofit
        dataDict[ticker+'_sma_returns'] = preturn
        dataDict[ticker+'_mr_profit'] = mtotalprofit
        dataDict[ticker+'_mr_returns'] = mpreturn


json.dump(dataDict, open("tradeData.json", "w"), indent=4)

print("Process Complete")
