import subprocess
import os
import platform
from flask import Flask, jsonify, request

import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Ensure the shared directory exists before starting download workers
# this is place both in main app and here we are making sure workers have the dowloand location up and ready
SHARED_DOWNLOAD_DIR = os.getenv('SHARED_DOWNLOAD_DIR', '/tmp/shared_audio_files')
os.makedirs(SHARED_DOWNLOAD_DIR, exist_ok=True)  # This runs before any worker starts

app = Flask(__name__)

# List to track worker PIDs
worker_pids = []

# Function to start a worker
def start_worker(worker_count=2, create_console=False):
    """Start a number of worker processes and store their PIDs."""
    global worker_pids

    for _ in range(worker_count):
        if platform.system() == 'Windows':
            if not create_console:
                # On Windows, open a process without a new console
                process = subprocess.Popen(["python", "download_worker.py"], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
            else:
                print("open console mode")
                # On Windows, open a new console window for each worker
                process = subprocess.Popen(
                    ["python", "download_worker.py"],
                    creationflags=subprocess.CREATE_NEW_CONSOLE  # Open a new console window
                )
        else:
            # On Linux/macOS, just spawn the process
            process = subprocess.Popen(["python3", "download_worker.py"])
        
        # Store the PID of the worker
        worker_pids.append(process.pid)
        print(f"Started download worker with PID: {process.pid}")

    return worker_pids

if __name__ == '__main__':
    # Start the worker with console mode enabled
    start_worker(create_console=True)
