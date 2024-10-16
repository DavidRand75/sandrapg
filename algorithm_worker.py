import zmq
import os
import subprocess
import logging
import traceback
import json
from datetime import datetime
import  sys

# Configure logging
logging.basicConfig(filename='algorithmworker.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s %(message)s')


def create_algorithm_output_directory(algorithm, directory):
    # Get the current date and time as a string
    date_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create the new directory path by appending the algorithm name and date_time
    new_directory = os.path.join(directory, f"{algorithm}_out_data_{date_time}")
    logging.info(f"New directory path: {new_directory}")

    # Ensure forward slashes (optional, usually works fine on most platforms)
    out_path = new_directory.replace('\\', '/')
    logging.info(f"Output path after replacement: {out_path}")

    # Check if the new directory exists, and if not, create it
    try:
        if not os.path.exists(out_path):
            os.makedirs(out_path)
            logging.info(f"Directory created: {out_path}")
        else:
            logging.info(f"Directory already exists: {out_path}")
    except Exception as e:
        logging.error(f"Failed to create directory {out_path}: {e}")
    
    return out_path

def algorithm_worker():
    print(f"This is an algorithm worker .... on PID: {os.getpid()} ready for processing")
    context = zmq.Context()

    # DEALER socket to receive tasks from algorithm router
    receiver = context.socket(zmq.DEALER)
    receiver.connect("tcp://localhost:5560")  # Connect to algorithm router

    logging.info(f"Worker {os.getpid()} connected to ROUTER on port 5560.")
    
    while True:
        try:

            message = receiver.recv_multipart()
            
            # The first part is the routing ID, second part is the task (JSON)
            routing_id = message[0]
            task_data = message[1].decode('utf-8')  # Decode the second part to get the JSON string
        
            task = json.loads(task_data)


            file_path = task['file']
            algorithm = task['algorithm']

            logging.info(f"Worker {os.getpid()} processing {file_path} with {algorithm}")
            print(f"Worker {os.getpid()} processing {file_path} with {algorithm}")


            # Run the algorithm on the file
            run_algorithm(algorithm, file_path)

        except Exception as e:
            logging.error(f"Error in worker {os.getpid()} while processing task: {task}", exc_info=True)
            traceback.print_exc()

def run_algorithm(algorithm, file_path):
    logging.info(f"Running algorithm {algorithm} on {file_path}")
    try:
        # Check if the file doesn't already have the .py extension
        if not algorithm.endswith(".py"):
            algorithm_file = algorithm + ".py"

        # Check if the file exists in the current directory
        if os.path.exists(algorithm_file):
            print(f"Algorithm implementatiom for {algorithm_file} exists.")

            # Extract the directory path from the filename
            directory = os.path.dirname(file_path)
            logging.info(f"Directory {file_path}")
            print(f"Directory {file_path}")
            sys.stdout.flush()  # Force the buffer to flush



            out_path = create_algorithm_output_directory(algorithm, directory)
            print("~o"*20)
            print(f"out path: {out_path}")
            print("~o"*20)


            result = subprocess.run(
                ["python", algorithm_file, file_path, out_path],
                capture_output=True, text=True
            )

        else:
            print(f"Algorithm implementatiom for {algorithm_file} does not exists. running dummy")
            # Run the corresponding Python script for the algorithm
            algorithm_file = "alg_dummy.py"

            result = subprocess.run(
                ["python", algorithm_file, file_path],
                capture_output=True, text=True
            )

        logging.info(f"Algorithm {algorithm} executed on {file_path}, result: {result.stdout}")
        print(f"Algorithm {algorithm} executed on {file_path}, result: {result.stdout}")
        if result.stderr:
            logging.error(f"Algorithm {algorithm} executed with errors. Stderr: {result.stderr}")
    except Exception as e:
        logging.error(f"Error in worker {os.getpid()} while trying to run the algorithm: {algorithm}", exc_info=True)
        traceback.print_exc()

if __name__ == "__main__":
    algorithm_worker()
