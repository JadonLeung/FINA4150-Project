import pandas as pd
from derivatives import bisection_imp_vol
import numpy as np
from vol_surface import vol_curve

APR = 3.41 / 100
r = np.log(1 + APR)

if __name__ == '__main__':
    df = pd.read_csv('/Users/jleung/workspace/FINA4150-Project/cleaned_data.csv')
    unique_maturity = pd.unique(df.maturity)
    temp_df = df[df.maturity == unique_maturity[0]]
    temp_df['logmoneyness'] = np.log(temp_df.moneyness.tolist())
    vol = [bisection_imp_vol(row.logmoneyness, row.strike, r, row.maturity, row.price) for idx, row in temp_df.iterrows()]
    put = temp_df[temp_df.type == 'P'].iloc[-1]
    call = temp_df[temp_df.type == 'C'].iloc[0]
    atm_vol = (bisection_imp_vol(put.logmoneyness, put.strike, r, put.maturity, put.price) * put.moneyness + \
    bisection_imp_vol(call.logmoneyness, call.strike, r, call.maturity, call.price) * call.moneyness) / (put.moneyness + call.moneyness)
    curve = vol_curve(vol, temp_df.logmoneyness.tolist(), atm_vol)
    curve.fit()