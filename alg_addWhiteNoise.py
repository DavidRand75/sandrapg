import numpy as np
import librosa
import soundfile as sf
import os
import sys
import matplotlib.pyplot as plt

def run_add_white_noise(input_file, output_dir):
    # Load the original audio file
    y, sr = librosa.load(input_file, sr=None)

    # Generate white noise
    noise = np.random.normal(0, 0.01, y.shape)

    # Add the noise to the audio signal
    noisy_audio = y + noise

    output_file = os.path.join(output_dir, f"added_white_noise_{os.path.basename(input_file)}")
    # Save the noisy audio
    sf.write(output_file, noisy_audio, sr)

    # Generate time axis
    time = np.linspace(0, len(y) / sr, len(y))

    # Plot 1: Original Signal
    plt.figure()
    plt.plot(time, y)
    plt.title('Original Signal')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.savefig(os.path.join(output_dir, 'original_signal.png'))
    plt.close()

    # Plot 2: Noisy Signal
    plt.figure()
    plt.plot(time, noisy_audio)
    plt.title('Noisy Signal')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.savefig(os.path.join(output_dir, 'noisy_signal.png'))
    plt.close()

    # Plot 3: Both Signals on Same Plot
    plt.figure()
    plt.plot(time, y, label='Original Signal')
    plt.plot(time, noisy_audio, label='Noisy Signal', alpha=0.7)
    plt.title('Original vs Noisy Signal')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.savefig(os.path.join(output_dir, 'comparison_signal.png'))
    plt.close()

if __name__ == "__main__":
    file_path = sys.argv[1]
    output_directory = sys.argv[2]

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    print(f"Received file path: {file_path}")
    run_add_white_noise(file_path, output_directory)
