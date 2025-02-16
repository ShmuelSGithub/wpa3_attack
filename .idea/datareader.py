import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
def data(path):
    f=open(path)
    T=f.readlines()
    f.close()
    T=T[6:-1]
    T=[str.split(a," ") for a in T]
    T=[(int(a[1][:-1],16),int(a[2][:-1],10)) for a in T]
    return pd.DataFrame(T)
