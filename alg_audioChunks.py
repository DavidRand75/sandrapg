import numpy as np
import librosa
import soundfile as sf
import os
import sys
import matplotlib.pyplot as plt
import pandas as pd

# Stage 1: Rectify and smooth signal to create envelope
def create_envelope(signal, sr, window_size_ms=50):
    # Rectify the signal (take the absolute value)
    rectified_signal = np.abs(signal)

    # Convert to a Pandas Series to apply rolling window
    rectified_series = pd.Series(rectified_signal)

    # Calculate the rolling window size in samples
    window_size = int(sr * window_size_ms / 1000)  # Convert ms to samples

    # Apply rolling average (moving average) to smooth the rectified signal
    smoothed_envelope = rectified_series.rolling(window=window_size, min_periods=1).mean().values

    return smoothed_envelope

# Stage 2: Apply multi-pass smoothing for cleaner envelope
def multi_pass_smoothing(envelope_signal, sr, pass1_ms=50, pass2_ms=100, pass3_ms=150):
    # First smoothing pass
    envelope_pass1 = create_envelope(envelope_signal, sr, pass1_ms)
    
    # Second smoothing pass
    envelope_pass2 = create_envelope(envelope_pass1, sr, pass2_ms)

    # Third smoothing pass
    envelope_pass3 = create_envelope(envelope_pass2, sr, pass3_ms)

    return envelope_pass3

# Stage 3: Detect audio chunks based on dynamic threshold and peaks
def detect_audio_chunks(envelope_signal, sr, threshold_percent=0.05, min_chunk_duration_ms=100):
    # Calculate the threshold as 5% of the maximum value after smoothing
    max_value = np.max(envelope_signal)
    threshold = threshold_percent * max_value
    
    # Convert durations from ms to samples
    padding_samples = int(sr * 5 / 1000)
    min_chunk_samples = int(sr * min_chunk_duration_ms / 1000)
    
    chunks = []
    in_chunk = False
    chunk_start = 0
    
    # Loop over the envelope to find chunks
    for i in range(10, len(envelope_signal) - 10):
        if envelope_signal[i] > threshold:
            # Detect the start of the chunk (going up the hill)
            if not in_chunk and np.all(np.diff(envelope_signal[i:i + 10]) > 0):
                chunk_start = max(0, i - padding_samples)
                in_chunk = True
            # Detect the end of the chunk (going down the hill)
            elif in_chunk and np.all(np.diff(envelope_signal[i:i + 10]) < 0):
                chunk_end = min(len(envelope_signal), i + padding_samples)
                # Only add chunk if its duration is above the minimum threshold
                if chunk_end - chunk_start >= min_chunk_samples:
                    chunks.append((chunk_start, chunk_end))
                in_chunk = False

    return chunks

# Stage 4: Extract audio chunks and save as separate files
def save_audio_chunks(original_signal, chunks, sr, file_name, output_dir):
    for idx, (start, end) in enumerate(chunks):
        chunk_signal = original_signal[start:end]
        chunk_file = os.path.join(output_dir, f'{file_name}_chunk{idx + 1}.wav')
        sf.write(chunk_file, chunk_signal, sr)
        
        # Save corresponding plot
        time = np.linspace(0, len(chunk_signal) / sr, len(chunk_signal))
        plt.figure()
        plt.plot(time, chunk_signal)
        plt.title(f'Chunk {idx + 1}')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Amplitude')
        plt.savefig(os.path.join(output_dir, f'{file_name}_chunk{idx + 1}.png'))
        plt.close()

# Full pipeline
def audio_processing_pipeline(input_file, output_dir, window_size_ms=50, threshold_percent=0.05, min_chunk_duration_ms=100):
    # Load the audio file
    y, sr = librosa.load(input_file, sr=None)
    file_name = os.path.splitext(os.path.basename(input_file))[0]

    # Stage 1: Create envelope using rectification and rolling average
    envelope_signal = create_envelope(y, sr, window_size_ms)

    # Stage 2: Apply multi-pass smoothing to create a smoother envelope
    smoothed_envelope_signal = multi_pass_smoothing(envelope_signal, sr)

    # Stage 3: Detect audio chunks based on dynamic threshold
    chunks = detect_audio_chunks(smoothed_envelope_signal, sr, threshold_percent, min_chunk_duration_ms)

    # Stage 4: Save audio chunks and their corresponding plots
    save_audio_chunks(y, chunks, sr, file_name, output_dir)

# Main script usage
if __name__ == "__main__":
    file_path = sys.argv[1]
    output_directory = sys.argv[2]

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Run the full audio processing pipeline
    audio_processing_pipeline(file_path, output_directory)
