import pandas as pd

data = pd.read_csv('TSLAdata.csv')
prices = data[['Close/Last']].rename(columns={'Close/Last': 'Price'})

prices['5dayAvg'] = prices['Price'].rolling(window=5).mean()



firstBuy = ''
buyprice = ''
isbought = False

for row in prices.values:
    price = row[0]
    avg = row[1]
    
    
    if firstBuy == '' and price < (avg*0.98):
        firstBuy = price
        print(f"Buying at: {price}")
        buyprice = price
        isbought = True
    
    
    elif price < (avg*0.98) and isbought == False:
        print(f"Buying at: {price}")
        buyprice = price
        isbought = True
        
    
    elif isbought and price > (avg*1.02):
        print(f"Selling at: {price}")
        print(f"Trade profit: {(buyprice-price)*-1}")
        isbought = False


    else:
        print('Hold')