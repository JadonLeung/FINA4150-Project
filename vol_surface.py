import numpy as np
import scipy.optimize as opt

'''

'''
class vol_curve:
    def __init__(self, vol: list, logmoneyness: list, atm_vol: float, kappa: float):
        self.sigma = vol
        self.K = logmoneyness
        self.sigmaATM = atm_vol
        self.kappa = kappa

    '''
    Sum of squared error of sigma
    '''
    def _obj(self, params, sigma, K, sigmaATM, kappa):
        delta, gamma = params
        sigma = np.array(sigma)
        K = np.array(K)
        return sum((sigma ** 2 - sigmaATM ** 2 - delta * (np.tanh(kappa * K) / kappa) - gamma / 2 * (np.tanh(kappa * K) / kappa) ** 2) ** 2)

    def fit(self, method='SLSQP', ini_guess=[1, 1, 1]):
        self.result = opt.minimize(self._obj, np.array(ini_guess), method=method, args=(self.sigma, self.K, self.sigmaATM, self.kappa))
        self.delta, self.gamma = self.result.x

    def get(self, logmoneyness: float or list):
        K = np.array(logmoneyness)
        return self.sigmaATM ** 2 + self.delta * (np.tanh(self.kappa * K) / self.kappa) + self.gamma / 2 * (np.tanh(self.kappa * K) / self.kappa) ** 2