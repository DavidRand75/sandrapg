import numpy as np
import librosa
import soundfile as sf
import os
import sys
import matplotlib.pyplot as plt
import noisereduce as nr
import pandas as pd

# Stage 1: Noise Reduction using Noisereduce
def noise_reduction(signal, sr):
    reduced_noise_signal = nr.reduce_noise(y=signal, sr=sr)
    return reduced_noise_signal

# Stage 2: Smoothing (can be tweaked as needed)
def smoothed_signal(signal, sr, window_size_ms, iterations=1):
    window_size = int(sr * window_size_ms / 1000)
    signal_series = pd.Series(signal)
    rectified = signal_series.abs()
    smoothed = rectified
    for _ in range(iterations):
        smoothed = smoothed.rolling(window=window_size, min_periods=1).mean()
    smoothed = smoothed.fillna(0).values
    return smoothed

# Full pipeline with plot saving
def audio_processing_pipeline(input_file, output_dir, window_size_ms=50):
    y, sr = librosa.load(input_file, sr=None)

    # Stage 1: Noise Reduction
    denoised_signal = noise_reduction(y, sr)

    # Save the denoised signal
    output_file = os.path.join(output_dir, f"denoised_{os.path.basename(input_file)}")
    sf.write(output_file, denoised_signal, sr)

    # Stage 2: Smoothing
    smoothed_signal_result = smoothed_signal(denoised_signal, sr, window_size_ms)

    # Time array for plotting
    time = np.linspace(0, len(y) / sr, len(y))

    # Generate plots
    plot_and_save(time, y, denoised_signal, smoothed_signal_result, output_dir)

def plot_and_save(time, original_signal, denoised_signal, smoothed_signal, output_dir):
    """Generate and save the 3 requested plots."""
    base_filename = "processed_audio"

    # 1. Original Signal (Time-based)
    plt.figure()
    plt.plot(time, original_signal)
    plt.title('Original Signal (Time-based)')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.savefig(os.path.join(output_dir, f'{base_filename}_original.png'))
    plt.close()

    # 2. After Noise Reduction (Time-based)
    plt.figure()
    plt.plot(time, denoised_signal)
    plt.title('Denoised Signal (Time-based)')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.savefig(os.path.join(output_dir, f'{base_filename}_denoised.png'))
    plt.close()

    # 3. Comparison of Original vs Processed (Time-based)
    plt.figure()
    plt.plot(time, original_signal, label='Original Signal')
    plt.plot(time, smoothed_signal, label='Processed Signal (Smoothed)', alpha=0.7)
    plt.title('Original vs Processed Signal (Time-based)')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.savefig(os.path.join(output_dir, f'{base_filename}_comparison.png'))
    plt.close()

# Main script usage
if __name__ == "__main__":
    file_path = sys.argv[1]
    output_directory = sys.argv[2]

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Run the full audio processing pipeline
    audio_processing_pipeline(file_path, output_directory)
