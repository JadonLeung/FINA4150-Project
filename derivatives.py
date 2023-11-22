import numpy as np
from scipy.misc import derivative 
from scipy.stats import norm

def BS(isCall, logmoneyness, K, r, T, sig):
    F = K / np.exp(logmoneyness)
    d1 = (logmoneyness + (sig**2/2)*T)/(sig*np.sqrt(T))
    d2 = d1 - sig*np.sqrt(T)
    if isCall:
        return (F*norm.cdf(d1) - K*norm.cdf(d2))*np.exp(-r*T)
    else:
        return (K*norm.cdf(-d2) - F*norm.cdf(-d1))*np.exp(-r*T)
    
def bisection_imp_vol(logmoneyness, K, r, T, prc, tol = 1e-20):
    isCall = True if logmoneyness < 0 else False
    sig_l, sig_r = 0, 1
    delta_temp = 1
    while (abs(delta_temp) > tol):
        sig_temp = (sig_l + sig_r)/2
        delta_temp = BS(isCall, logmoneyness, K, r, T, sig_temp) - prc
        if delta_temp > 0:
            sig_r = sig_temp
        else:
            sig_l = sig_temp
    return sig_temp

def partial_derivative(func, var=0, degree=1, point=[]):
    args = point[:]
    def wraps(x):
        args[var] = x
        return func(*args)
    return derivative(wraps, point[var], dx = 1e-6, n = degree)

def forward(c, p, K, r, T):
    return (c - p) * np.exp(r*T) + K

'''
point = [logmoneyness, K, r, T, prc]
'''
def local_vol(point):
    y, K, r, T, prc = point
    w = bisection_imp_vol(y, K, r, T, prc)
    dw_t = partial_derivative(bisection_imp_vol, 3, 1, point)
    dw_y = partial_derivative(bisection_imp_vol, 0, 1, point)
    dw_y2 = partial_derivative(bisection_imp_vol, 0, 2, point)
    return dw_t / (1 - y/w * dw_y + (-1/4 - 1/w + y**2/w**2) * dw_y ** 2 / 4 + dw_y2 / 2)

