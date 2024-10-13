import zmq
import logging
import traceback
import os
import socket

# Configure logging
logging.basicConfig(
    filename='download_router.log', 
    level=logging.DEBUG, 
    format='%(asctime)s %(levelname)s %(message)s'
)

def check_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0
    
def download_router():
    
    if check_port_in_use(5557):
        logging.error("Port 5557 is already in use. Aborting router startup.")
        return
    
    if check_port_in_use(5558):
        logging.error("Port 5558 is already in use. Aborting router startup.")
        return
    
    print(f"Starting the Download Router... on PID: {os.getpid()} ready for processing")

    logging.info("Starting the Download Router...")

    try:
        context = zmq.Context()

        # ROUTER socket to receive tasks from Flask app
        frontend = context.socket(zmq.ROUTER)
        frontend.bind("tcp://*:5557")
        logging.info("ROUTER socket bound to tcp://*:5557 for Flask app.")

        # DEALER socket to forward tasks to download workers
        backend = context.socket(zmq.DEALER)
        backend.bind("tcp://*:5558")
        logging.info("DEALER socket bound to tcp://*:5558 for download workers.")

        # Start the proxy between frontend and backend
        logging.info("Starting ZMQ proxy between ROUTER (frontend) and DEALER (backend).")
        while True:
            # Poll the frontend to see if there's a message from Flask
            message = frontend.recv_multipart()
            logging.info(f"Received message from frontend: {message}")
            print(f"Received message: {message}")  # Optional print for CLI

            # Forward the message to the backend (download workers)
            backend.send_multipart(message)
            logging.info(f"Forwarded message to backend (download workers).")

    except zmq.ZMQError as e:
        logging.error(f"ZMQError occurred: {e}")
        traceback.print_exc()

    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        traceback.print_exc()

    finally:
        # Clean up sockets and context
        logging.info("Shutting down Download Router.")
        frontend.close()
        backend.close()
        context.term()
        logging.info("Download Router successfully shut down.")

if __name__ == "__main__":
    download_router()
