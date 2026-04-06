import pandas as pd

# Sample DataFrame
data = {'Name': ['John', 'Anna', 'Peter', 'Linda'],
        'Age': [28, 34, 29, 32],
        'City': ['New York', 'Paris', 'Berlin', 'London']}
df = pd.DataFrame(data)

# Sort by the 'Age' column in ascending order (default)
df_sorted = df.sort_values(by='Age')

print(df_sorted)
