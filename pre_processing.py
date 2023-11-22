import pandas as pd
import numpy as np
from datetime import datetime
from derivatives import forward

if __name__ == '__main__':
    trades = pd.read_csv('/Users/jleung/workspace/FINA4150-Project/last_trades.csv')
    trades[['underlying', 'maturity_date', 'strike', 'option_type']] = trades['instrument_name'].str.split('-', expand=True)
    trades.drop_duplicates(subset=['maturity_date', 'strike', 'option_type'], inplace=True)
    trades['maturity_date'] = pd.to_datetime(trades['maturity_date'], format='%d%b%y')
    trades['maturity'] = (trades['maturity_date'] - datetime(2023, 11, 21)) / pd.Timedelta(days=365)
    
    put_maturity = []
    put_strike = []
    put_data = []
    call_data = []
    call_maturity =[]
    call_strike=[]
    forward_price = []
    for maturity in pd.unique(trades['maturity']):
        temp = trades[trades['maturity'] == maturity]
        put = temp[temp['option_type'] == 'P']
        call = temp[temp['option_type'] == 'C']
        put_maturity.append(put.maturity.tolist())
        put_data.append(put.price.tolist())
        put_strike.append(put.strike.tolist())
        call_maturity.append(call.maturity.tolist())
        call_data.append(call.price.tolist())
        call_strike.append(call.strike.tolist())
        strikes = list(set(put.strike) & set(call.strike))
        f = 0
        n_strike = len(strikes)
        if n_strike > 0:
            for strike in strikes:
                p = float(put[put['strike'] == strike]['price'])
                c = float(call[call['strike'] == strike]['price'])
                f += forward(c, p, float(strike), 0.03, maturity)
            f /= n_strike
        forward_price.append(f)
        