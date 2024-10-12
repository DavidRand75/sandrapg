import zmq
import time
import os

def worker():
    context = zmq.Context()

    # Create PULL socket to receive tasks from the Flask app
    receiver = context.socket(zmq.PULL)
    receiver.connect("tcp://localhost:5555")  # Connect to Flask PUSH

    print(f"Worker {os.getpid()} connected to PULL socket.")

    while True:
        task = receiver.recv_string()  # Receive task from Flask
        print(f"Worker {os.getpid()} received task: {task}")

        # Simulate file processing (replace this with your real processing logic)
        time.sleep(1)

        print(f"Worker {os.getpid()} completed task: {task}")

if __name__ == "__main__":
    worker()
