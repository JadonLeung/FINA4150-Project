import numpy as np
from vol_surface import vol_surface


np.random.seed(4150)
n_steps = 90
n_paths = 3000
paths = np.random.standard_normal((int(n_paths), int(n_steps)))


def MC(FP, r, vol_surface, Z=paths, T=0.25, dt=0.25/n_steps):
    F0 = 2000
    # local_vol2_list = [(vol**2)/2 for vol in local_vol_list]
    # Ft = np.array(F0*np.cumprod(np.exp((r-(local_vol2_list))*dt+local_vol_list*Z*np.sqrt(dt)), axis=1))

    Ft = []
    for path in Z:
        Ft_path = []
        current_spot = F0
        for step in range(len(path)):
            local_vol = vol_surface.get_vol(strike = current_spot, t = step * dt)
            current_spot = current_spot * np.exp((r - (local_vol ** 2) / 2) * dt + local_vol * path[step] * np.sqrt(dt))
            Ft_path.append(current_spot)
        Ft.append(Ft_path)
    Ft = np.array(Ft)

    shares_sim = []
    for row in range(len(Ft)):
        shares = []
        accum_double = np.where(Ft[row][::7]<FP)[0]  # check win/loss weekly
        trigger_KO = np.where(Ft[row][::7]>1.1*F0)[0]  # check whether the path triggered KO
        for i in range(int(n_steps / 7)):
            if len(trigger_KO) == 0:  # if never triggered KO
                if i in accum_double:
                    shares.extend([2] * 7)  # buy double shares if losing
                else:
                    shares.extend([1] * 7)  # buy one share if not losing

            else:  # if triggered KO
                if trigger_KO[0] < 3:  # if triggered before guaranteed period
                    if i < trigger_KO[0]:  # before triggering KO
                        if i in accum_double:
                            shares.extend([2] * 7)  # buy double shares if losing
                        else:
                            shares.extend([1] * 7)  # buy one share if not losing
                    elif trigger_KO[0] <= i < 3:  # after triggering KO and before 3 weeks
                        shares.extend([1] * 7)
                    else:  # after triggering KO and after guaranteed period
                        shares.extend([0] * 7)
                else:  # if triggered after guaranteed period
                    if i >= trigger_KO[0]:
                        shares.extend([0] * 7)  # terminate after KO
                    else:
                        if i in accum_double:
                            shares.extend([2] * 7)  # buy double shares if losing
                        else:
                            shares.extend([1] * 7)  # buy one share if not losing
        shares_sim.append(shares)
    shares_sim = np.array(shares_sim)
    sum_shares_sim = np.cumsum(shares_sim, axis=1)[:, -1]  # total number of shares bought for each path

    # payoff
    payoff = []
    for row in range(len(paths)):
        trigger_KO = np.where(Ft[row][::7]>1.1*F0)[0]  # check whether the path triggered KO
        if len(trigger_KO) == 0:  # if never triggered KO
            payoff.append(sum_shares_sim[row] * (Ft[row][-1] - FP) * np.exp(-r * T))
        else:  # if triggered KO
            if trigger_KO[0]<3:
                t = (21 / n_steps) * T  # discount from 3 week
            else:
                t = (trigger_KO[0] / n_steps) * T  # discount from the time triggering KO
            payoff.append(sum_shares_sim[row] * (Ft[row][trigger_KO[0]] - FP) * np.exp(-r * t))
    payoff = np.array(payoff)

    expected_payoff = np.mean(payoff)
    return expected_payoff
