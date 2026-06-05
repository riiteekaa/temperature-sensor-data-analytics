import sqlite3
import pandas as pd

# Create database
conn = sqlite3.connect('sensor_data.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS temperature_readings (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        time_s          REAL,
        temp_c          REAL,
        time_min        REAL,
        rolling_avg     REAL,
        rate_of_change  REAL
    )
''')
conn.commit()

# Import clean CSV
df = pd.read_csv('clean_data.csv')
df.to_sql(
    name='temperature_readings',
    con=conn,
    if_exists='replace',
    index=False
)
conn.commit()

# Verify
cursor.execute('SELECT COUNT(*) FROM temperature_readings')
count = cursor.fetchone()[0]
print(f"Successfully imported {count} rows!")

conn.close()