import pandas as pd

# Load the dataset
df = pd.read_csv('path/to/your/file.csv')

# Display the first few rows of the dataset
print(df.head())

# Get a summary of the dataset
print(df.info())

# Get descriptive statistics
print(df.describe())
