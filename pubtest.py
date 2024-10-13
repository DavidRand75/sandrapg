import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.PUSH)

# Try binding to a port
try:
    socket.bind("tcp://*:5556")  # Use the desired port
    print("Socket successfully bound to port 5555")
except zmq.ZMQError as e:
    print(f"Failed to bind to port 5555: {e}")

time.sleep(1)  # Wait a bit to allow subscribers to connect

while True:
    task_to_push = {
                    'file': "test file",
                    'algorithm': "test algo"
                }
    socket.send_json(task_to_push)
    print(f"Sent: {task_to_push}")
    time.sleep(2)  # Send a message every 2 seconds
