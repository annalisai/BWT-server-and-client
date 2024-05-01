# Import necessary modules
import socket  # Provides access to socket API
import time  # Provides time-related functions
import logging  # Provides logging functionality
import threading
import argparse




# CLIENT IMPLEMENTATION

# Function to validate input data
def validate_input_data(data):
    # Example: Check if the input data is a valid DNA sequence
    valid_chars = set("ATCG")
    return all(char in valid_chars for char in data)

# Function to handle socket errors
def handle_socket_error(e):
    logging.error(f"Socket error: {e}")

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

def parse_args():
    parser = argparse.ArgumentParser(description='Client for BWT server.')
    parser.add_argument('--host', default=socket.gethostname(), help='Server hostname')
    parser.add_argument('--port', type=int, help='Server port', required=True)
    parser.add_argument('--command', choices=['BWT', 'InverseBWT'], help='Command to execute', required=True)
    parser.add_argument('--data', help='Data for command execution', required=True)
    return parser.parse_args()

if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_args()

    # Start the client
    run_client(args.host, args.port, args.command, args.data)