import pandas as pd
import numpy as np
from datetime import datetime
from derivatives import forward

APR = 3.41 / 100
r = np.log(1 + APR)

if __name__ == '__main__':
    trades = pd.read_csv('/Users/jleung/workspace/FINA4150-Project/order_book.csv')
    trades = trades[['best_bid_price', 'best_ask_price', 'last_price', 'underlying_index', 'underlying_price', 'instrument_name', 'timestamp.1']]
    trades[['underlying', 'maturity_date', 'strike', 'option_type']] = trades['instrument_name'].str.split('-', expand=True)
    trades['strike'] = trades['strike'].astype(float)
    trades.best_bid_price = [trades.best_bid_price[i] if trades.best_bid_price[i] > 0 else trades.best_ask_price[i] for i in range(len(trades))]
    trades.best_ask_price = [trades.best_ask_price[i] if trades.best_ask_price[i] > 0 else trades.best_bid_price[i] for i in range(len(trades))]
    trades['mid'] = (trades.best_ask_price + trades.best_bid_price) / 2
    trades.mid = [trades.mid[i] if trades.mid[i] > 0 else trades.last_price[i] for i in range(len(trades))]
    trades.dropna(inplace=True)
    trades.sort_values('strike', inplace=True)

    trades['maturity_date'] = pd.to_datetime(trades['maturity_date'], format='%d%b%y')
    trades['maturity'] = (trades['maturity_date'] - datetime(2023, 11, 20)) / pd.Timedelta(days=365)
    
    # put_maturity = []
    # put_moneyness = []
    # put_data = []
    # call_data = []
    # call_maturity =[]
    # call_moneyness =[]
    # forward_price = []
    df = pd.DataFrame()
    for maturity in pd.unique(trades['maturity']):
        temp = trades[trades['maturity'] == maturity]
        underlying = np.float64(list(temp[temp['timestamp.1'] == max(temp['timestamp.1'])]['underlying_price'])[0])
        put = temp[temp['option_type'] == 'P']
        call = temp[temp['option_type'] == 'C']
        strikes = list(set(put.strike) & set(call.strike))
        if len(strikes) == 0:
            continue
        # f, count = 0, 0
        # if len(strikes) > 0:
        #     print('Maturity is ', maturity)
        #     print('Maturity date is ', temp['maturity_date'].iloc[0])
        #     print('strikes are ', strikes)
        #     for strike in strikes:
        #         if abs(float(strike) / underlying - 1) < 0.1:
        #             p = float(put[put['strike'] == strike]['mid'])
        #             c = float(call[call['strike'] == strike]['mid'])
        #             f += forward(c, p, float(strike), r, maturity)
        #             count += 1
        #     f /= count
        #     print('Forward Price is', f)
        # if f == 0:
        #     continue

        n_put = len(put[put.strike / underlying <= 1])
        n_call = len(call[call.strike / underlying > 1])

        puts = pd.DataFrame({
            'maturity': put.maturity.tolist()[:n_put],
            'moneyness': put.strike.tolist()[:n_put] / underlying,
            'price': put.mid.tolist()[:n_put], 
            'strike': put.strike.tolist()[:n_put],
            'type': ['P'] * n_put,
            'forward': underlying
        })
        df = pd.concat([df, puts], axis=0)

        calls = pd.DataFrame({
            'maturity': call.maturity.tolist()[-n_call:],
            'moneyness': call.strike.tolist()[-n_call:] / underlying,
            'price': call.mid.tolist()[-n_call:], 
            'strike': call.strike.tolist()[-n_call:],
            'type': ['C'] * n_call,
            'forward': underlying
        })
        df = pd.concat([df, calls], axis=0)

        # put_maturity.append(put.maturity.tolist()[:n_put])
        # put_data.append(put.mid.tolist()[:n_put])
        # # put_moneyness.append(put.strike.tolist() / f)
        # put_moneyness.append(put.strike.tolist()[:n_put] / underlying)
        # call_maturity.append(call.maturity.tolist()[-n_call:])
        # call_data.append(call.mid.tolist()[-n_call:])
        # # call_moneyness.append(call.strike.tolist() / f)
        # call_moneyness.append(call.strike.tolist()[-n_call:] / underlying)
        # forward_price.append(underlying)

    df.to_csv('cleaned_data.csv', index=False)
        