import numpy as np
import librosa
import soundfile as sf
import os
import sys
import matplotlib.pyplot as plt
import pandas as pd

# Stage 1: Rectify and smooth signal to create envelope using EMA
def create_envelope_ema(signal, sr, alpha=0.1):
    # Rectify the signal (take the absolute value)
    rectified_signal = np.abs(signal)

    # Exponential Moving Average (EMA)
    smoothed_envelope = pd.Series(rectified_signal).ewm(alpha=alpha).mean().values

    return smoothed_envelope

# Full pipeline with plot saving
def audio_processing_pipeline(input_file, output_dir, alpha=0.1):
    # Load the audio file
    y, sr = librosa.load(input_file, sr=None)

    # Stage 1: Create envelope using rectification and EMA
    envelope_signal = create_envelope_ema(y, sr, alpha)

    # Time array for plotting
    time = np.linspace(0, len(y) / sr, len(y))

    # Generate plots
    plot_and_save(time, y, envelope_signal, output_dir)

def plot_and_save(time, original_signal, envelope_signal, output_dir):
    """Generate and save the 2 requested plots."""
    base_filename = "processed_audio"

    # 1. Original Signal (Time-based)
    plt.figure()
    plt.plot(time, original_signal)
    plt.title('Original Signal (Time-based)')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.savefig(os.path.join(output_dir, f'{base_filename}_original.png'))
    plt.close()

    # 2. Comparison of Original vs Envelope Signal (Time-based)
    plt.figure()
    plt.plot(time, original_signal, label='Original Signal')
    plt.plot(time, envelope_signal, label='Envelope Signal (EMA)', color='red', alpha=0.7)
    plt.title('Original vs Envelope Signal (Time-based)')
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
