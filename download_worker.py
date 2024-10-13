import zmq
import os
import time
from s3_manager import S3Manager

import logging
import traceback


# Configure logging
logging.basicConfig(filename='downloadworker.log', level=logging.ERROR, 
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
    context = zmq.Context()

    # PULL socket to receive download tasks
    receiver = context.socket(zmq.PULL)
    receiver.connect("tcp://localhost:5557")  # Connect to download task source

    # PUSH socket to send tasks to algorithm workers
    sender = context.socket(zmq.PUSH)
    sender.bind("tcp://localhost:5556")  # Connect to algorithm workers

    # Instantiate the S3Manager for downloading files
    print(f"Started a download worker on PID {os.getpid()}")
    logging.info(f"Worker {os.getpid()} connected to PULL socket.")



    while True:
        try:
            # Receive a download task
            task = receiver.recv_json()  # Task format: {'bucket': ..., 'file': ..., 'algorithms': [...]}
            logging.info(f"Worker {os.getpid()} received task: {task}")

            bucket = task['bucket']
            file = task['file']
            algorithms = task['algorithms']

            logging.info(f"bucket {bucket} file{file} task: {algorithms}")


            # Define local file path
            download_path = os.path.join(SHARED_DOWNLOAD_DIR, file)

            

            # Download the file
            if not os.path.exists(download_path):
                print(f"Downloading {file} from {bucket} to {download_path}")
                #s3_manager.download_file(bucket, file, download_path)
            else:
                print(f"File {file} already exists, skipping download.")

            # Once downloaded, push tasks to algorithm workers
            for algorithm in algorithms:
                task_to_push = {
                    'file': download_path,
                    'algorithm': algorithm
                }
                sender.send_json(task_to_push)
                print(f"Dispatched task for {file} with algorithm {algorithm}")
        except Exception as e:
            # Log the error with stack trace
            logging.error(f"Error in worker {os.getpid()} while processing task: {task}", exc_info=True)
            traceback.print_exc()
            print(f"Worker {os.getpid()} encountered an error: {e}")

if __name__ == "__main__":

    # Pass environment variables to S3Manager
    s3_manager = S3Manager(aws_access_key, aws_secret_key, aws_region)

    download_worker()
