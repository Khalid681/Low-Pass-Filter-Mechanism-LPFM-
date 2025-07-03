import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the datasets
data_433 = pd.read_csv(r'C:\Users\khalid usman\Desktop\New Folder\newdata433\433\spreading_433factor500_12.csv')
data_915 = pd.read_csv(r'C:\Users\khalid usman\Desktop\New Folder\newdata915\915\spreading_915factor500_12.csv')
 #check for different limits from the dataset for the impact of the result
start_index =1 
end_index = start_index + 200

snr_column_name = 'snr' 
if snr_column_name not in data_433.columns or snr_column_name not in data_915.columns:
    raise ValueError(f"The column '{snr_column_name}' is not present in one of the datasets.")

snr_433mhz = data_433[snr_column_name][start_index:end_index]
snr_915mhz = data_915[snr_column_name][start_index:end_index]

weight = 0.2 

def compute_avg_snr(snr_data, weight):
    avg_snr = [0] 
    for snr in snr_data:
        avg_value = (1 - weight) * avg_snr[-1] + weight * snr
        avg_snr.append(avg_value)
    return avg_snr[1:]  


avg_snr_433mhz = compute_avg_snr(snr_433mhz, weight)
avg_snr_915mhz = compute_avg_snr(snr_915mhz, weight)

intersection_points = []
for i in range(1, len(avg_snr_433mhz)):
    
    if (avg_snr_433mhz[i-1] - avg_snr_915mhz[i-1]) * (avg_snr_433mhz[i] - avg_snr_915mhz[i]) < 0:
        
        x_intersect = i - 1 + abs(avg_snr_433mhz[i-1] - avg_snr_915mhz[i-1]) / abs(avg_snr_433mhz[i] - avg_snr_915mhz[i] - (avg_snr_433mhz[i-1] - avg_snr_915mhz[i-1]))
        y_intersect = avg_snr_433mhz[i-1] + (x_intersect - (i - 1)) * (avg_snr_433mhz[i] - avg_snr_433mhz[i-1])
        #
        intersection_points.append((x_intersect, y_intersect))


shift_averages = []
for i in range(1, len(intersection_points)):
    start = int(np.floor(intersection_points[i-1][0]))
    end = int(np.floor(intersection_points[i][0]))
    avg_433 = np.mean(avg_snr_433mhz[start:end])
    avg_915 = np.mean(avg_snr_915mhz[start:end])
    shift_averages.append((i, (avg_433 + avg_915) / 2))


shift_averages = [(idx, avg_value / 1) for idx, avg_value in shift_averages]

shift_averages.sort(key=lambda x: x[1])
lowest_averages = shift_averages[:3]

plt.figure(figsize=(12, 6))
plt.plot(avg_snr_433mhz, label='433 MHz', color='blue')
plt.plot(avg_snr_915mhz, label='915 MHz', color='red')

for (x_intersect, y_intersect) in intersection_points:
    plt.scatter(x_intersect, y_intersect, color='black', s=50, label=f'Total Shifts:( {len(intersection_points)})' if intersection_points.index((x_intersect, y_intersect)) == 0 else "", zorder=5)

for (idx, avg_value) in lowest_averages:
    x_point = intersection_points[idx][0]
    y_point = intersection_points[idx][1]
    plt.scatter(x_point, y_point, color='green', s=100, label='Snr Gain' if lowest_averages.index((idx, avg_value)) == 0 else "", zorder=6)
    plt.text(x_point, y_point + 1.0, f'{avg_value:.2f}%', fontsize=12, color='black', ha='center')
    
    plt.annotate('', xy=(x_point, y_point + 1.0), xytext=(x_point, y_point),
                 arrowprops=dict(facecolor='green', arrowstyle='->', shrinkA=0, shrinkB=0, lw=1.5, mutation_scale=25), fontsize=9, color='green')

plt.xlabel('Time')
plt.ylabel(' SNR(db)')
plt.title('SF=12   BW=500khz')
plt.legend(loc='upper left')
plt.grid(True)
plt.xticks([])
plt.yticks(np.arange(2,9.12,1))
plt.show()
