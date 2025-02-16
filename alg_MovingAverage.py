import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter1d
import sys
import os
from scipy.io import wavfile

def load_wav_signal(file_path):
    """
    Loads a respiration signal from a WAV file.
    Returns the sample rate and the audio data.
    """
    sample_rate, data = wavfile.read(file_path)
    return sample_rate, data

def save_results(t, noisy_signal, smooth_envelope, output_directory):
    """
    Saves the plot and the smooth envelope data to the output directory.
    """
    # Save the plot
    plt.figure()
    plt.plot(t, noisy_signal, label='Noisy Respiration Signal')
    plt.plot(t, smooth_envelope, label='Smooth Envelope (Moving Average)', color='red', linewidth=2)
    plt.legend()
    plot_path = os.path.join(output_directory, "smooth_envelope_plot.png")
    plt.savefig(plot_path)
    plt.close()

    # Save the envelope data
    envelope_path = os.path.join(output_directory, "smooth_envelope.csv")
    np.savetxt(envelope_path, smooth_envelope, delimiter=",")

    print(f"Results saved to {output_directory}")

if __name__ == "__main__":
    # Ensure correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python script.py <file_path> <output_directory>")
        sys.exit(1)

    file_path = sys.argv[1]
    output_directory = sys.argv[2]

    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Load the signal from the WAV file
    sample_rate, noisy_signal = load_wav_signal(file_path)

    # Simulate time axis based on sample rate
    t = np.linspace(0, len(noisy_signal) / sample_rate, len(noisy_signal))

    # Step 1: Clip the negative values (set negatives to zero, leaving positive peaks only)
    positive_signal = np.where(noisy_signal > 0, noisy_signal, 0)

    # Step 2: Apply a Moving Average Filter to smooth the positive signal
    window_size = 100  # Adjust the window size as needed
    smooth_envelope = uniform_filter1d(positive_signal, size=window_size)

    # Save the results (plot and data)
    save_results(t, noisy_signal, smooth_envelope, output_directory)
