import numpy as np
import librosa
import soundfile as sf
import os
import sys
import matplotlib.pyplot as plt
from scipy.signal import hilbert, butter, filtfilt

def compute_envelope_hilbert(signal):
    """Compute the envelope using the Hilbert transform."""
    analytic_signal = hilbert(signal)
    envelope = np.abs(analytic_signal)
    return envelope

def compute_envelope_lowpass(signal, sr, cutoff=10):
    """Compute the envelope using a lowpass filter."""
    nyquist = 0.5 * sr
    normal_cutoff = cutoff / nyquist
    b, a = butter(4, normal_cutoff, btype='low', analog=False)
    envelope = filtfilt(b, a, np.abs(signal))
    return envelope

def plot_and_save(time, y, envelope_hilbert, envelope_lowpass, output_dir):
    """Generate and save plots for original and envelope signals."""
    # 1. Original Signal
    plt.figure()
    plt.plot(time, y)
    plt.title('Original Signal')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.savefig(os.path.join(output_dir, 'original_signal.png'))
    plt.close()

    # 2. Envelope (Hilbert)
    plt.figure()
    plt.plot(time, y, label='Original Signal')
    plt.plot(time, envelope_hilbert, color='orange', label='Envelope (Hilbert)', linewidth=2)
    plt.title('Original Signal with Envelope (Hilbert)')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.savefig(os.path.join(output_dir, 'hilbert_envelope.png'))
    plt.close()

    # 3. Envelope (Lowpass)
    plt.figure()
    plt.plot(time, y, label='Original Signal')
    plt.plot(time, envelope_lowpass, color='red', label='Envelope (Lowpass)', linewidth=2)
    plt.title('Original Signal with Envelope (Lowpass)')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.savefig(os.path.join(output_dir, 'lowpass_envelope.png'))
    plt.close()

    # 4. Comparison of Both Envelopes
    plt.figure()
    plt.plot(time, y, label='Original Signal')
    plt.plot(time, envelope_hilbert, color='orange', label='Envelope (Hilbert)', linewidth=2)
    plt.plot(time, envelope_lowpass, color='red', label='Envelope (Lowpass)', linewidth=2)
    plt.title('Original vs Both Envelopes')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.savefig(os.path.join(output_dir, 'comparison_envelopes.png'))
    plt.close()

if __name__ == "__main__":
    file_path = sys.argv[1]
    output_directory = sys.argv[2]

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Load audio file
    y, sr = librosa.load(file_path, sr=None)

    # Time array
    time = np.linspace(0, len(y) / sr, len(y))

    # Compute envelopes
    envelope_hilbert = compute_envelope_hilbert(y)
    envelope_lowpass = compute_envelope_lowpass(y, sr)

    # Generate plots
    plot_and_save(time, y, envelope_hilbert, envelope_lowpass, output_directory)
