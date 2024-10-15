import os
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import librosa
import librosa.display
from scipy.signal import wiener
from pydub import AudioSegment
import sys

# Function to convert non-WAV files to WAV
def convert_to_wav(input_file):
    file_format = input_file.split('.')[-1].lower()
    if file_format in ['mp3', 'm4a']:
        audio = AudioSegment.from_file(input_file, format=file_format)
        wav_file = input_file.replace(f".{file_format}", ".wav")
        audio.export(wav_file, format="wav")
        return wav_file
    return input_file

# Function to apply Wiener filtering
def wiener_filtering(input_file, output_dir):
    # Convert to WAV if needed
    wav_file = convert_to_wav(input_file)
    
    # Load the audio file
    y, sr = librosa.load(wav_file, sr=None)
    
    # Apply the Wiener filter
    filtered_signal = wiener(y)
    
    # Save the filtered audio
    output_wav = os.path.join(output_dir, f"wiener_filtered_{os.path.basename(wav_file)}")
    sf.write(output_wav, filtered_signal, sr)
    
    # Plot and save the before and after spectrograms
    save_spectrograms(y, filtered_signal, sr, wav_file, output_dir)
    
    # Save the output file in the original format if needed
    if input_file != wav_file:
        save_converted_format(input_file, output_wav, output_dir)
    
    return output_wav

# Function to save spectrograms
def save_spectrograms(original_audio, filtered_audio, sr, original_file, output_dir):
    # Spectrogram before noise removal
    plt.figure(figsize=(10, 6))
    
    # Original Spectrogram
    plt.subplot(3, 1, 1)
    D_original = librosa.amplitude_to_db(np.abs(librosa.stft(original_audio)), ref=np.max)
    librosa.display.specshow(D_original, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Original Spectrogram')
    plt.savefig(os.path.join(output_dir, f"{os.path.basename(original_file).split('.')[0]}_original_spectrogram.png"))
    
    # Filtered Spectrogram
    plt.subplot(3, 1, 2)
    D_filtered = librosa.amplitude_to_db(np.abs(librosa.stft(filtered_audio)), ref=np.max)
    librosa.display.specshow(D_filtered, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Filtered Spectrogram')
    plt.savefig(os.path.join(output_dir, f"{os.path.basename(original_file).split('.')[0]}_filtered_spectrogram.png"))
    
    # Overlay original and filtered for comparison
    plt.subplot(3, 1, 3)
    plt.plot(original_audio, label='Original')
    plt.plot(filtered_audio, label='Filtered')
    plt.legend()
    plt.title('Original vs Filtered Audio')
    plt.savefig(os.path.join(output_dir, f"{os.path.basename(original_file).split('.')[0]}_comparison.png"))
    
    plt.close()

# Function to save files in the original format
def save_converted_format(original_file, processed_wav_file, output_dir):
    file_format = original_file.split('.')[-1].lower()
    if file_format in ['mp3', 'm4a']:
        # Convert WAV back to original format (MP3 or M4A)
        audio = AudioSegment.from_wav(processed_wav_file)
        output_converted = os.path.join(output_dir, f"wiener_filtered_{os.path.basename(original_file)}")
        audio.export(output_converted, format=file_format)

# Main function for worker process
def run_wiener_filter_worker(input_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Apply Wiener filtering and generate outputs
    output_wav = wiener_filtering(input_file, output_dir)
    
    print(f"Processed file saved at: {output_wav}")

# Example usage
if __name__ == "__main__":
    file_path = sys.argv[1]  # Path of the input file passed as argument
    print(f"Received file path: {file_path}")
    output_directory = sys.argv[2]
    run_wiener_filter_worker(file_path, output_directory)
