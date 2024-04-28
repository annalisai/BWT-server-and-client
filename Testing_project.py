# Unit tests
# Define unit tests for BWT functions and server-client system
class TestBWTFunctions(unittest.TestCase):
    def test_bwt_transform(self):
        result = run_single_client("BWT", "ATGC")
        print(f"Actual result (bwt_transform): {result}")
        self.assertEqual(result, "C$GTA")

    def test_inverse_bwt_transform(self):
        result = run_single_client("InverseBWT", "CATG$")
        print(f"Actual result (inverse_bwt_transform): {result}")
        self.assertEqual(result, "AAAAT")

class TestServerClientSystem(unittest.TestCase):
    def test_bwt_integration(self):
        response = run_single_client("BWT", "ATGC")
        print(f"Actual response (BWT integration): {response}")
        self.assertEqual(response, "C$GTA")

    def test_inverse_bwt_integration(self):
        response = run_single_client("InverseBWT", "CATG$")
        print(f"Actual response (inverse BWT integration): {response}")
        self.assertEqual(response, "AAAAT")

# Entry point for running unit tests
if __name__ == "__main__":
    unittest.main()
