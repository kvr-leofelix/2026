import pandas as pd
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00194/sensor_readings_24.data"
df_robot = pd.read_csv(url, header=None)
data = df_robot[0]

a=len(data)
MeanVal =sum(data)/a
SortedSensor = sorted(data)
if a % 2 == 0:#finding the median
    b = int(a / 2)
    MedianVal=(SortedSensor[b-1]+SortedSensor[b])/2
else:
    MedianVal=SortedSensor[int(a/2)]

ModeVal = data.mode()[0]#most element in the data set
range_val =max(data)-min(data)

sum_sq = 0
for c in data:
    sum_sq = sum_sq + ((c - MeanVal) ** 2)
SampleVar = sum_sq / (a - 1)
std_dev = SampleVar ** 0.5
print("Standard Deviation is", std_dev)
if MeanVal > MedianVal:
    print("The data is right skew")
elif MeanVal < MedianVal:
    print("The given data is left skew")
else:
    print("The given data is symmetric")

#doing the VARIANCE AND SD USING THE MEAN AND MEANVA
print("Mean is ", MeanVal)
print("Median is ", MedianVal)
print("Mode is", ModeVal)
print("Range is", range_val)
