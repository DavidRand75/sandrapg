import numpy as np
import librosa
import soundfile as sf
import os
import sys
import matplotlib.pyplot as plt

def generate_pink_noise(size):
    uneven = np.random.randn(size // 2 + 1) + 1j * np.random.randn(size // 2 + 1)
    s = np.concatenate([uneven, np.conj(uneven[-2:0:-1])])
    y = np.fft.ifft(s).real
    y = y / np.max(np.abs(y))
    return y[:size]

def run_add_pink_noise(input_file, output_dir):
    y, sr = librosa.load(input_file, sr=None)
    pink_noise = generate_pink_noise(len(y)) * 0.01
    noisy_audio = y + pink_noise

    output_file = os.path.join(output_dir, f"added_pink_noise_{os.path.basename(input_file)}")
    sf.write(output_file, noisy_audio, sr)

    time = np.linspace(0, len(y) / sr, len(y))
    plot_and_save(time, y, noisy_audio, 'pink', output_dir)

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

    run_add_pink_noise(file_path, output_directory)
