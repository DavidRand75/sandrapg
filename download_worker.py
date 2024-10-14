import zmq
import os
import time
from s3_manager import S3Manager
import json


import logging
import traceback

# Configure logging
logging.basicConfig(filename='downloadworker.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s %(message)s')

import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Retrieve environment variables
aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_DEFAULT_REGION')

SHARED_DOWNLOAD_DIR = os.getenv('SHARED_DOWNLOAD_DIR', '/tmp/shared_audio_files')

def download_worker():
    global s3_manager

    context = zmq.Context()  # Reuse the same context for all sockets

    # DEALER socket to receive tasks from the ROUTER (task distributor)
    dealerDownloaders = context.socket(zmq.DEALER)
    dealerDownloaders.connect("tcp://localhost:5558")  # Connect to the ROUTER for download workers

    # DEALER socket to send tasks to algorithm workers via another ROUTER
    routerAlgorithm = context.socket(zmq.DEALER)
    routerAlgorithm.connect("tcp://localhost:5559")  # Connect to ROUTER for algorithm workers

    # Instantiate the S3Manager for downloading files
    print(f"Started a download worker... on PID {os.getpid()} ready for processing")
    logging.info(f"Worker {os.getpid()} connected to ROUTER sockets.")

    while True:
        try:

             # Receive a multipart message from the ROUTER
            message = dealerDownloaders.recv_multipart()
            
            # The first part is the routing ID, second part is the task (JSON)
            routing_id = message[0]
            task_data = message[1].decode('utf-8')  # Decode the second part to get the JSON string
            
            # Now, parse the JSON data
            task = json.loads(task_data)  # Convert the string back to JSON
            logging.info(f"Worker {os.getpid()} received task: {task}")

            bucket = task['bucket']
            file = task['file']
            algorithms = task['algorithms']

            logging.info(f"bucket: {bucket}, file: {file}, task: {algorithms}")

            # Define local file path
            download_path = os.path.join(SHARED_DOWNLOAD_DIR, file)

            # Normalize to forward slashes
            download_path = download_path.replace("\\", "/")

            # Download the file from S3 if it doesn't already exist
            if not os.path.exists(download_path):
                print(f"Downloading {file} from {bucket} to {download_path}")
                # Uncomment the following line to enable actual S3 download
                s3_manager.download_file(bucket, file, download_path)
            else:
                print(f"File {file} already exists, skipping download.")
                logging.info(f"File {file} already exists, skipping download.")

            # Once the file is downloaded, push tasks to algorithm workers
            for algorithm in algorithms:
                task_to_push = {
                    'file': download_path,
                    'algorithm': algorithm
                }
                logging.info(f"task_push {task_to_push} going to algo router")
                # Convert the message to JSON
                task_json = json.dumps(task_to_push)
                logging.info(f"task_json {task_json} going to algo router")

                # Send as multipart (including an empty routing frame if needed)
                routerAlgorithm.send(task_json.encode('utf-8'))  # No empty frame

                print(f"Dispatched task for {file} with algorithm {algorithm}")
                
        except Exception as e:
            # Log the error with stack trace
            logging.error(f"Error in worker {os.getpid()} while processing task: {task}", exc_info=True)
            traceback.print_exc()
            print(f"Worker {os.getpid()} encountered an error: {e}")

if __name__ == "__main__":
    # Pass environment variables to S3Manager
    s3_manager = S3Manager(aws_access_key, aws_secret_key, aws_region)

    # Ensure the shared directory exists before starting
    os.makedirs(SHARED_DOWNLOAD_DIR, exist_ok=True)

    download_worker()
