import pandas as pd
import os

folderpath = '/Users/joshua/Desktop/HW4-Trading/Data'
bestprofit = 0 


for filename in os.listdir(folderpath):
    if filename.endswith('.csv'):
        filepath = os.path.join(folderpath, filename)  
        data = pd.read_csv(filepath)  
        
        prices = data[['Close/Last']].rename(columns={'Close/Last': 'Price'})
        prices['Price'] = prices['Price'].replace('[\$,]', '', regex=True).astype(float)
        prices['5dayAvg'] = prices['Price'].rolling(window=5).mean()

        firstBuy = None
        buyprice = None
        isbought = False
        totalprofit = 0
        profitAmts = [] 

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
            
            elif price < (avg*buyThreshold) and isbought == False:
                # print(f"Buying at: {price}")
                buyprice = price
                isbought = True
                
            elif isbought and price > (avg*sellThreshold):
                # print(f"Selling at: {price}")
                tprofit = round((price-buyprice), 2)
                totalprofit += tprofit
                # print(f"Trade profit: {tprofit}")
                isbought = False
                profitAmts.append(tprofit)

        avgt = sum(profitAmts)/len(profitAmts)
        print()
        print(f'------- {len(profitAmts)} Trades Complete for {filename[:-4]} -------')
        print(f'Total profit: {round(totalprofit,2)}')
        print(f'Average trade profit: {round(avgt,2)}')
        print(f'First buy: {firstBuy}')
        print(f'Percent return: {round((totalprofit/firstBuy)*100,2)}'+'%')

        if totalprofit > bestprofit:
            bestprofit = round(totalprofit,2)
            fmessage = f"\nBest total profit was ${bestprofit} from {filename[:-4]}"



print(fmessage)
