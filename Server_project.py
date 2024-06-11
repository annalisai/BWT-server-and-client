# Import necessary modules
import socket  # Provides access to socket API
import logging  # Provides logging functionality
import threading

# BWT IMPLEMENTATION
# Function to perform Burrows-Wheeler Transform
def bwt_transform(input_str):
    """
    Perform the Burrows-Wheeler Transform on the input string.
    
    Parameters:
    input_str (str): The input string to transform.

    Returns:
    str: The transformed string.
    """
    try:
        # Append '$' to the end of the input string
        input_str += "$"
        # Generate a suffix array and sort it based on suffixes
        suffix_array = sorted(range(len(input_str)), key=lambda i: input_str[i:])

        # Construct the BWT from the sorted suffix array
        bwt_result = ''.join(input_str[i - 1] for i in suffix_array)
        return bwt_result
    except Exception as e:
        logging.exception(f"Error in BWT transform")
        return "Error in BWT transform"

# Function to perform inverse Burrows-Wheeler Transform
def inverse_bwt_transform(bwt_str):
    """
    Perform the inverse Burrows-Wheeler Transform.
    
    Parameters:
    bwt_str (str): The BWT transformed string.

    Returns:
    str: The original string before BWT.
    """
    table = [""] * len(bwt_str)
    for _ in range(len(bwt_str)):
        table = sorted([bwt_str[i] + table[i] for i in range(len(bwt_str))])
    s = [row for row in table if row.endswith("$")]
    return s[0][:-1] if s else "Error in inverse BWT transform"


# Configure logging
logging.basicConfig(level=logging.INFO)

# Function to handle socket errors
def handle_socket_error(e):
    """
    Log socket errors.
    
    Parameters:
    e (Exception): The exception object.
    """
    logging.error(f"Socket error: {e}")


# Function to validate input data
def validate_input_data(data):
    """
    Validate the input data to ensure it is a valid DNA sequence.
    
    Parameters:
    data (str): The input data to validate.

    Returns:
    bool: True if the input data is valid, False otherwise.
    """
    # Check if the input data is a valid DNA sequence
    valid_chars = set("ATCGN$")
    return all(char in valid_chars for char in data)


# SERVER IMPLEMENTATION

# Funzione per ricevere il messaggio terminato con il carattere speciale
def receive_message(client_socket):
    """
    Receive a message from the client.
    
    Parameters:
    client_socket (socket.socket): The client socket.

    Returns:
    str: The received message.
    """
    try:
        message = ""
        while True:
            # Ricevi dati dal client
            chunk = client_socket.recv(1024).decode()
            if not chunk:
                break
            message += chunk
            # Controlla se il messaggio contiene il carattere speciale di fine messaggio
            if '\0' in message:
                message = message.split('\0')[0]
                break
        logging.info(f"Received message: {message.strip()}")
        return message.strip()
    except Exception as e:
        logging.exception(f"Error receiving message: {e}")
        return ""


# Function to handle client requests
def handle_request(request):
    """
    Handle a client request.
    
    Parameters:
    request (str): The request string containing the command and data.

    Returns:
    str: The response string.
    """
    # Split the request into command and data
    command, data = request.split(':',1)
    try:
        # Process the request based on the command
        if command == "BWT":
            return bwt_transform(data)
        elif command == "InverseBWT":
            return inverse_bwt_transform(data)
        else:
            return "Invalid command" 
    except Exception as e:
        logging.exception(f"Error processing request")
        return "Error processing request"
    

def send_response(client_socket, response):
    """
    Send a response to the client.
    
    Parameters:
    client_socket (socket.socket): The client socket.
    response (str): The response to send.
    """
    try:
        response += '\0'
        client_socket.sendall(response.encode())
        logging.info(f"Sent response: {response}")
    except Exception as e:
        logging.exception(f"Failed to send response")

# Function to run the server
def run_server(host, port, stop_event):
    """
    Run the server to accept and handle client connections.
    
    Parameters:
    host (str): The server hostname.
    port (int): The server port.
    stop_event (threading.Event): Event to signal the server to stop.
    """
    # Create a server socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        try:
            # Bind the server socket to the specified host and port
            server_socket.bind((host, port))
            # Listen for incoming connections
            server_socket.listen(5)
            # Log server status
            logging.info(f"Server listening on {host}:{port}")

            while not stop_event.is_set():
                server_socket.settimeout(1.0)
                try:
                    client_socket, addr = server_socket.accept()
                except socket.timeout:
                    continue
                with client_socket:
                    logging.info(f"Accepted connection from {addr}")
                    request = receive_message(client_socket)
                    logging.info(f"Received request: {request}")
                    response = handle_request(request)
                    send_response(client_socket, response)
        except Exception as e:
            handle_socket_error(e)

def start_server(host, port):
    """
    Start the server in a separate thread.
    
    Parameters:
    host (str): The server hostname.
    port (int): The server port.

    Returns:
    tuple: The stop event and the server thread.
    """
    stop_event = threading.Event()
    server_thread = threading.Thread(target=run_server, args=(host, port, stop_event))
    server_thread.start()
    return stop_event, server_thread

def stop_server(stop_event, server_thread):
    """
    Stop the server by setting the stop event and joining the server thread.
    
    Parameters:
    stop_event (threading.Event): The event to signal the server to stop.
    server_thread (threading.Thread): The server thread.
    """
    stop_event.set()
    server_thread.join()

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Define the host and port
    host = "127.0.0.1"  
    port = 8080  

    stop_event, server_thread = start_server(host, port)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        stop_server(stop_event, server_thread)
        logging.info("Server interrupted. Shutting down.")
