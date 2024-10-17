import os
import sys
from pydub import AudioSegment
import argparse

def convert_and_split_audio(input_file, output_folder):
    # Ensure the output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Extract the original filename (without extension)
    filename = os.path.splitext(os.path.basename(input_file))[0]
    
    # Convert m4a to wav using pydub
    audio = AudioSegment.from_file(input_file, format="m4a")
    
    # Set chunk duration (60 seconds max)
    chunk_duration = 60 * 1000  # pydub works in milliseconds
    
    total_duration = len(audio)
    num_chunks = (total_duration // chunk_duration) + 1

    # Split and export chunks
    for i in range(num_chunks):
        start_time = i * chunk_duration
        end_time = min((i + 1) * chunk_duration, total_duration)
        
        chunk = audio[start_time:end_time]
        
        # Calculate the time in seconds for naming
        start_seconds = start_time // 1000
        end_seconds = end_time // 1000
        
        # Create the output filename
        output_filename = f"{filename}_start{start_seconds}_end{end_seconds}_chunk{i + 1}.wav"
        output_path = os.path.join(output_folder, output_filename)
        
        # Export the chunk as a .wav file
        chunk.export(output_path, format="wav")
        print(f"Exported {output_filename}")

if __name__ == "__main__":
    file_path = sys.argv[1]  # Input file path
    output_directory = sys.argv[2]  # Output directory path

    convert_and_split_audio(file_path, output_directory)
