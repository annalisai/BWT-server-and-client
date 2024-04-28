# Import necessary modules
import socket  # Provides access to socket API
import threading  # Provides threading support
import logging  # Provides logging functionality



# BWT IMPLEMENTATION
# Function to perform Burrows-Wheeler Transform
def bwt_transform(input_str):
    # Append '$' to the end of the input string
    input_str += "$"
    # Generate a suffix array and sort it based on suffixes

    lenght_str = range(len(input_str))
    suffix_array = (sorted(lenght_str), key=lambda i: input_str[i:])
    # Construct the BWT from the sorted suffix array
    bwt_result = ''.join(input_str[i - 1] for i in suffix_array)
    return bwt_result

    # Function to perform inverse Burrows-Wheeler Transform
def inverse_bwt_transform(bwt_str):
    # Determine the length of the input BWT string
    length = len(bwt_str)
    # Find the index of the sentinel character '$'
    sentinel_index = bwt_str.index("$")

    # Sort the BWT string to get the first column
    first_column = sorted(bwt_str)
    # Count occurrences of each character in the BWT string
    char_count = {char: 0 for char in set(bwt_str)}
    for char in bwt_str:
        char_count[char] += 1

    # Calculate the position of each character in the sorted first column
    char_position = {char: 0 for char in char_count}
    for char in first_column:
        char_position[char] += 1

    # Initialize an empty string to store the original string
    original_str = ""
    # Initialize the index with the sentinel index
    index = sentinel_index

    # Reconstruct the original string using backward traversal
    for _ in range(length):
        original_str = first_column[index] + original_str
        char = bwt_str[index]
        index = char_position[char] + bwt_str[:index].count(char)

    return original_str

# Configure logging
logging.basicConfig(level=logging.INFO)

# Function to handle socket errors
def handle_socket_error(e):
    logging.error(f"Socket error: {e}")


import socket  # Import the socket module for hostname retrieval

# Function to parse configuration (host and port)
def parse_config():
    config = {
        "host": socket.gethostname(),  # Get the hostname of the machine where the script runs
        "port": None  # Set the port to None initially
    }
    
    # Optional input for host (useful if you want to override the default hostname)
    # You can leave or remove this part depending on your needs
    host_input = input("Enter the host name (press Enter to use default): ")
    if host_input:
        config["host"] = host_input

    # Input for port with validity check
    while True:
        port_input = input("Enter the port number: ")
        try:
            port = int(port_input)
            if 0 < port < 65536:  # Check if the port is within the valid range (1-65535)
                config["port"] = port
                break
            else:
                print("Invalid port number. Please enter a number between 1 and 65535.")
        except ValueError:
            print("Invalid input. Please enter a valid number for the port.")

    return config


# Function to validate input data
def validate_input_data(data):
    # Example: Check if the input data is a valid DNA sequence
    valid_chars = set("ATCG")
    return all(char in valid_chars for char in data)


# SERVER IMPLEMENTATION

# Function to handle client requests
def handle_request(request):
    # Split the request into command and data
    command, data = request.split(':')
    try:
        # Process the request based on the command
        if command == "BWT":
            return bwt_transform(data)
        elif command == "InverseBWT":
            return inverse_bwt_transform(data)
        else:
            return "Invalid command" 
    except Exception as e:
        logging.exception(f"Error processing request: {e}")
        return "Error processing request"

# Function to run the server
def run_server(host, port):
    # Create a server socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        try:
            # Bind the server socket to the specified host and port
            server_socket.bind((host, port))
            # Listen for incoming connections
            server_socket.listen(5)
            # Log server status
            logging.info(f"Server listening on {host}:{port}")

            # Server loop to accept client connections
            while True:
                # Accept incoming client connection
                client_socket, addr = server_socket.accept()
                try:
                    # Log client connection
                    logging.info(f"Accepted connection from {addr}")
                    # Receive request from client
                    request = client_socket.recv(1024).decode()

                    # Handle request and generate response
                    response = handle_request(request)
                    # Send response to client
                    client_socket.send(response.encode())
                except (socket.error, ConnectionResetError) as e:
                    # Handle socket errors
                    handle_socket_error(e)
                finally:
                    # Close client socket
                    client_socket.close()
        except socket.error as e:
            # Handle socket errors
            handle_socket_error(e)
        except KeyboardInterrupt:
            # Log server shutdown on keyboard interrupt
            logging.info("Server interrupted. Shutting down.")


