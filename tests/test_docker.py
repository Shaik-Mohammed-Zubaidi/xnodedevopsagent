import unittest
from unittest.mock import patch, MagicMock
from tools import run_docker_container  # Update with actual import path

class TestDockerTool(unittest.TestCase):

    @patch("your_module.docker.from_env")
    def test_docker_deployment_success(self, mock_docker):
        """Test successful Docker container deployment."""
        mock_client = MagicMock()
        mock_docker.return_value = mock_client
        mock_client.containers.run.return_value = MagicMock(id="12345")

        result = run_docker_container(image="nginx", name="test-container", ports={"80/tcp": 8080})
        self.assertEqual(result, "Container test-container started successfully.")

    @patch("your_module.docker.from_env")
    def test_docker_image_not_found(self, mock_docker):
        """Test failure when image is not found."""
        mock_client = MagicMock()
        mock_docker.return_value = mock_client
        mock_client.containers.run.side_effect = Exception("Image not found")

        result = run_docker_container(image="invalid-image", name="test-container", ports={"80/tcp": 8080})
        self.assertIn("Error deploying Docker container", result)

if __name__ == "__main__":
    unittest.main()
