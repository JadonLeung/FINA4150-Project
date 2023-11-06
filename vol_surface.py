import numpy as np
import scipy.optimize as opt

'''

'''
class vol_curve:
    def __init__(self, vol: list, logmoneyness: list, atm_vol: float):
        self.sigma = vol
        self.K = logmoneyness
        self.sigmaATM = atm_vol

    def _obj(params, sigma, K, sigmaATM):
        delta, gamma, kappa = params
        sigma = np.array(sigma)
        K = np.array(K)
        return sum((sigma - sigmaATM - delta * (np.tanh(kappa * K) / kappa) - gamma / 2 * (np.tanh(kappa * K) / kappa) ** 2) ** 2)

    def fit(self, method='SLSQP', ini_guess=[1, 1, 1]):
        self.result = opt.minimize(self._obj, np.array(ini_guess), method=method, args = (self.sigma, self.K, self.sigmaATM))
        self.delta, self.gamma, self.kappa = self.result.x

    def get(self, logmoneyness: float or list):
        K = np.array(logmoneyness)
        return self.sigmaATM + self.delta * (np.tanh(self.kappa * K) / self.kappa) + self.gamma / 2 * (np.tanh(self.kappa * K) / self.kappa) ** 2