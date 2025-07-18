import unittest
from unittest.mock import patch, MagicMock
from your_module import deploy_kubernetes_app  # Update with actual import path

class TestKubernetesTool(unittest.TestCase):
    
    @patch("your_module.client.CoreV1Api")  
    @patch("your_module.client.AppsV1Api")  
    @patch("your_module.config.load_kube_config")  
    def test_kubernetes_deployment_success(self, mock_config, mock_apps_v1, mock_core_v1):
        """Test successful Kubernetes deployment."""
        mock_core_v1.return_value.list_namespace.return_value.items = [MagicMock(metadata=MagicMock(name="my-namespace"))]
        mock_apps_v1.return_value.create_namespaced_deployment.return_value = MagicMock()
        mock_core_v1.return_value.create_namespaced_service.return_value = MagicMock()

        result = deploy_kubernetes_app(namespace="my-namespace", image="nginx", replicas=1)
        self.assertEqual(result, "Kubernetes deployment and service created successfully.")

    @patch("your_module.client.CoreV1Api")
    def test_kubernetes_invalid_namespace(self, mock_core_v1):
        """Test failure when namespace does not exist."""
        mock_core_v1.return_value.list_namespace.return_value.items = []

        result = deploy_kubernetes_app(namespace="wrong-namespace", image="nginx", replicas=1)
        self.assertIn("Namespace 'wrong-namespace' does not exist", result)

if __name__ == "__main__":
    unittest.main()
