import unittest
from unittest.mock import patch, MagicMock
from tools import apply_terraform  # Update with actual import path

class TestTerraformTool(unittest.TestCase):

    @patch("your_module.subprocess.run")
    def test_terraform_apply_success(self, mock_subprocess):
        """Test successful Terraform apply."""
        mock_subprocess.return_value = MagicMock(returncode=0, stdout="Apply complete.")

        result = apply_terraform(action="apply")
        self.assertEqual(result, "Terraform apply executed successfully.")

    @patch("your_module.subprocess.run")
    def test_terraform_failure(self, mock_subprocess):
        """Test Terraform failure handling."""
        mock_subprocess.side_effect = Exception("Terraform error")

        result = apply_terraform(action="apply")
        self.assertIn("Error executing Terraform", result)

if __name__ == "__main__":
    unittest.main()
