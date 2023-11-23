import numpy as np

n_steps = 365 * 0.25
n_paths = 10000
paths = np.random.standard_normal((int(n_paths), int(n_steps)))