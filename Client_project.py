# Import necessary modules
import socket  # Provides access to socket API
import logging  # Provides logging functionality
import argparse

# CLIENT IMPLEMENTATION

# Function to validate input data
def validate_input_data(data):
    """
    Validate the input data to ensure it is a valid DNA sequence.
    
    Parameters:
    data (str): The input data to validate.

    Returns:
    bool: True if the input data is valid, False otherwise.
    """
    # Example: Check if the input data is a valid DNA sequence
    valid_chars = set("ATCGN$")
    return all(char in valid_chars for char in data)

# Function to handle socket errors
def handle_socket_error(e):
    """
    Log socket errors.
    
    Parameters:
    e (Exception): The exception object.
    """
    logging.error(f"Socket error: {e}")

# Funzione per inviare il messaggio terminato con il carattere speciale
def send_message(client_socket, message):
    """
    Send a message to the server.
    
    Parameters:
    client_socket (socket.socket): The client socket.
    message (str): The message to send.
    """
    try:
        # Aggiungi il carattere speciale alla fine del messaggio
        message += '\0'
        client_socket.sendall(message.encode())
        logging.info(f"Sent message: {message}")
    except Exception as e:
        logging.exception(f"Failed to send message: {e}")


# Function to run the client
def run_client(host, port, command, data):
    """
    Run the client to send a command and data to the server.
    
    Parameters:
    host (str): The server hostname.
    port (int): The server port.
    command (str): The command to execute ('BWT' or 'InverseBWT').
    data (str): The data for the command.

    Returns:
    str: The response from the server.
    """
    # Validate input data
    if not validate_input_data(data):
        logging.error("Invalid input data")
        return "Invalid input data"
    
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
            send_message(client_socket, request)

            # Receive response from server
            response = client_socket.recv(1024).decode()
            # Log response
            logging.info(f"Received response: {response}")
            return response.strip()
        except socket.error as e:
            # Handle socket errors
            handle_socket_error(e)
        except Exception as e:
            logging.exception(f"Unexpected error: {e}")


# Configure logging
logging.basicConfig(level=logging.INFO)

def parse_args():
    """
    Parse command-line arguments.
    
    Returns:
    argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Client for BWT server.')
    parser.add_argument('--host', default='127.0.0.1', help='Server hostname')
    parser.add_argument('--port', type=int, help='Server port', required=True)
    parser.add_argument('--command', choices=['BWT', 'InverseBWT'], help='Command to execute', required=True)
    #parser.add_argument('--data', help='Data for command execution', required=True)
    return parser.parse_args()

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Parse command-line arguments
    args = parse_args()

    # Prompt the user for the data input
    data = input("Please enter the data: ")

    # Start the client
    run_client(args.host, args.port, args.command, data)