import pandas as pd
df = pd.read_csv('testdata.csv', encoding='latin1')

print(df.head(10))
print(df.shape)
print(df.dtypes)
print(df.describe())

# ---- clean & Transform ----

# Rename columns to simpler names (easier to type)
df.columns = ['time_s', 'temp_c']

# Check for missing values
print("Missing values:")
print(df.isnull().sum())

# Add a column: time in minutes (easier to read than seconds)
df['time_min'] = df['time_s'] / 60

# Add a column: rolling average (smooths out noise in the signal)
df['rolling_avg'] = df['temp_c'].rolling(window=20, min_periods=1).mean()

# Add a column: rate of change (how fast is temperature rising?)
df['rate_of_change'] = df['temp_c'].diff() / df['time_s'].diff()

# Preview the new table
print(df.head(10))

# ----Analyse & Statistics ----

# Basic statistics
print("=== Key Statistics ===")
print(f"Total readings:        {len(df)}")
print(f"Duration:              {df['time_min'].max():.1f} minutes")
print(f"Starting temperature:  {df['temp_c'].iloc[0]:.2f} °C")
print(f"Maximum temperature:   {df['temp_c'].max():.2f} °C")
print(f"Minimum temperature:   {df['temp_c'].min():.2f} °C")
print(f"Average temperature:   {df['temp_c'].mean():.2f} °C")
print(f"Peak reached at:       {df.loc[df['temp_c'].idxmax(), 'time_min']:.1f} minutes")

# Heating phase vs stable phase
heating = df[df['time_min'] < 5]
stable  = df[df['time_min'] >= 5]

print("\n=== Heating Phase (first 5 minutes) ===")
print(f"Temp rise:  {heating['temp_c'].iloc[-1] - heating['temp_c'].iloc[0]:.2f} °C")
print(f"Avg rate:   {heating['rate_of_change'].mean():.4f} °C/s")

print("\n=== Stable Phase (after 5 minutes) ===")
print(f"Avg temp:   {stable['temp_c'].mean():.2f} °C")
print(f"Std dev:    {stable['temp_c'].std():.4f} °C")

# ----Visualise ----

import matplotlib.pyplot as plt

# Create a figure with 2 charts stacked vertically
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# --- Chart 1: Temperature over time ---
ax1.plot(df['time_min'], df['temp_c'], 
         color='steelblue', linewidth=1, alpha=0.5, label='Raw temperature')
ax1.plot(df['time_min'], df['rolling_avg'], 
         color='crimson', linewidth=2, label='Rolling average')
ax1.axvline(x=12, color='green', linestyle='--', linewidth=1.5, label='Stable phase starts')
ax1.set_title('Temperature over time')
ax1.set_xlabel('Time (minutes)')
ax1.set_ylabel('Temperature (°C)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# --- Chart 2: Rate of change ---
ax2.plot(df['time_min'], df['rate_of_change'], 
         color='orange', linewidth=1)
ax2.axhline(y=0, color='black', linestyle='--', linewidth=1)
ax2.axvline(x=12, color='green', linestyle='--', linewidth=1.5, label='Stable phase starts')
ax2.set_title('Rate of change (°C per second)')
ax2.set_xlabel('Time (minutes)')
ax2.set_ylabel('°C/s')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('temperature_analysis.png', dpi=150)
plt.show()

print("Chart saved as temperature_analysis.png")

# ----Export clean CSV ----

# Round all values to 3 decimal places (clean and readable)
df = df.round(3)

# Export to CSV — this will be used in Phase 2 (SQL)
df.to_csv('clean_data.csv', index=False)

print("=== Export complete! ===")
print(f"Rows exported:   {len(df)}")
print(f"Columns:         {list(df.columns)}")
print("File saved as:   clean_data.csv")