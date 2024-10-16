import numpy as np
import librosa
import soundfile as sf
import os
import sys
import matplotlib.pyplot as plt
import pandas as pd

# Stage 1: Rectify and smooth signal to create envelope
def create_envelope(signal, sr, window_size_ms=50):
    # Rectify the signal (take the absolute value)
    rectified_signal = np.abs(signal)

    # Convert to a Pandas Series to apply rolling window
    rectified_series = pd.Series(rectified_signal)

    # Calculate the rolling window size in samples
    window_size = int(sr * window_size_ms / 1000)  # Convert ms to samples

    # Apply rolling average (moving average) to smooth the rectified signal
    smoothed_envelope = rectified_series.rolling(window=window_size, min_periods=1).mean().values

    return smoothed_envelope

# Stage 2: Scale the envelope based on the peak amplitude of the original signal
def scale_envelope(original_signal, envelope_signal):
    original_max = np.max(np.abs(original_signal))  # Max amplitude of original signal
    envelope_max = np.max(envelope_signal)          # Max amplitude of envelope
    scaling_factor = original_max / envelope_max    # Calculate the scaling factor

    # Scale the envelope signal
    scaled_envelope = envelope_signal * scaling_factor
    return scaled_envelope

# Stage 3: Apply second pass smoothing to the scaled envelope
def smooth_envelope(envelope_signal, window_size_ms, sr):
    # Convert the envelope to a Pandas Series for rolling average
    envelope_series = pd.Series(envelope_signal)

    # Calculate window size for the second smoothing pass
    window_size = int(sr * window_size_ms / 1000)

    # Apply a second smoothing (rolling average)
    smoothed_envelope = envelope_series.rolling(window=window_size, min_periods=1).mean().values

    return smoothed_envelope

# Full pipeline with plot saving
def audio_processing_pipeline(input_file, output_dir, window_size_ms=50, second_pass_window_ms=100):
    # Load the audio file
    y, sr = librosa.load(input_file, sr=None)

    # Stage 1: Create envelope using rectification and rolling average
    envelope_signal = create_envelope(y, sr, window_size_ms)

    # Stage 2: Scale the envelope to match the original signal's peak amplitude
    scaled_envelope_signal = scale_envelope(y, envelope_signal)

    # Stage 3: Apply second pass of smoothing to further smooth the envelope
    smoothed_envelope_signal = smooth_envelope(scaled_envelope_signal, second_pass_window_ms, sr)

    # Time array for plotting
    time = np.linspace(0, len(y) / sr, len(y))

    # Generate plots
    plot_and_save(time, y, smoothed_envelope_signal, output_dir)

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

    # 2. Comparison of Original vs Smoothed Envelope Signal (Time-based)
    plt.figure()
    plt.plot(time, original_signal, label='Original Signal')
    plt.plot(time, envelope_signal, label='Smoothed Envelope Signal', color='red', alpha=0.7)
    plt.title('Original vs Smoothed Envelope Signal (Time-based)')
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
