import zmq
import logging
import traceback
import os
import socket

# Configure logging
logging.basicConfig(
    filename='algorithm_router.log', 
    level=logging.INFO, 
    format='%(asctime)s %(levelname)s %(message)s'
)

def check_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0
    
def algorithm_router():

    if check_port_in_use(5559):
        logging.info("Port 5559 is already in use. Aborting router startup.")
        return
    
    if check_port_in_use(5560):
        logging.info("Port 5560 is already in use. Aborting router startup.")
        return
    
    print(f"Starting the Algorithm Router... on PID: {os.getpid()} ready for processing")

    logging.info("Starting the Algorithm Router...")
    
    try:
        context = zmq.Context()

        # ROUTER socket to receive tasks from download workers
        frontend = context.socket(zmq.ROUTER)
        frontend.bind("tcp://*:5559")
        logging.info("ROUTER socket bound to tcp://*:5559 for download workers.")

        # DEALER socket to forward tasks to algorithm workers
        backend = context.socket(zmq.DEALER)
        backend.bind("tcp://*:5560")
        logging.info("DEALER socket bound to tcp://*:5560 for algorithm workers.")

        while True:
            # Poll the frontend to receive a message from download workers
            message = frontend.recv_multipart()
            logging.info(f"Received message from frontend (download workers): {message}")
            print(f"Received message: {message}")  # Optional print for CLI

            # Forward the message to the backend (algorithm workers)
            backend.send_multipart(message)
            logging.info(f"Forwarded message to backend (algorithm workers).")

    except zmq.ZMQError as e:
        logging.error(f"ZMQError occurred: {e}")
        traceback.print_exc()
    
    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        traceback.print_exc()

    finally:
        # Clean up sockets and context
        logging.info("Shutting down Algorithm Router.")
        frontend.close()
        backend.close()
        context.term()
        logging.info("Algorithm Router successfully shut down.")

if __name__ == "__main__":
    algorithm_router()
