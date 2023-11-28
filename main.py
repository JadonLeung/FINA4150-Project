import pandas as pd
from derivatives import bisection_imp_vol, local_vol
import numpy as np
from vol_surface import vol_curve, vol_surface
from simulation import MC
from matplotlib import pyplot as plt


APR = 3.41 / 100
r = np.log(1 + APR)
kappa = 5
FP_test = np.arange(1500, 1950, 50)  # things to solve
# np.random.seed(4150)

if __name__ == '__main__':
    df = pd.read_csv('cleaned_data.csv')
    unique_maturity = sorted(pd.unique(df.maturity))
    curves = []
    for maturity in unique_maturity:
        temp_df = df[df.maturity == maturity]
        temp_df['logmoneyness'] = np.log(temp_df.moneyness.tolist())
        vol = [bisection_imp_vol(row.logmoneyness, row.strike, r, row.maturity, row.price) for idx, row in temp_df.iterrows()]
        put = temp_df[temp_df.type == 'P'].iloc[-1]
        call = temp_df[temp_df.type == 'C'].iloc[0]
        lvs = []
        for idx, row in temp_df.iterrows():
            lv = local_vol([row.logmoneyness, row.strike, r, row.maturity, row.price])
            if lv < 0 or abs(lv) < 0.0001:
                lvs.append(0.0)
            else:
                lvs.append(lv)
        start, end = np.nonzero(lvs)[0][0], np.nonzero(lvs)[0][-1] + 1
        if len(lvs[start:end]) <= 3:
            continue
        atm_vol = (local_vol([put.logmoneyness, put.strike, r, put.maturity, put.price]) * put.moneyness + \
        local_vol([call.logmoneyness, call.strike, r, call.maturity, call.price]) * call.moneyness) / (put.moneyness + call.moneyness)
        atm_vol = atm_vol if atm_vol > 0 else 0
        curve = vol_curve(np.sqrt(lvs[start:end]), temp_df.strike[start:end], temp_df.forward[start:end], np.sqrt(atm_vol), maturity, kappa)
        curve.fit()
        strikes = np.linspace(1000, 5000, 100)
        plt.plot(strikes, curve.get_vol_list(strikes))
        curves.append(curve)
    surface = vol_surface(curves)

    for FP in FP_test:
        payoff = MC(FP=FP, r=r, vol_surface=surface)
        print("FP: ", FP, "    payoff:", payoff)
    # payoff = MC(FP=, r=r, vol_surface=surface)
    # print(payoff)