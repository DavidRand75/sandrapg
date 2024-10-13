import zmq
import os
import subprocess

import logging
import traceback


# Configure logging
logging.basicConfig(filename='algorithmworker.log', level=logging.ERROR, 
                    format='%(asctime)s %(levelname)s %(message)s')

def algorithm_worker():
    context = zmq.Context()

    # PULL socket to receive tasks from download workers
    receiver = context.socket(zmq.PULL)
    receiver.connect("tcp://localhost:5556")  # Connect to download workers' PUSH socket

    print(f"Started an algorithm worker on PID {os.getpid()}")
    logging.error(f"Started an algorithm worker on PID {os.getpid()}")

    while True:
        # Receive a task to process a file with an algorithm
        task = receiver.recv_json()  # Task format: {'file': ..., 'algorithm': ...}
        file_path = task['file']
        algorithm = task['algorithm']

        print(f"Worker {os.getpid()} processing {file_path} with {algorithm}")
        logging.error(f"Worker {os.getpid()} processing {file_path} with {algorithm}")


        # Run the algorithm on the file
        run_algorithm(algorithm, file_path)

def run_algorithm(algorithm, file_path):
    print("Running algo: ", algorithm)
    try:
        # Run the corresponding Python script for the algorithm
        '''
        result = subprocess.run(
            ["python", f"{algorithm}.py", file_path],
            capture_output=True, text=True
        )
        '''
        result = subprocess.run(
            ["python", "dummyAlg.py", file_path],
            capture_output=True, text=True
        )
        print(f"Algorithm {algorithm} executed on {file_path}, result: {result.stdout}")
    except Exception as e:
        logging.error(f"Error in worker {os.getpid()} while trying to run the algorithm: {algorithm}", exc_info=True)
        traceback.print_exc()
        print(f"Error running algorithm {algorithm} on {file_path}: {e}")

if __name__ == "__main__":
    algorithm_worker()
