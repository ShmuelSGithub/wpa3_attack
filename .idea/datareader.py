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

def qplot(df,addrs=20):
    for j in range(addrs):
        tmp=plt.plot(range(50),[df[1][df[0]==j].quantile(i/50) for i in range(50)],label=j)
    #plt.legend() if you care about which address matches which graph
    #plt.show() if you don't wanna add anything else

#2, 1, 2, 1, 1, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 9, 1, 1, 2, for the default case(password abcdefgh,20 addresses), next line is addresses 20-255
#2, 3, 1, 2, 4, 1, 2, 3, 1, 3, 1, 2, 2, 1, 1, 3, 4, 4, 4, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 4, 3, 2, 1, 3, 1, 3, 3, 1, 3, 2, 3, 1, 1, 3, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 4, 2, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 2, 1, 1, 2, 3, 1, 2, 2, 1, 1, 2, 1, 1, 10, 2, 1, 6, 1, 1, 1, 1, 1, 1, 5, 1, 1, 2, 1, 1, 3, 3, 1, 1, 1, 6, 3, 1, 1, 1, 3, 1, 1, 2, 1, 1, 2, 1, 4, 2, 1, 2, 1, 3, 1, 2, 2, 1, 2, 1, 3, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 6, 1, 4, 1, 1, 1, 5, 3, 1, 1, 2, 3, 1, 3, 2, 1, 1, 3, 1, 1, 2, 4, 4, 2, 3, 3, 1, 3, 1, 5, 1, 1, 5, 2, 2, 3, 1, 1, 2, 2, 1, 1, 1, 2, 3, 2, 3, 1, 2, 1, 1, 1, 3, 2, 2, 1, 1, 3, 1, 2, 1, 1, 1, 1, 1,
def min_iter(df,addrs=20):
    '''retuns a DataFrame list of minimum possible iterations for each address'''
    q=pd.DataFrame([(j,df[1][df[0]==j].quantile(0.15),df[1][df[0]==j].quantile(0.35)) for j in range(addrs)])
    q[3]=0
    i=1
    while(not q[3].all() and i<256):
        idmin=q[1][q[3]==0].idxmin()#get the index with smallest quantile to not be selected
        q.loc[np.logical_and(q[3]==0,q[1]<=q[2][idmin]),3]=i#assign min iterations to all intersecting quantiles
        i+=1
    return q[3]

def iterations(df,addrs=20):
    '''retuns a DataFrame list of iterations for each address, assuming there are addresses with 1,2,3 iterations'''
    q=pd.DataFrame([(j,df[1][df[0]==j].quantile(0.15),df[1][df[0]==j].quantile(0.35)) for j in range(addrs)])
    q[3]=0
    i=1
    while(not q[3].all() and i<256):
        idmin=q[1][q[3]==0].idxmin()#get the index with smallest quantile to not be selected
        q.loc[np.logical_and(q[3]==0,q[1]<=q[2][idmin]),3]=i#assign min iterations to all intersecting quantiles
        i+=1
    #qsums[j-1]=(count of j iterations addresses,sum of the low quntiles at j, sum of the high quantiles at j)
    qsums=[((q[3]==j).sum(),q[1][q[3]==j].sum(),q[2][q[3]==j].sum()) for j in (1,2,3)]
    #time(1 iteration)≈E[((quntile of x iterations)-(quntile of x-k iterations))/k]≈sum(all such possible pairs)/#(all such possible pairs)
    itrtimelowhigh=[(qsums[2][j]*(qsums[1][0]+0.5*qsums[0][0])+qsums[1][j]*(qsums[0][0]-qsums[2][0])+qsums[0][j]*(-qsums[1][0]-0.5*qsums[2][0]))/
                    (qsums[1][0]*(qsums[0][0]+qsums[2][0])+qsums[0][0]*qsums[2][0]) for j in (1,2)]
    itrtime=sum(itrtimelowhigh)/2
    i=4
    maxi=q[3].max()
    floor1=qsums[0][1]/qsums[0][0]#average low quntile of 1 iteration addresses
    q[4]=0
    while(i<=maxi):
        floor=(q[1][q[3]==i].sum()+q[2][q[3]==i].sum())/(2*(q[3]==i).sum())#average of average quntile of group i
        q.loc[q[3]==i,4]=1+(floor-floor1)//itrtime#number of iterations estimate
        i+=1
    
    return q[3].clip(lower=q[4])
