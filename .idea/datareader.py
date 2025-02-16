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

#the default case(password abcdefgh, 20 addresses) is 2, 1, 2, 1, 1, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 9, 1, 1, 2
def min_iter(df,addrs=20):
    '''retuns a DataFrame list of minimum possible iterations for each address, reliebly identifies as long as there are no gaps with 0 addresses'''
    q=pd.DataFrame([(j,t[1][t[0]==j].quantile(0.15),t[1][t[0]==j].quantile(0.35)) for j in range(addrs)])
    q[3]=0
    i=1
    while(not q[3].all() and i<256):
        idmin=q[1][q[3]==0].idxmin()#get the index with smallest quantile to not be selected
        q.loc[np.logical_and(q[3]==0,q[1]<=q[2][idmin]),3]=i#assign min iterations to all intersecting quantiles
        i+=1
    return q[3]
