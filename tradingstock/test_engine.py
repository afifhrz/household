from .engine_trading import summary1, check_signal_buy
from datetime import datetime, timezone

def main_test_engine(stockCode, dataClose, dataOpen, timestamp):
    startBalance = 10000000
    balance = startBalance
    theOne_Percentage = 0.5
    buyFast_Percentage = 0.25
    lotBalance = 0
    startIndex = 0
    endIndex = len(dataClose)//2
    timeline = []
    owned = False

    while True:
        prevData = summary1(dataClose[startIndex:endIndex], dataOpen[startIndex:endIndex], test=True)
        todayData = summary1(dataClose[startIndex+1:endIndex+1], dataOpen[startIndex+1:endIndex+1], test=True)
        if owned:        
            resultCheck = check_signal_buy(todayData, prevData, owned=owned, buy_price=timeline[-1]['price'])
        else:
            resultCheck = check_signal_buy(todayData, prevData, owned=owned)

        if resultCheck == "THEONE" or resultCheck == "BUY_FAST":
            if resultCheck == "THEONE":
                availableToBuy = theOne_Percentage*balance
            elif resultCheck == "BUY_FAST":
                availableToBuy = buyFast_Percentage*balance

            lotToBuy = availableToBuy//(dataOpen[endIndex+2]*100)
            balance -= lotToBuy*100*dataOpen[endIndex+2]
            lotBalance += lotToBuy
            timeline.append({
                "prevdata_ma_d_3": prevData["ma_d_3"],
                "prevdata_ma_d_18": prevData["ma_d_18"],
                "prevdata_ma_d_50": prevData["ma_d_50"],
                "data_today": todayData["last_price"],
                "data_ma_d_3": todayData["ma_d_3"],
                "data_ma_d_18": todayData["ma_d_18"],
                "data_ma_d_50": todayData["ma_d_50"],
                "data_ma_d_100": todayData["ma_d_100"],
                "data_ma_d_200": todayData["ma_d_200"],
                "datetime":datetime.fromtimestamp(timestamp[endIndex+2], timezone.utc).isoformat('T', 'microseconds'),
                "action": resultCheck,
                "balance": balance,
                "buyAmount" : dataOpen[endIndex+2]*lotBalance*100,
                "lotBalance" : lotBalance,
                "buyLot": lotToBuy,
                "price": dataOpen[endIndex+2]
            })
            owned = True
        elif resultCheck == "SELL_TAKEPROFIT_CROSS" or resultCheck == "SELL_CUTLOSS" or resultCheck == "SELL_TAKEPROFIT":
            availableToSell = lotBalance*dataOpen[endIndex+2]*100
            balance += availableToSell
            lotToSell = lotBalance
            lotBalance -= lotToSell
            timeline.append({
                "data_ma_d_3": todayData["ma_d_3"],
                "data_ma_d_18": todayData["ma_d_18"],
                "datetime":datetime.fromtimestamp(timestamp[endIndex+2], timezone.utc).isoformat('T', 'microseconds'),
                "action": resultCheck,
                "balance": balance,
                "sellAmount" : availableToSell,
                "lotBalance" : lotBalance,
                "sellLot": lotToSell,
                "price": dataOpen[endIndex+2]
            })
            owned = False

        startIndex+=1
        endIndex+=1

        if endIndex+2 >= len(dataClose):
            break
    
    if lotBalance != 0:
        availableToSell = lotBalance*dataOpen[endIndex+1]*100
        balance += availableToSell
        lotBalance -= lotBalance
        timeline.append({
            "datetime":datetime.fromtimestamp(timestamp[endIndex+1], timezone.utc).isoformat('T', 'microseconds'),
            "action": "SELL_FORC",
            "balance": balance,
            "sellAmount" : availableToSell,
            "lotBalance" : lotBalance,
            "price": dataOpen[endIndex+1]
        })

    return {
        "stockCode":stockCode,
        "balance": balance,
        "gain/loss": (balance-startBalance)/startBalance,
        "startbalance":startBalance,
        "detail_timeline":timeline
    }