import time
import psutil
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Collect data over a period of one minute
data = []
start_time = time.time()
while time.time() - start_time < 60:
    cpu_load = psutil.cpu_percent(interval=1)
    temps = psutil.sensors_temperatures()
    cpu_temp = temps['coretemp'][0].current if 'coretemp' in temps else None
    current_time = time.time() - start_time
    data.append((current_time, cpu_load, cpu_temp))

# Create a DataFrame
df = pd.DataFrame(data, columns=['Time', 'CPU_Load', 'CPU_Temperature'])

# Plot CPU load and temperature over time
fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.plot(df['Time'], df['CPU_Load'], marker='o', color='blue', label='CPU Load')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('CPU Load (%)')
ax1.grid(True)

# Create a second y-axis for the CPU temperature
ax2 = ax1.twinx()
ax2.plot(df['Time'], df['CPU_Temperature'], marker='o', color='red', label='CPU Temperature')
ax2.set_ylabel('CPU Temperature (°C)')

# Add titles and legends
plt.title('CPU Load and Temperature Over Time')
fig.tight_layout()
fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))

plt.show()

# Perform extensive statistical analysis on CPU Load
print(df[['Time', 'CPU_Load']].describe())

# Histogram of CPU Load
plt.figure(figsize=(10, 6))
sns.histplot(df['CPU_Load'], kde=True)
plt.title('Histogram of CPU Load')
plt.xlabel('CPU Load (%)')
plt.ylabel('Frequency')
plt.show()

# Scatterplot of CPU Load over Time
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Time', y='CPU_Load', data=df)
plt.title('Scatterplot of CPU Load Over Time')
plt.xlabel('Time (s)')
plt.ylabel('CPU Load (%)')
plt.grid(True)
plt.show()

# Boxplot of CPU Load
plt.figure(figsize=(10, 6))
sns.boxplot(y=df['CPU_Load'])
plt.title('Boxplot of CPU Load')
plt.ylabel('CPU Load (%)')
plt.grid(True)
plt.show()