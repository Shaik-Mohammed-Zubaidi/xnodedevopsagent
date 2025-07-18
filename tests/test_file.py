import unittest
from unittest.mock import patch
from tools import save_to_file  # Update with actual import path

class TestFileSaveTool(unittest.TestCase):

    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_save_to_file_success(self, mock_open):
        """Test successful file saving."""
        result = save_to_file("test.txt", "Hello World")
        self.assertEqual(result, "File saved successfully.")

    @patch("builtins.open", side_effect=Exception("Permission denied"))
    def test_save_to_file_failure(self, mock_open):
        """Test failure when file cannot be written."""
        result = save_to_file("test.txt", "Hello World")
        self.assertIn("Error saving file", result)

if __name__ == "__main__":
    unittest.main()
