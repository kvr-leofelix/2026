import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('contact_force.csv')
data = df['Force_Newtons']
a = len(data)
min_val=min(data)
max_val=max(data)

SortedForce=sorted(data)#doing the sequence things
if a%2 == 0:
    b = int(a/2)
    MedianVal=(SortedForce[b-1]+SortedForce[b])/2
else:
     MedianVal = SortedForce[int(a/2)]

Q1 = data.quantile(0.25)#her q1 and q3 are found
Q3 = data.quantile(0.75)
iqr_val = Q3 - Q1
lower_fence = Q1-(1.5*iqr_val)#finding the outlier
UpperFence=Q3+(1.5*iqr_val)

MeanVal = sum(data) / a
print("Mean is", MeanVal)
print("Minimum valu is:", min_val)
print("Q1:", Q1)
print("Q3:", Q3)
print("Median value is:", MedianVal)

print("Maximum value :", max_val)
print("IQR value:", iqr_val)
print("Lower Fence is:", lower_fence)
print("Upper Fence is", UpperFence)


if MeanVal > MedianVal:
    print("this distribution is right-skewed")
elif MeanVal < MedianVal:
        print("This distribution is left-skewed")
else:
    print("This distribution is symmetric")

plt.boxplot(data)
plt.show()

Sq = 0
for c in data:
    Sq=Sq+((c-MeanVal)**2)#vaiance and standard deviation
SampleVar=Sq/(a-1)
std_dev=SampleVar**0.5

Cu = 0
for c in data:
    Cu=Cu+((c-MeanVal)**3)
SkewnessVal = Cu/((a-1)*(std_dev**3))
print(SkewnessVal)
