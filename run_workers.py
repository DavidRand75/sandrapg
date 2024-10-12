import subprocess
import os
import platform
from flask import Flask, jsonify, request

app = Flask(__name__)

# List to track worker PIDs
worker_pids = []

# Function to start a worker
def start_worker(worker_count=4, create_console=False):
    """Start a number of worker processes and store their PIDs."""
    global worker_pids

    for _ in range(worker_count):
        if platform.system() == 'Windows':
            if not create_console:
                # On Windows, open a process without a new console
                process = subprocess.Popen(["python", "algorithm_worker.py"], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
            else:
                print("open console mode")
                # On Windows, open a new console window for each worker
                process = subprocess.Popen(
                    ["python", "algorithm_worker.py"],
                    creationflags=subprocess.CREATE_NEW_CONSOLE  # Open a new console window
                )
        else:
            # On Linux/macOS, just spawn the process
            process = subprocess.Popen(["python3", "algorithm_worker.py"])
        
        # Store the PID of the worker
        worker_pids.append(process.pid)
        print(f"Started worker with PID: {process.pid}")

    return worker_pids

if __name__ == '__main__':
    # Start the worker with console mode enabled
    start_worker(create_console=True)
