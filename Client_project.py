# Import necessary modules
import socket  # Provides access to socket API
import time  # Provides time-related functions
import logging  # Provides logging functionality




# CLIENT IMPLEMENTATION

# Function to validate input data
def validate_input_data(data):
    # Example: Check if the input data is a valid DNA sequence
    valid_chars = set("ATCG")
    return all(char in valid_chars for char in data)

# Function to run the client
def run_client(host, port, command, data):
    # Create a client socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            # Connect to the server
            client_socket.connect((host, port))
            # Log successful connection
            logging.info(f"Connecting to {host}:{port}")

            # Construct request message
            request = f"{command}:{data}"
            # Send request to server
            client_socket.send(request.encode())

            # Receive response from server
            response = client_socket.recv(1024).decode()
            # Log response
            logging.info("Response: %s", response)
        except socket.error as e:
            # Handle socket errors
            handle_socket_error(e)

# Example of run
if __name__ == "__main__":
    # Parse configuration
    config = parse_config()
    # Extract host and port from configuration
    host = config["host"]
    port = config["port"]

    # Start the server in a separate thread
    server_thread = threading.Thread(target=run_server, args=(host, port))
    server_thread.start() 

    # Allow some time for the server to start before running the client
    time.sleep(1)

    # Run the client with a sample command and data
    run_client(host, port, "BWT", "ATGC")
