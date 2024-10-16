'''
Empirical Mode Decomposition (EMD):
EMD is a method that breaks down a signal into a finite number of intrinsic mode functions (IMFs), 
which represent different frequency components of the signal. 
The sum of these IMFs gives the original signal back. 
This method adapts well to non-linear and non-stationary signals like respiration data.
After decomposition, you can combine the lower frequency IMFs to reconstruct a smooth version of the signal.
The last few IMFs can represent the general trend or envelope of the signal.
'''

import numpy as np
import matplotlib.pyplot as plt
from PyEMD import EMD
import sys
import os

def load_signal(file_path):
    """
    Loads a respiration signal from a text or CSV file.
    Assumes the file contains one column of data points.
    """
    # For example, if the file contains a column of values
    return np.loadtxt(file_path)

def save_results(t, noisy_signal, smooth_envelope, output_directory):
    """
    Saves the plot and the envelope data to the output directory.
    """
    # Save the plot
    plt.figure()
    plt.plot(t, noisy_signal, label='Noisy Respiration Signal')
    plt.plot(t, smooth_envelope, label='Smooth Envelope', color='red', linewidth=2)
    plt.legend()
    plot_path = os.path.join(output_directory, "smooth_envelope_plot.png")
    plt.savefig(plot_path)
    plt.close()

    # Save the envelope data
    envelope_path = os.path.join(output_directory, "smooth_envelope.csv")
    np.savetxt(envelope_path, smooth_envelope, delimiter=",")

    print(f"Results saved to {output_directory}")

if __name__ == "__main__":
    import sys

    # Ensure correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python script.py <file_path> <output_directory>")
        sys.exit(1)

    file_path = sys.argv[1]
    output_directory = sys.argv[2]

    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Load the signal
    noisy_signal = load_signal(file_path)

    # Simulate time axis (adjust based on actual sampling rate, etc.)
    t = np.linspace(0, 10, len(noisy_signal))

    # Apply EMD
    emd = EMD()
    IMFs = emd.emd(noisy_signal)

    # Sum the low-frequency IMFs for a smooth envelope (e.g., the last few IMFs)
    smooth_envelope = np.sum(IMFs[-2:], axis=0)

    # Save the results (plot and data)
    save_results(t, noisy_signal, smooth_envelope, output_directory)

