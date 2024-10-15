import os
import librosa
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
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

# Function to apply spectral subtraction for noise reduction
def spectral_subtraction(input_file, output_dir):
    # Convert to WAV if needed
    wav_file = convert_to_wav(input_file)
    
    # Load the audio file
    y, sr = librosa.load(wav_file, sr=None)

    # Perform Short-Time Fourier Transform (STFT)
    stft = librosa.stft(y)
    stft_db = librosa.amplitude_to_db(np.abs(stft), ref=np.max)

    # Estimate noise spectrum from silent parts (noise floor)
    noise_estimation = np.mean(stft_db[:, :10], axis=1, keepdims=True)
    
    # Subtract noise estimate from signal (spectral subtraction)
    stft_cleaned_db = stft_db - noise_estimation
    stft_cleaned_db = np.maximum(stft_cleaned_db, -80)  # Ensure dB doesn't go below -80

    # Convert back to the time domain
    stft_cleaned = librosa.db_to_amplitude(stft_cleaned_db)
    y_cleaned = librosa.istft(stft_cleaned)

    # Save the processed audio as a WAV file
    output_wav = os.path.join(output_dir, f"processed_{os.path.basename(wav_file)}")
    sf.write(output_wav, y_cleaned, sr)

    # Plot and save before and after spectrograms
    save_spectrograms(y, y_cleaned, sr, wav_file, output_dir)

    # Save the output file in the original format if needed
    if input_file != wav_file:
        save_converted_format(input_file, output_wav, output_dir)

    return output_wav

# Function to save spectrograms separately
def save_spectrograms(original_audio, processed_audio, sr, original_file, output_dir):
    # Save Original Spectrogram
    plt.figure(figsize=(10, 6))
    librosa.display.specshow(librosa.amplitude_to_db(np.abs(librosa.stft(original_audio)), ref=np.max), sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Original Spectrogram')
    original_img = os.path.join(output_dir, f"{os.path.basename(original_file).split('.')[0]}_original_spectrogram.png")
    plt.savefig(original_img)
    plt.close()

    # Save Processed Spectrogram
    plt.figure(figsize=(10, 6))
    librosa.display.specshow(librosa.amplitude_to_db(np.abs(librosa.stft(processed_audio)), ref=np.max), sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Processed Spectrogram')
    processed_img = os.path.join(output_dir, f"{os.path.basename(original_file).split('.')[0]}_processed_spectrogram.png")
    plt.savefig(processed_img)
    plt.close()

    # Save Overlay Plot (Original vs Processed)
    plt.figure(figsize=(10, 6))
    plt.plot(original_audio, label='Original', alpha=0.7)
    plt.plot(processed_audio, label='Processed', alpha=0.7)
    plt.legend()
    plt.title('Original vs Processed Waveform')
    overlay_img = os.path.join(output_dir, f"{os.path.basename(original_file).split('.')[0]}_overlay_waveform.png")
    plt.savefig(overlay_img)
    plt.close()

    print(f"Spectrograms saved: {original_img}, {processed_img}, {overlay_img}")

# Function to save files in the original format
def save_converted_format(original_file, processed_wav_file, output_dir):
    file_format = original_file.split('.')[-1].lower()
    if file_format in ['mp3', 'm4a']:
        # Convert WAV back to original format (MP3 or M4A)
        audio = AudioSegment.from_wav(processed_wav_file)
        output_converted = os.path.join(output_dir, f"sepctral_subtraction_{os.path.basename(original_file)}")
        audio.export(output_converted, format=file_format)

# Main function for worker process
def run_spectral_subtraction_worker(input_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Apply spectral subtraction and generate outputs
    output_wav = spectral_subtraction(input_file, output_dir)
    
    print(f"Processed file saved at: {output_wav}")

# Example usage
if __name__ == "__main__":
    file_path = sys.argv[1]  # Input file path
    output_directory = sys.argv[2]  # Output directory path

    print(f"Processing {file_path}, saving results to {output_directory}")
    run_spectral_subtraction_worker(file_path, output_directory)
