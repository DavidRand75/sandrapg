import os
import librosa
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from pydub import AudioSegment
import sys
from datetime import datetime


# Function to convert non-WAV files to WAV
def convert_to_wav(input_file):
    file_format = input_file.split('.')[-1].lower()
    if file_format in ['mp3', 'm4a']:
        audio = AudioSegment.from_file(input_file, format=file_format)
        wav_file = input_file.replace(f".{file_format}", ".wav")
        audio.export(wav_file, format="wav")
        return wav_file
    return input_file

# Function to apply spectral gating
def spectral_gating(input_file, output_dir, noise_threshold_db=-30):
    # Convert to WAV if needed
    wav_file = convert_to_wav(input_file)
    
    # Load the audio file
    y, sr = librosa.load(wav_file, sr=None)

    # Perform Short-Time Fourier Transform (STFT)
    stft = librosa.stft(y)
    stft_db = librosa.amplitude_to_db(np.abs(stft), ref=np.max)

    # Create a noise gate mask by thresholding
    mask = stft_db > noise_threshold_db

    # Apply the mask to the STFT matrix
    gated_stft = stft * mask

    # Perform the inverse STFT to get the gated signal back
    y_gated = librosa.istft(gated_stft)

    # Save the processed audio
    output_wav = os.path.join(output_dir, f"spectral_gating_{os.path.basename(wav_file)}")
    sf.write(output_wav, y_gated, sr)

    # Plot and save before and after spectrograms
    save_spectrograms(y, y_gated, sr, wav_file, output_dir)

    # Save the output file in the original format if needed
    if input_file != wav_file:
        save_converted_format(input_file, output_wav, output_dir)

    return output_wav

# Function to save spectrograms
def save_spectrograms(original_audio, processed_audio, sr, original_file, output_dir):
    # Plot original audio
    plt.figure(figsize=(10, 6))
    plt.subplot(3, 1, 1)
    librosa.display.specshow(librosa.amplitude_to_db(np.abs(librosa.stft(original_audio)), ref=np.max), sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Original Spectrogram')

    # Plot processed audio
    plt.subplot(3, 1, 2)
    librosa.display.specshow(librosa.amplitude_to_db(np.abs(librosa.stft(processed_audio)), ref=np.max), sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Processed Spectrogram')

    # Plot both on top of each other for comparison
    plt.subplot(3, 1, 3)
    plt.plot(original_audio, label='Original')
    plt.plot(processed_audio, label='Processed')
    plt.legend()
    plt.title('Original vs Processed Audio')

    # Save the figure as a PNG file
    output_img = os.path.join(output_dir, f"{os.path.basename(original_file).split('.')[0]}_spectrograms.png")
    plt.savefig(output_img)
    plt.close()

# Function to save files in the original format
def save_converted_format(original_file, processed_wav_file, output_dir):
    file_format = original_file.split('.')[-1].lower()
    if file_format in ['mp3', 'm4a']:
        # Convert WAV back to original format (MP3 or M4A)
        audio = AudioSegment.from_wav(processed_wav_file)
        output_converted = os.path.join(output_dir, f"processed_{os.path.basename(original_file)}")
        audio.export(output_converted, format=file_format)

# Main function for worker process
def run_spectral_gating_worker(input_file, output_dir):
    # Apply spectral gating and generate outputs
    output_wav = spectral_gating(input_file, output_dir)
    
    print(f"Processed file saved at: {output_wav}")

# Example usage
if __name__ == "__main__":
    file_path = sys.argv[1]
    output_directory = sys.argv[2]

    print(f"Received file path: {file_path}")

    run_spectral_gating_worker(file_path, output_directory)
