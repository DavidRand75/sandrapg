import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

# Function to resample and normalize amplitude
def resample_segment(segment, sample_rate):
    # Extract x and y values from segment
    x_values = [point[0] for segment_line in segment for point in segment_line]
    y_values = [point[1] for segment_line in segment for point in segment_line]
    
    # Resample the x-axis to match the given sample rate
    max_time = max(x_values)
    num_samples = int(max_time * sample_rate)
    x_resampled = np.linspace(0, max_time, num_samples)
    
    # Interpolate y-values across the resampled x-axis
    interp_function = interp1d(x_values, y_values, kind='linear', fill_value="extrapolate")
    y_resampled = interp_function(x_resampled)
    
    # Normalize y-values to the range [0, 1]
    y_min = np.min(y_resampled)
    y_max = np.max(y_resampled)
    y_normalized = (y_resampled - y_min) / (y_max - y_min)
    
    return x_resampled, y_normalized

# Function to save the resampled data as CSV files
def save_csv(filename, x, y):
    df = pd.DataFrame({"Time": x, "Amplitude": y})
    df.to_csv(filename, index=False)

# Input data: inhale and exhale segments
inhale_segment = [
    [(0, 0), (0.5, 0)],
    [(0.5, 0), (1, 0.5)], 
    [(1, 0.5), (2.15, 0)], 
    [(2.15, 0), (2.65, 0)]
]

exhale_segment = [
    [(2.2, 0), (2.56, 0)],
    [(2.56, 0), (3.42, 0.5)],
    [(3.42, 0.5), (4.7, 0)],
    [(4.7, 0), (5.2, 0)]
]

# Resample both segments for 48kHz and 44.1kHz, with amplitude normalization
inhale_48khz_x, inhale_48khz_y = resample_segment(inhale_segment, 48000)
exhale_48khz_x, exhale_48khz_y = resample_segment(exhale_segment, 48000)
inhale_44_1khz_x, inhale_44_1khz_y = resample_segment(inhale_segment, 44100)
exhale_44_1khz_x, exhale_44_1khz_y = resample_segment(exhale_segment, 44100)

# Save the resampled data as CSV files
save_csv("inhale_48khz.csv", inhale_48khz_x, inhale_48khz_y)
save_csv("exhale_48khz.csv", exhale_48khz_x, exhale_48khz_y)
save_csv("inhale_44.1khz.csv", inhale_44_1khz_x, inhale_44_1khz_y)
save_csv("exhale_44.1khz.csv", exhale_44_1khz_x, exhale_44_1khz_y)

# Plot the resampled segments (48kHz)
plt.figure(figsize=(10, 6))
plt.plot(inhale_48khz_x, inhale_48khz_y, 'b-', label='Inhale (48kHz)', linewidth=2)
plt.plot(exhale_48khz_x, exhale_48khz_y, 'r-', label='Exhale (48kHz)', linewidth=2)
plt.xlabel('Time (seconds)')
plt.ylabel('Normalized Amplitude (0 to 1)')
plt.title('Inhale and Exhale (48kHz)')
plt.legend()
plt.grid(True)
plt.savefig("inhale_exhale_48khz_plot.png")
plt.show()

# Plot the resampled segments (44.1kHz)
plt.figure(figsize=(10, 6))
plt.plot(inhale_44_1khz_x, inhale_44_1khz_y, 'b-', label='Inhale (44.1kHz)', linewidth=2)
plt.plot(exhale_44_1khz_x, exhale_44_1khz_y, 'r-', label='Exhale (44.1kHz)', linewidth=2)
plt.xlabel('Time (seconds)')
plt.ylabel('Normalized Amplitude (0 to 1)')
plt.title('Inhale and Exhale (44.1kHz)')
plt.legend()
plt.grid(True)
plt.savefig("inhale_exhale_44.1khz_plot.png")
plt.show()

# Plot the inhale and exhale masks separately (time domain only, normalized x-axis starting from zero)
plt.figure(figsize=(10, 6))
plt.plot(inhale_48khz_x - inhale_48khz_x[0], inhale_48khz_y, 'b-', label='Inhale Mask (48kHz)', linewidth=2)
plt.xlabel('Samples')
plt.ylabel('Amplitude')
plt.title('Inhale Mask (48kHz Time Domain)')
plt.grid(True)
plt.savefig("inhale_mask_48khz.png")
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(exhale_48khz_x - exhale_48khz_x[0], exhale_48khz_y, 'r-', label='Exhale Mask (48kHz)', linewidth=2)
plt.xlabel('Samples')
plt.ylabel('Amplitude')
plt.title('Exhale Mask (48kHz Time Domain)')
plt.grid(True)
plt.savefig("exhale_mask_48khz.png")
plt.show()
