import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
np.random.seed(20)

n=500
lam=2
A=2

B=3
mu,sigma=5,2
# sigma=2

d1=np.random.exponential(1/lam,n)
d2= np.random.normal(mu,sigma,n)
d3= np.random.beta(A,B,n)
grp=[d1,d2,d3] #makea group

label=['expo','NORMAL',"BETA"]
x0=1.5
plt.figure(figsize=(20,20))

for i,data in enumerate(grp):#to make the index with group
    kde= gaussian_kde(data) #
    densityAt_x0 = kde.evaluate(x0)[0]

    
    print(label[i]," density at  x=",x0,densityAt_x0)
    
    plt.subplot(1,3,i+1) 
    # print(densityAt_x0) so this work
    plt.hist(data, bins=30, density=True,color='gray', label='hist Graph')


    x_range = np.linspace(min(data), max(data), 1000)
    plt.plot(x_range, kde(x_range), lw=2, label='KDE')
    plt.axvline(x0, color='blue',)
    plt.title(f"{label[i]} Distribution")

    plt.legend()

plt.tight_layout()
plt.show()