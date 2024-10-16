import numpy as np
import librosa
import soundfile as sf
import os
import sys
import matplotlib.pyplot as plt
import pandas as pd

# Stage 1: Rectify and smooth signal to create envelope
def create_envelope(signal, sr, window_size_ms=50):
    rectified_signal = np.abs(signal)
    rectified_series = pd.Series(rectified_signal)
    window_size = int(sr * window_size_ms / 1000)  # Convert ms to samples
    smoothed_envelope = rectified_series.rolling(window=window_size, min_periods=1).mean().values
    return smoothed_envelope

# Stage 2: Apply multi-pass smoothing for cleaner envelope
def multi_pass_smoothing(envelope_signal, sr, pass1_ms=50, pass2_ms=100, pass3_ms=150):
    envelope_pass1 = create_envelope(envelope_signal, sr, pass1_ms)
    envelope_pass2 = create_envelope(envelope_pass1, sr, pass2_ms)
    envelope_pass3 = create_envelope(envelope_pass2, sr, pass3_ms)
    return envelope_pass3

# Stage 3: Detect audio chunks
def detect_audio_chunks(envelope_signal, sr, threshold_percent=0.05, min_chunk_duration_ms=100):
    max_value = np.max(envelope_signal)
    threshold = threshold_percent * max_value
    min_chunk_samples = int(sr * min_chunk_duration_ms / 1000)
    
    chunks = []
    in_chunk = False
    chunk_start = 0
    
    for i in range(10, len(envelope_signal) - 10):
        if envelope_signal[i] > threshold:
            if not in_chunk and np.all(np.diff(envelope_signal[i:i + 10]) > 0):
                chunk_start = i
                in_chunk = True
            elif in_chunk and np.all(np.diff(envelope_signal[i:i + 10]) < 0):
                chunk_end = i
                if chunk_end - chunk_start >= min_chunk_samples:
                    chunks.append((chunk_start, chunk_end))
                in_chunk = False
    return chunks

# Stage 4: Extract audio chunks with separate start and end padding
def save_audio_chunks(original_signal, chunks, sr, file_name, output_dir, start_padding_ms=400, end_padding_ms=1000):
    start_padding_samples = int(sr * start_padding_ms / 1000)
    end_padding_samples = int(sr * end_padding_ms / 1000)

    for idx, (start, end) in enumerate(chunks):
        # Apply separate padding before and after the chunk
        shifted_start = max(0, start - start_padding_samples)
        shifted_end = min(len(original_signal), end + end_padding_samples)
        
        # Extract the chunk using the shifted start and end
        chunk_signal = original_signal[shifted_start:shifted_end]
        
        # Save the chunk as a WAV file
        chunk_file = os.path.join(output_dir, f'{file_name}_chunk{idx + 1}.wav')
        sf.write(chunk_file, chunk_signal, sr)
        
        # Save corresponding plot for the chunk
        time = np.linspace(shifted_start / sr, shifted_end / sr, len(chunk_signal))  # Align plot to real time
        plt.figure()
        plt.plot(time, chunk_signal)
        plt.title(f'Chunk {idx + 1} (with {start_padding_ms} ms start padding, {end_padding_ms} ms end padding)')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Amplitude')
        plt.savefig(os.path.join(output_dir, f'{file_name}_chunk{idx + 1}.png'))
        plt.close()

# Full pipeline
def audio_processing_pipeline(input_file, output_dir, window_size_ms=50, threshold_percent=0.05, min_chunk_duration_ms=100, start_padding_ms=400, end_padding_ms=1000):
    y, sr = librosa.load(input_file, sr=None)
    file_name = os.path.splitext(os.path.basename(input_file))[0]

    # Stage 1: Create envelope using rectification and rolling average
    envelope_signal = create_envelope(y, sr, window_size_ms)

    # Stage 2: Apply multi-pass smoothing to create a smoother envelope
    smoothed_envelope_signal = multi_pass_smoothing(envelope_signal, sr)

    # Stage 3: Detect audio chunks based on dynamic threshold
    chunks = detect_audio_chunks(smoothed_envelope_signal, sr, threshold_percent, min_chunk_duration_ms)

    # Stage 4: Save audio chunks and plots with separate start and end padding
    save_audio_chunks(y, chunks, sr, file_name, output_dir, start_padding_ms, end_padding_ms)

# Main script usage
if __name__ == "__main__":
    file_path = sys.argv[1]
    output_directory = sys.argv[2]
    start_padding_ms = int(sys.argv[3]) if len(sys.argv) > 3 else 400  # Default start padding of 400ms
    end_padding_ms = int(sys.argv[4]) if len(sys.argv) > 4 else 1000  # Default end padding of 1000ms

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Run the full audio processing pipeline
    audio_processing_pipeline(file_path, output_directory, start_padding_ms=start_padding_ms, end_padding_ms=end_padding_ms)
