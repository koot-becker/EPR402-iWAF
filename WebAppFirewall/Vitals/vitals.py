import time
import psutil
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def collect_data(duration=60):
    data = []
    start_time = time.time()
    while time.time() - start_time < duration:
        cpu_load = psutil.cpu_percent(interval=1)
        temps = psutil.sensors_temperatures()
        cpu_temp = temps['soc_thermal'][0].current if 'soc_thermal' in temps else None
        current_time = time.time() - start_time
        data.append((current_time, cpu_load, cpu_temp))
    return pd.DataFrame(data, columns=['Time', 'CPU_Load', 'CPU_Temperature'])

def plot_data(df):
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

    fig, axs = plt.subplots(1, 3, figsize=(18, 6))

    # Histogram of CPU Load
    sns.histplot(df['CPU_Load'], kde=True, ax=axs[0])
    axs[0].set_title('Histogram of CPU Load')
    axs[0].set_xlabel('CPU Load (%)')
    axs[0].set_ylabel('Frequency')

    # Scatterplot of CPU Load over Time
    sns.scatterplot(x='Time', y='CPU_Load', data=df, ax=axs[1])
    axs[1].set_title('Scatterplot of CPU Load Over Time')
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylabel('CPU Load (%)')
    axs[1].grid(True)

    # Boxplot of CPU Load
    sns.boxplot(y=df['CPU_Load'], ax=axs[2])
    axs[2].set_title('Boxplot of CPU Load')
    axs[2].set_ylabel('CPU Load (%)')
    axs[2].grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    df = collect_data(duration=300)
    df.to_pickle('vitals_data.pkl')
    # df = pd.read_pickle('vitals_data.pkl')
    # plot_data(df)