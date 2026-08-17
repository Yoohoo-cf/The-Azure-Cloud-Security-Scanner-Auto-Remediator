terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "sec_lab" {
  name     = "rg-security-automation-lab"
  location = "East US"
}

# Non-Compliant Storage Account (Public access allowed)
resource "azurerm_storage_account" "vulnerable_sa" {
  name                     = "stsecvunlab001"
  resource_group_name      = azurerm_resource_group.sec_lab.name
  location                 = azurerm_resource_group.sec_lab.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  allow_nested_items_to_be_public = true
}

# Compliant Storage Account
resource "azurerm_storage_account" "secure_sa" {
  name                     = "stsecseclab001"
  resource_group_name      = azurerm_resource_group.sec_lab.name
  location                 = azurerm_resource_group.sec_lab.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  allow_nested_items_to_be_public = false
}