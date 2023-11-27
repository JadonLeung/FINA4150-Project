import numpy as np
import scipy.optimize as opt
from scipy.interpolate import CubicSpline

'''

'''
class vol_curve:
    def __init__(self, vol: list, strike: list, forward: list, atm_vol: float, maturity: float, kappa: float):
        self.sigma = vol
        self.K = np.array(strike)
        self.F = np.array(forward)
        self.logM = np.log(self.K / self.F)
        self.sigmaATM = atm_vol
        self.maturity = maturity
        self.kappa = kappa

    '''
    Sum of squared error of sigma
    '''
    def _obj(self, params, sigma, logM, sigmaATM):
        kappa = self.kappa
        delta, gamma = params
        # delta, gamma, kappa = params
        sigma = np.array(sigma)
        logM = np.array(logM)
        x = (np.tanh(kappa * logM) / kappa)
        return sum((sigma * sigma - sigmaATM - delta * x - gamma * x * x / 2) ** 2)

    def fit(self, method='SLSQP', ini_guess=[1, 1]):
        self.result = opt.minimize(self._obj, np.array(ini_guess), method=method, args=(self.sigma, self.logM, self.sigmaATM))
        # self.delta, self.gamma, self.kappa = self.result.x
        self.delta, self.gamma = self.result.x

    def get(self, K: float or list):
        logM = np.log(np.array(K / self.F[0]))
        x = (np.tanh(self.kappa * logM) / self.kappa)
        return self.sigmaATM + self.delta * x  + self.gamma * x * x / 2

class vol_surface:
    def __init__(self, curves: list):
        self.curves = curves

    def get(self, strike, t):
        vols = []
        maturities = []
        for curve in self.curves:
            vols.append(curve.get(strike))
            maturities.append(curve.maturity)
        print(vols)
        CS = CubicSpline(np.array(maturities), np.array(vols))
        return CS(t)

        