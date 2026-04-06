import numpy as np
import pandas as pd
a=pd.read_csv("tr.csv")
b=a["AAPL"]
c=b.sort_values()
mean1=sum(c)/len(c)
if len(c)%2==0:
    medi1=(c[len(c)/2-1]+c[len(c)/2])/2
else:
    medi1=c[len(c)/2]
