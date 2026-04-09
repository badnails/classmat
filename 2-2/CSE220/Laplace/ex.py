import numpy as np

t = np.arange(0,6,1, dtype=int)
delta = 0.3
td = 2

def u_sin():
    return t

def quantize(u):
        return delta * np.round(u / delta)
    
def shift(u):
    return np.interp(t + td, t, u)


print(u_sin())
print(shift(u_sin()))