import numpy as np
import scipy.optimize as opt

class vol_curve:
    def __init__(self):
        pass

    def _obj(params, sigma, K, sigmaATM):
        delta, gamma, kappa = params
        sigma = np.array(sigma)
        K = np.array(K)
        return sum((sigma - sigmaATM - delta * (np.tanh(kappa * K) / kappa) - gamma / 2 * (np.tanh(kappa * K) / kappa) ** 2) ** 2)

    def fit():
        pass

def vol_curve_obj(params, sigma, K, sigmaATM):
    delta, gamma, kappa = params
    sigma = np.array(sigma)
    K = np.array(K)
    return sum((sigma - sigmaATM - delta * (np.tanh(kappa * K) / kappa) - gamma / 2 * (np.tanh(kappa * K) / kappa) ** 2) ** 2)

def vol_curve_get(params, K, sigmaATM):
    delta, gamma, kappa = params
    K = np.array(K)
    return sigmaATM + delta * (np.tanh(kappa * K) / kappa) + gamma / 2 * (np.tanh(kappa * K) / kappa) ** 2

def vol_curve_optimize(vol, K, volATM):
    res = opt.minimize(vol_curve_obj, np.array([1, 1, 1]), method='SLSQP', args = (vol, K, volATM))
    return res.x