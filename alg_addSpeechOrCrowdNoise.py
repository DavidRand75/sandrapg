import numpy as np
import librosa
import soundfile as sf
import os
import sys
import matplotlib.pyplot as plt
from pydub import AudioSegment

def adjust_noise_length(noise, target_length):
    """Repeat or trim the noise to match the target audio length."""
    if len(noise) < target_length:
        loop_count = target_length // len(noise) + 1
        noise = np.tile(noise, loop_count)
    return noise[:target_length]

def run_add_speech_noise(input_file, output_dir, noise_file='crowd_chatter.wav'):
    # Load the original audio file
    y, sr = librosa.load(input_file, sr=None)
    
    # Load the speech noise (crowd chatter)
    noise_audio = AudioSegment.from_wav(noise_file)
    noise_audio = np.array(noise_audio.get_array_of_samples(), dtype=np.float32)
    
    # Adjust the noise length to match the original audio length
    noise_audio = adjust_noise_length(noise_audio, len(y))

    # Scale down the noise (reduce volume)
    noise_audio *= 0.05  # Adjust this factor to control the noise level

    # Add the noise to the original audio
    noisy_audio = y + noise_audio

    # Save the noisy audio
    output_file = os.path.join(output_dir, f"added_speech_noise_{os.path.basename(input_file)}")
    sf.write(output_file, noisy_audio, sr)

    # Time array for plotting
    time = np.linspace(0, len(y) / sr, len(y))

    # Generate plots
    plot_and_save(time, y, noisy_audio, 'speech', output_dir)

def plot_and_save(time, y, noisy_audio, noise_type, output_dir):
    """Generate and save plots for the original, noisy, and comparison signals."""
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

    run_add_speech_noise(file_path, output_directory)
