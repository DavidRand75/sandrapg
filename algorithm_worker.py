import zmq
import os
import subprocess
import logging
import traceback
import json

# Configure logging
logging.basicConfig(filename='algorithmworker.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s %(message)s')

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
        # Run the corresponding Python script for the algorithm
        result = subprocess.run(
            ["python", "dummyAlg.py", file_path],
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
