import random
import numpy as np
random.seed(20)

n=20
p=0.7
N=500
# -------
data =np.random.binomial(n,p,size=N)
# print(data)
def ans(data,binn):
    a,b=np.histogram(data,bins=binn)
    # print(a)
    # print(b)

    total=len(data)
    pmf=a/total
    # print(len(a)," ",len(a/total))
    print(f"number of total bin is {binn}")
    for i in range(len(a)):
        print(f"interval {b[i]:.2f} to {b[i+1]:.2f} : probabiility {pmf[i]:.2f}")

    summation=np.sum(pmf)


    postive=np.all(pmf>=0)
    print(f"total sigma sum is : {summation}")

    if (summation==1)&(postive>=0):#now check pmf with both condition
        print("yes it is pmf")

ans(data,5)