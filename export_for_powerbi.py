import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('sensor_data.db')

# Query 1 — full cleaned data with all columns
df_full = pd.read_sql_query('''
    SELECT
        time_s,
        time_min,
        temp_c,
        rolling_avg,
        rate_of_change,
        ROUND(MAX(temp_c) OVER (
            ORDER BY time_min
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ), 2)                           AS cumulative_max,
        CASE
            WHEN time_min < 12 THEN 'Heating phase'
            ELSE 'Stable phase'
        END                             AS phase,
        ROUND(PERCENT_RANK() OVER (
            ORDER BY temp_c
        ) * 100, 1)                     AS percentile
    FROM temperature_readings
    ORDER BY time_min
''', conn)

# Query 2 — summary stats per minute (for bar charts in Power BI)
df_per_minute = pd.read_sql_query('''
    SELECT
        CAST(time_min AS INTEGER)       AS minute,
        COUNT(*)                        AS readings,
        ROUND(AVG(temp_c), 2)           AS avg_temp,
        ROUND(MAX(temp_c), 2)           AS max_temp,
        ROUND(MIN(temp_c), 2)           AS min_temp
    FROM temperature_readings
    GROUP BY CAST(time_min AS INTEGER)
    ORDER BY minute
''', conn)

# Query 3 — phase summary (for KPI cards in Power BI)
df_phases = pd.read_sql_query('''
    SELECT
        CASE
            WHEN time_min < 12 THEN 'Heating phase'
            ELSE 'Stable phase'
        END                             AS phase,
        COUNT(*)                        AS readings,
        ROUND(AVG(temp_c), 2)           AS avg_temp,
        ROUND(MIN(temp_c), 2)           AS min_temp,
        ROUND(MAX(temp_c), 2)           AS max_temp
    FROM temperature_readings
    GROUP BY phase
''', conn)

conn.close()

# Export all three as CSV
df_full.to_csv('powerbi_full_data.csv',       index=False)
df_per_minute.to_csv('powerbi_per_minute.csv', index=False)
df_phases.to_csv('powerbi_phases.csv',         index=False)

print("=== Export complete! ===")
print(f"powerbi_full_data.csv     — {len(df_full)} rows")
print(f"powerbi_per_minute.csv    — {len(df_per_minute)} rows")
print(f"powerbi_phases.csv        — {len(df_phases)} rows")
print("\nAll files ready for Power BI!")