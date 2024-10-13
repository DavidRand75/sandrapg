import psutil

def find_and_close_ports(ports):
    """
    Finds and terminates any process using the specified ports.

    Args:
    - ports (list): List of port numbers to check and close.

    Prints the results for each port.
    """
    for port in ports:
        port_found = False
        for conn in psutil.net_connections(kind='inet'):
            if conn.laddr.port == port:
                port_found = True
                # Fetch the process using this connection
                process = psutil.Process(conn.pid)
                print(f"Process found on port {port}: {process.name()} (PID: {conn.pid})")
                try:
                    # Terminate the process
                    process.terminate()  # You can also use process.kill() for a forceful kill
                    process.wait(timeout=5)  # Wait for the process to terminate
                    print(f"Process {process.name()} (PID: {conn.pid}) using port {port} has been terminated.")
                except psutil.NoSuchProcess:
                    print(f"Process using port {port} no longer exists.")
                except Exception as e:
                    print(f"Failed to terminate process using port {port}: {e}")
                break  # No need to check further connections for this port

        if not port_found:
            print(f"No process found using port {port}.")


if __name__ == "__main__":
    ports_to_check = [5557, 5558, 5559, 5560]  # Define the list of ports to check
    print(f"Checking the following ports: {ports_to_check}")
    find_and_close_ports(ports_to_check)
