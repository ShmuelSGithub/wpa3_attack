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

def qplot(df):
    for j in range(20):
        tmp=plt.plot(range(50),[df[1][df[0]==j].quantile(i/50) for i in range(50)],label=j)
    #plt.legend() if you care about which address matches which graph
    #plt.show() if you don't wanna add anything else
