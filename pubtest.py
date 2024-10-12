import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.PUB)

# Try binding to a port
try:
    socket.bind("tcp://*:5555")  # Use the desired port
    print("Socket successfully bound to port 5555")
except zmq.ZMQError as e:
    print(f"Failed to bind to port 5555: {e}")

time.sleep(1)  # Wait a bit to allow subscribers to connect

while True:
    message = "Hello from publisher"
    socket.send_string(message)
    print(f"Sent: {message}")
    time.sleep(2)  # Send a message every 2 seconds
