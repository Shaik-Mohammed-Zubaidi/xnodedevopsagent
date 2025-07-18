provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example_resources" {
  name     = "example-resources"
  location = "East US"
}

resource "azurerm_network_interface" "example_nic" {
  name                = "example-nic"
  location            = azurerm_resource_group.example_resources.location
  resource_group_name = azurerm_resource_group.example_resources.name

  ip_configuration {
    name                          = "internal"
    priority                      = 1000
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.example_public_ip.id
  }
}

resource "azurerm_public_ip" "example_public_ip" {
  name                = "example-public-ip"
  location            = azurerm_resource_group.example_resources.location
  resource_group_name = azurerm_resource_group.example_resources.name
  allocation_method   = "Dynamic"
}

resource "azurerm_virtual_network" "example_vnet" {
  name                = "example-vnet"
  location            = azurerm_resource_group.example_resources.location
  resource_group_name = azurerm_resource_group.example_resources.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "example_subnet" {
  name                 = "example-subnet"
  resource_group_name  = azurerm_resource_group.example_resources.name
  virtual_network_name = azurerm_virtual_network.example_vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_linux_virtual_machine" "example_vm" {
  name                 = "example-vm"
  location             = azurerm_resource_group.example_resources.location
  resource_group_name  = azurerm_resource_group.example_resources.name
  size                 = "Standard_DS1_v2"
  admin_username      = "azureuser"
  admin_password      = "P@ssword1234!"
  network_interface_ids = [azurerm_network_interface.example_nic.id]
  os_disk {
    caching              = "ReadWrite"
    create_option        = "FromImage"
  }
  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
}