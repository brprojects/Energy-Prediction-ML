import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file (adjust the path as needed)
df = pd.read_csv('Gas_Price_Data.csv')

# Ensure the 'Trading day' column is in datetime format
df['Trading day'] = pd.to_datetime(df['Trading day'], errors='coerce')

# Plot 'MIBGAS Daily Price [EUR/MWh]' vs 'Trading day'
plt.figure(figsize=(10, 6))  # Set the figure size for the plot
plt.plot(df['Trading day'], df['MIBGAS Daily Price [EUR/MWh]'], linestyle='-', color='b')

# Labeling the plot
plt.title('MIBGAS Daily Price vs Trading Day')
plt.xlabel('Trading Day')
plt.ylabel('MIBGAS Daily Price [EUR/MWh]')
plt.xticks(rotation=45)  # Rotate date labels for better readability

# Display the plot
plt.tight_layout()  # Adjust layout to ensure everything fits
plt.show()
