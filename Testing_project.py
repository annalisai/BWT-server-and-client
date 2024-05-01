import unittest
from Client_project import run_client  # Import your client function from the client file
from Server_project import handle_request  # Import your server function from the server file

# Define unit tests for BWT functions and server-client system
class TestBWTFunctions(unittest.TestCase):
    def test_bwt_transform(self):
        # Call the client function directly with appropriate parameters
        result = run_client("localhost", 8080, "BWT", "ATGC")
        print(f"Actual result (bwt_transform): {result}")
        self.assertEqual(result, "C$GTA")

    def test_inverse_bwt_transform(self):
        # Call the client function directly with appropriate parameters
        result = run_client("localhost", 8080, "InverseBWT", "CATG$")
        print(f"Actual result (inverse_bwt_transform): {result}")
        self.assertEqual(result, "AAAAT")

class TestServerClientSystem(unittest.TestCase):
    def test_bwt_integration(self):
        # Call the server function directly with a sample request
        response = handle_request("BWT:ATGC")
        print(f"Actual response (BWT integration): {response}")
        self.assertEqual(response, "C$GTA")

    def test_inverse_bwt_integration(self):
        # Call the server function directly with a sample request
        response = handle_request("InverseBWT:CATG$")
        print(f"Actual response (inverse BWT integration): {response}")
        self.assertEqual(response, "AAAAT")

# Entry point for running unit tests
if __name__ == "__main__":
    unittest.main()

