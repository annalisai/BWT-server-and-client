import time
import unittest
import socket
import threading
from unittest.mock import patch
from Client_project import run_client  # Import your client function from the client file
from Server_project import run_server, handle_request, start_server, stop_server 

#UniTest for the connection Server-Client
class TestClientServerConnection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Imposta l'ambiente di test avviando il server in un thread separato.
        """
        cls.host = "127.0.0.1"
        cls.port = 8080

        # Start the server in a separate thread
        cls.stop_event, cls.server_thread = start_server(cls.host, cls.port)
        time.sleep(1)  # Give the server some time to start

        # Check if the server is running before running tests
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex((cls.host, cls.port)) != 0:
                raise RuntimeError("Server is not running")
            
    @classmethod
    def tearDownClass(cls):
        """
        Pulisci dopo i test.
        """
        # Ferma il server
        stop_server(cls.stop_event, cls.server_thread)

    def test_connection(self):
        """
        Test the client connection to the server.
        """
        # Test the client connection to the server
        response = run_client("127.0.0.1", 8080, "BWT", "ATGC")
        self.assertIsNotNone(response)  # Ensure we get a response



# Define unit tests for BWT functions and server-client system
class TestBWTFunctions(unittest.TestCase):
    def test_bwt_transform(self):
        """
        Test the Burrows-Wheeler Transform function.
        """
        result = handle_request("BWT:ATGC")
        self.assertEqual(result, "C$GTA")


    def test_inverse_bwt_transform(self):
        """
        Test the inverse Burrows-Wheeler Transform function.
        """
        result = handle_request("InverseBWT:C$GTA")
        self.assertEqual(result, "ATGC")

class TestServerClientSystem(unittest.TestCase):
    def test_bwt_integration(self):
        """
        Test the BWT integration with the server-client system.
        """
        response = run_client("127.0.0.1", 8080, "BWT", "ATGC")
        self.assertEqual(response, "C$GTA")

    def test_inverse_bwt_integration(self):
        """
        Test the inverse BWT integration with the server-client system.
        """
        response = run_client("127.0.0.1", 8080, "InverseBWT", "C$GTA")
        self.assertEqual(response, "ATGC")

class TestInputValidation(unittest.TestCase):
    def test_valid_input(self):
        """
        Test the client with valid input.
        """
        response = run_client("127.0.0.1", 8080, "BWT", "ATGC")
        self.assertNotEqual(response, "Invalid input data")

    def test_invalid_input(self):
        """
        Test the client with invalid input.
        """
        response = run_client("127.0.0.1", 8080, "BWT", "XYZ")
        self.assertEqual(response, "Invalid input data")
    
    def test_empty_input(self):
        """
        Test the client with empty input.
        """
        response = run_client("127.0.0.1", 8080, "BWT", "")
        self.assertEqual(response, "Invalid input data")

    def test_short_input(self):
        """
        Test the client with a short input.
        """
        response = run_client("127.0.0.1", 8080, "BWT", "A")
        self.assertNotEqual(response, "Invalid input data")
        self.assertEqual(response, "A$")

    def test_long_input(self):
        """
        Test the client with a long input.
        """
        long_input = "ATCG" * 1000
        response = run_client("127.0.0.1", 8080, "BWT", long_input)
        self.assertNotEqual(response, "Invalid input data")

    def test_invalid_command(self):
        """
        Test the client with an invalid command.
        """
        response = run_client("127.0.0.1", 8080, "INVALID", "ATGC")
        self.assertEqual(response, "Invalid command")

# Entry point for running unit tests
if __name__ == "__main__":
    unittest.main()

