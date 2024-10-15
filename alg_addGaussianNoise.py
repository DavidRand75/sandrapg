import numpy as np
import librosa
import soundfile as sf
import os
import sys
import matplotlib.pyplot as plt

def run_add_gaussian_noise(input_file, output_dir):
    y, sr = librosa.load(input_file, sr=None)
    gaussian_noise = np.random.normal(0, 0.01, y.shape)
    noisy_audio = y + gaussian_noise

    output_file = os.path.join(output_dir, f"added_gaussian_noise_{os.path.basename(input_file)}")
    sf.write(output_file, noisy_audio, sr)

    time = np.linspace(0, len(y) / sr, len(y))
    plot_and_save(time, y, noisy_audio, 'gaussian', output_dir)

def plot_and_save(time, y, noisy_audio, noise_type, output_dir):
    plt.figure()
    plt.plot(time, y)
    plt.title('Original Signal')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.savefig(os.path.join(output_dir, f'original_signal_{noise_type}.png'))
    plt.close()

    plt.figure()
    plt.plot(time, noisy_audio)
    plt.title(f'Noisy Signal ({noise_type})')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.savefig(os.path.join(output_dir, f'noisy_signal_{noise_type}.png'))
    plt.close()

    plt.figure()
    plt.plot(time, y, label='Original Signal')
    plt.plot(time, noisy_audio, label=f'Noisy Signal ({noise_type})', alpha=0.7)
    plt.legend()
    plt.savefig(os.path.join(output_dir, f'comparison_signal_{noise_type}.png'))
    plt.close()

if __name__ == "__main__":
    file_path = sys.argv[1]
    output_directory = sys.argv[2]

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    run_add_gaussian_noise(file_path, output_directory)
