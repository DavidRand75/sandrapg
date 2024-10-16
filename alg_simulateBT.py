import numpy as np
import librosa
import soundfile as sf
import os
import sys
import matplotlib.pyplot as plt
from pydub import AudioSegment
from scipy.signal import butter, lfilter

# Function to apply a bandpass filter (combining high-pass and low-pass filters)
def apply_bandpass(audio, sr, lowcut=300, highcut=3400, order=5):
    nyquist = 0.5 * sr
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, audio)

# Function to simulate low-bitrate compression
def apply_compression(audio, sr, bitrate='16k'):
    compressed_file = 'compressed_temp.wav'
    sf.write(compressed_file, audio, sr)
    
    # Simulate lossy compression by converting to a lower bitrate and back
    compressed_audio = AudioSegment.from_wav(compressed_file)
    compressed_audio.export(compressed_file, format="wav", bitrate=bitrate)
    
    compressed_audio = sf.read(compressed_file)[0]
    os.remove(compressed_file)
    
    return compressed_audio

# Function to simulate microphone noise
def add_microphone_noise(audio, noise_level=0.005):
    noise = np.random.normal(0, noise_level, audio.shape)
    return audio + noise

def run_bluetooth_quality_simulation(input_file, output_dir, lowcut=300, highcut=3400, noise_level=0.005, bitrate='16k'):
    # Load the original audio file
    y, sr = librosa.load(input_file, sr=None)

    # Apply bandpass filter to simulate Bluetooth's frequency range
    filtered_audio = apply_bandpass(y, sr, lowcut, highcut)

    # Simulate lossy compression
    compressed_audio = apply_compression(filtered_audio, sr, bitrate)

    # Add microphone noise
    degraded_audio = add_microphone_noise(compressed_audio, noise_level)

    # Save the degraded audio
    output_file = os.path.join(output_dir, f"bluetooth_simulation_{os.path.basename(input_file)}")
    sf.write(output_file, degraded_audio, sr)

    # Time array for plotting
    time = np.linspace(0, len(y) / sr, len(y))

    # Generate plots
    plot_and_save(time, y, degraded_audio, 'bluetooth', output_dir)

def plot_and_save(time, original_audio, degraded_audio, label, output_dir):
    """Generate and save plots for the original, degraded, and comparison signals."""
    plt.figure()
    plt.plot(time, original_audio)
    plt.title('Original Signal')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.savefig(os.path.join(output_dir, f'original_signal_{label}.png'))
    plt.close()

    plt.figure()
    plt.plot(time, degraded_audio)
    plt.title(f'Degraded Signal ({label})')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.savefig(os.path.join(output_dir, f'degraded_signal_{label}.png'))
    plt.close()

    plt.figure()
    plt.plot(time, original_audio, label='Original Signal')
    plt.plot(time, degraded_audio, label=f'Degraded Signal ({label})', alpha=0.7)
    plt.legend()
    plt.savefig(os.path.join(output_dir, f'comparison_signal_{label}.png'))
    plt.close()

if __name__ == "__main__":
    file_path = sys.argv[1]
    output_directory = sys.argv[2]

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    run_bluetooth_quality_simulation(file_path, output_directory)
