import numpy as np
import matplotlib.pyplot as plt
import librosa
import os
import sys
from scipy.ndimage import gaussian_filter1d

# Function to apply Gaussian smoothing on the envelope
def gaussian_envelope(signal, sigma=1):
    envelope = np.abs(signal)  # Take the absolute value
    smoothed_envelope = gaussian_filter1d(envelope, sigma=sigma)
    return smoothed_envelope

# Function to generate and save the envelope plots
def plot_envelope(input_file, output_dir, sigma=5):
    # Load the audio file
    signal, sr = librosa.load(input_file, sr=None)
    time = np.linspace(0, len(signal) / sr, len(signal))

    # Apply Gaussian smoothing to the envelope
    gaussian_env = gaussian_envelope(signal, sigma=sigma)

    # Plot original signal
    plt.figure()
    plt.plot(time, signal, label='Original Signal', color='blue')
    plt.title('Original Signal (Time-based)')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.savefig(os.path.join(output_dir, 'original_signal.png'))
    plt.close()

    # Plot Gaussian smoothed envelope
    plt.figure()
    plt.plot(time, gaussian_env, label='Gaussian Envelope', color='orange', linewidth=2)
    plt.title(f'Gaussian Smoothed Envelope (sigma={sigma})')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.savefig(os.path.join(output_dir, 'gaussian_envelope.png'))
    plt.close()

    # Plot both original signal and Gaussian envelope
    plt.figure()
    plt.plot(time, signal, label='Original Signal', color='blue')
    plt.plot(time, gaussian_env, label=f'Gaussian Envelope (sigma={sigma})', color='orange', linewidth=2)
    plt.title(f'Original Signal vs Gaussian Envelope (sigma={sigma})')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.savefig(os.path.join(output_dir, 'comparison_signal_gaussian.png'))
    plt.close()

# Main script usage with sys.argv inputs
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <input_audio_file> <output_directory>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_directory = sys.argv[2]

    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    plot_envelope(input_file, output_directory, sigma=5)  # You can change sigma for more or less smoothing
