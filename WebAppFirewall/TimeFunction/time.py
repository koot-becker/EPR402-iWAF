import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data from the three files
files = ['time_ctf.csv', 'time_dvwa.csv', 'time_tiredful.csv']
data_ctf = pd.read_csv(files[0])
data_dvwa = pd.read_csv(files[1])
data_tiredful = pd.read_csv(files[2])

# Function to plot lineplot
def plot_lineplot(data, title, ax):
    ax2 = ax.twinx()
    sns.lineplot(x=data.index, y='time', data=data, color='red', label='Compute Time', ax=ax)
    sns.lineplot(x=data.index, y='rtt', data=data, color='blue', label='Round Trip Time', ax=ax2)
    
    ax.set_title(title)
    ax.set_ylabel('Compute Time (s)')
    ax2.set_ylabel('Round Trip Time (s)')
    ax.set_xlabel('Index')
    
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper right')
    ax.legend().remove()

# Function to plot statistical plots
def plot_statistical(data, title, axs):
    # Histogram of 'time'
    sns.histplot(data['time'], kde=True, color='red', ax=axs[0, 0])
    axs[0, 0].set_title(f'Histogram of Compute Time ({title})')
    axs[0, 0].set_ylabel('Frequency')
    axs[0, 0].set_xlabel('Time (s)')

    # Scatter plot of 'time'
    sns.scatterplot(x=data.index, y='time', data=data, color='red', ax=axs[0, 1])
    axs[0, 1].set_title(f'Scatter Plot of Compute Time ({title})')
    axs[0, 1].set_ylabel('Time (s)')
    axs[0, 1].set_xlabel('Index')

    # Boxplot of 'time'
    sns.boxplot(y=data['time'], color='red', ax=axs[0, 2])
    axs[0, 2].set_title(f'Boxplot of Compute Time ({title})')
    axs[0, 2].set_ylabel('Time (s)')

    # Histogram of 'rtt'
    sns.histplot(data['rtt'], kde=True, color='blue', ax=axs[1, 0])
    axs[1, 0].set_title(f'Histogram of Round Trip Time ({title})')
    axs[1, 0].set_ylabel('Frequency')
    axs[1, 0].set_xlabel('Round Trip Time (s)')
    axs[1, 0].set_xlim([0, 100])

    # Scatter plot of 'rtt'
    sns.scatterplot(x=data.index, y='rtt', data=data, color='blue', ax=axs[1, 1])
    axs[1, 1].set_title(f'Scatter Plot of Round Trip Time ({title})')
    axs[1, 1].set_ylabel('Round Trip Time (s)')
    axs[1, 1].set_xlabel('Index')
    axs[1, 1].set_ylim([0, 100])

    # Boxplot of 'rtt'
    sns.boxplot(y=data['rtt'], color='blue', ax=axs[1, 2])
    axs[1, 2].set_title(f'Boxplot of Round Trip Time ({title})')
    axs[1, 2].set_ylabel('Round Trip Time (s)')
    axs[1, 2].set_ylim([0, 100])

# Plot lineplots
# Plot lineplots
fig, ax = plt.subplots(figsize=(10, 5))
plot_lineplot(data_ctf, 'Compute Time and Round Trip Time Over Index (CTF)', ax)
plt.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(10, 5))
plot_lineplot(data_dvwa, 'Compute Time and Round Trip Time Over Index (DVWA)', ax)
plt.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(10, 5))
plot_lineplot(data_tiredful, 'Compute Time and Round Trip Time Over Index (Tiredful)', ax)
plt.tight_layout()
plt.show()

# Plot statistical plots
# fig, axs = plt.subplots(2, 3, figsize=(18, 12))
# plot_statistical(data_ctf, 'CTF', axs)
# plt.tight_layout()
# plt.show()

# fig, axs = plt.subplots(2, 3, figsize=(18, 12))
# plot_statistical(data_dvwa, 'DVWA', axs)
# plt.tight_layout()
# plt.show()

# fig, axs = plt.subplots(2, 3, figsize=(18, 12))
# plot_statistical(data_tiredful, 'Tiredful', axs)
# plt.tight_layout()
# plt.show()