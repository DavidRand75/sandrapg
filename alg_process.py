import multiprocessing
from multiprocessing import Manager
from queue import Empty
import os

def worker_task(task_queue):
    """
    Worker process task to handle file and algorithm processing.
    """
    print(f"Worker process started with PID: {os.getpid()}")

    while True:
        try:
            task = task_queue.get()

            if task is None:
                print(f"Worker {os.getpid()} received sentinel and is exiting.")
                break

            bucket, file, algorithm = task
            print(f"Processing {file} from {bucket} with {algorithm} in worker {os.getpid()}")
            # Here you would process the file (e.g., download from S3, apply algorithm)

        except Empty:
            print(f"Worker {os.getpid()} found the queue empty.")
            break
        except Exception as e:
            print(f"Worker {os.getpid()} encountered an error: {e}")


class AlgProcessManager:
    def __init__(self):
        """
        Initialize the AlgProcessManager instance.
        """
        print("Initialize the AlgProcessManager instance.")
        self.manager = Manager()  # Manager to manage shared objects
        self.task_queue = self.manager.Queue()  # Use Manager's Queue
        self.workers = []
        self.num_cores = os.cpu_count()  # Detect the number of CPU cores.
        self.manager_process = None

    def start_a_batch(self, files_and_algorithms):
        """
        Start a batch of tasks (list of (file, algorithm) tuples).
        """
        print(f"Received batch with {len(files_and_algorithms)} tasks.")

        # Clear the task queue before adding new tasks
        while not self.task_queue.empty():
            self.task_queue.get()

        # Add tasks to the queue before spawning workers
        for task in files_and_algorithms:
            print(f"Adding task: {task}")
            self.task_queue.put(task)

        # Add sentinel values after tasks are added
        num_workers = min(len(files_and_algorithms), self.num_cores * 2)
        for _ in range(num_workers):
            print("Adding sentinel to queue")
            self.task_queue.put(None)  # Sentinel value to signal worker termination

        # Spawn the workers
        self.spawn_manager_and_workers(num_workers)

    def spawn_manager_and_workers(self, num_workers):
        """
        Spawns worker processes to handle the tasks.
        """
        print(f"Spawning {num_workers} workers...")

        for _ in range(num_workers):
            worker = multiprocessing.Process(target=worker_task, args=(self.task_queue,))
            worker.start()
            self.workers.append(worker)

        # Wait for workers to finish
        for worker in self.workers:
            worker.join()
