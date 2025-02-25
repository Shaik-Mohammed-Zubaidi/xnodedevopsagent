from langchain.tools import Tool
from kubernetes import client, config

def validate_kubernetes_config(namespace, image):
    """Validates Kubernetes configuration before deployment."""
    try:
        config.load_kube_config()  # Load kubeconfig

        v1 = client.CoreV1Api()

        # Check if namespace exists
        namespaces = [ns.metadata.name for ns in v1.list_namespace().items]
        if namespace not in namespaces:
            return False, f"Namespace '{namespace}' does not exist."

        #TODO: Check if the image is accessible (basic check using Kubernetes API)
        
        return True, "Validation successful."
    
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def deploy_kubernetes_app(namespace="my-namespace", image="nginx", replicas=1):
    namespace = "my-namespace" 
    """
    Deploys a sample web application on Kubernetes.
    
    Args:
        namespace (str): Kubernetes namespace to deploy in.
        image (str): Docker image for the application.
        replicas (int): Number of replicas.
        
    Returns:
        str: Deployment status message.
    """
    try:
        # Validate configuration before applying
        is_valid, validation_message = validate_kubernetes_config(namespace, image)
        if not is_valid:
            return f"Validation failed: {validation_message}"
        # Load kubeconfig
        config.load_kube_config()  # Adjust if running inside a cluster with `config.load_incluster_config()`

        # Create Kubernetes API clients
        v1 = client.CoreV1Api()
        apps_v1 = client.AppsV1Api()

        # Define Deployment
        deployment = client.V1Deployment(
            metadata=client.V1ObjectMeta(name="sample-app"),
            spec=client.V1DeploymentSpec(
                replicas=replicas,
                selector={"matchLabels": {"app": "sample-app"}},
                template=client.V1PodTemplateSpec(
                    metadata={"labels": {"app": "sample-app"}},
                    spec=client.V1PodSpec(containers=[
                        client.V1Container(name="sample-app", image=image, ports=[client.V1ContainerPort(container_port=80)])
                    ])
                )
            )
        )

        # Define Service
        service = client.V1Service(
            metadata=client.V1ObjectMeta(name="sample-app-service"),
            spec=client.V1ServiceSpec(
                selector={"app": "sample-app"},
                ports=[client.V1ServicePort(protocol="TCP", port=80, target_port=80)],
                type="NodePort"
            )
        )

        # Apply Deployment
        apps_v1.create_namespaced_deployment(namespace=namespace, body=deployment)

        # Apply Service
        v1.create_namespaced_service(namespace=namespace, body=service)

        return "Kubernetes deployment and service created successfully."

    except Exception as e:
        return f"Error deploying to Kubernetes: {str(e)}"


# Register tool in LangChain
kubernetes_tool = Tool(
    name="KubernetesDeployer",
    func=deploy_kubernetes_app,
    description="Deploys a web application to a Kubernetes cluster."
)

# Docker Tool

from langchain.tools import Tool
import subprocess


def run_command(command):
    """Run shell commands and return output."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error executing {command}: {e.stderr}"

def build_docker_image(app_name="hello-world-app", dockerfile_path="."):
    """Build the Docker image for the app."""
    command = f"cd agentcode && docker build -t {app_name}:latest {dockerfile_path}"
    return run_command(command)

def list_docker_images():
    """List all available Docker images."""
    return run_command("docker images")

def remove_docker_image(app_name="hello-world-app"):
    """Remove the Docker image."""
    command = f"docker rmi {app_name}:latest"
    return run_command(command)

def run_docker_container(app_name="hello-world-app", dockerfile_path="."):
    build_docker_image(app_name, dockerfile_path)
    """Run a container from the built image."""
    command = f"docker run -d --name {app_name}-container {app_name}:latest"
    return run_command(command)


# Define the tool for the AI agent
docker_tool = Tool(
    name="DockerTool",
    func=run_docker_container,
    description="Builds a Docker image for the given application before Kubernetes deployment."
)


# Saving content to file tool
import os

def save_to_file(content, file_path):
    """Save content to a file, creating necessary folders if they don't exist."""
    try:
        # Extract directory path
        folder_path = os.path.dirname(file_path)
        
        # Create the folder if it does not exist
        if folder_path and not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Write the file
        with open(file_path, "w") as file:
            file.write(content)

        return f"Content saved to {file_path}"
    except Exception as e:
        return f"Error saving content to file: {str(e)}"

# Define the tool for the AI agent
save_to_file_tool = Tool(
    name="SaveToFile",
    func=save_to_file,
    description="Saves content to a file."
)

import subprocess

def generate_terraform_config():
    """Generate Terraform configuration for an Azure Virtual Machine."""
    
    main_tf_content = """
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0.2"
    }
  }

  required_version = ">= 1.1.0"
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_virtual_network" "example" {
  name                = "example-network"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
}

resource "azurerm_subnet" "example" {
  name                 = "example-subnet"
  resource_group_name  = azurerm_resource_group.example.name
  virtual_network_name = azurerm_virtual_network.example.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_public_ip" "example" {
  name                = "example-public-ip"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  allocation_method   = "Dynamic"
}

resource "azurerm_network_interface" "example" {
  name                = "example-nic"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.example.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.example.id
  }
}

resource "azurerm_virtual_machine" "example" {
  name                  = "example-machine"
  location              = azurerm_resource_group.example.location
  resource_group_name   = azurerm_resource_group.example.name
  network_interface_ids = [azurerm_network_interface.example.id]
  vm_size               = "Standard_DS1_v2"

  storage_os_disk {
    name              = "example-os-disk"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  os_profile {
    computer_name  = "examplevm"
    admin_username = var.admin_username
    admin_password = var.admin_password
  }

  os_profile_linux_config {
    disable_password_authentication = false
  }
}
"""

    variables_tf_content = """
variable "resource_group_name" {
  description = "The name of the Azure resource group"
  default     = "example-resources"
}

variable "location" {
  description = "Azure region"
  default     = "East US"
}

variable "admin_username" {
  description = "Admin username for the VM"
  default     = "azureuser"
}

variable "admin_password" {
  description = "Admin password for the VM"
  default     = "P@ssword1234!"
}
"""

    outputs_tf_content = """
output "public_ip" {
  description = "The public IP address of the VM"
  value       = azurerm_public_ip.example.ip_address
}
"""

    return {
        "main.tf": main_tf_content,
        "variables.tf": variables_tf_content,
        "outputs.tf": outputs_tf_content
    }


def run_terraform_command(command):
    """Run a Terraform command."""
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"Error running Terraform command: {str(e)}"

def validate_terraform():
    """Validate Terraform configuration before applying it."""
    validate_result = run_terraform_command("terraform validate")
    if "Success!" in validate_result:
        return True, "Terraform configuration is valid."
    return False, validate_result


def apply_terraform(args):
    """Initialize, validate, and apply Terraform configuration."""
    print(args)

    # Initialize Terraform
    init_result = run_terraform_command("terraform init")
    if "Terraform has been successfully initialized!" not in init_result:
        return init_result

    # Validate Terraform
    is_valid, validation_message = validate_terraform()
    if not is_valid:
        return f"Terraform validation failed:\n{validation_message}"

    # Apply Terraform if validation is successful
    apply_result = run_terraform_command("terraform apply -auto-approve")
    return apply_result

def destroy_terraform():
    """Destroy Terraform-managed infrastructure."""
    return run_terraform_command("terraform destroy -auto-approve")

# Define Terraform tool for AI Agent
terraform_tool = Tool(
    name="TerraformProvision",
    func=apply_terraform,
    description="Provisions infrastructure on Azure using Terraform."
)



# agent.run("")
# Deploy an Nginx web application to my local Kubernetes cluster with 3 replicas.

# If the user asks:
# Deploy a web app to Kubernetes
# → The agent will only run the Kubernetes tool.

# If the user asks:
# "Build and deploy a web app to Kubernetes,"
# → The agent will first build the Docker image using the Docker tool,
# → Then it will deploy the app using the Kubernetes tool.
