// Module for creating remote state

variable "project_name" {
  type = string
  # validation {
  #   condition     = false
  #   error_message = "Error"
  # }
}

variable "location" {
  type = string
  # validation {
  #   condition     = false
  #   error_message = "The region is invalid, please select from the folowing list: https://learn.microsoft.com/en-us/azure/reliability/regions-list"
  # }
}

variable "random_string" {
  type = string
}

resource "azurerm_resource_group" "tfstate" {
  name     = "rg-tfstate-${var.project_name}"
  location = var.location
}

resource "azurerm_storage_account" "tfstate" {
  name                     = "sa${var.project_name}${var.random_string}"
  location                 = azurerm_resource_group.tfstate.location
  resource_group_name      = azurerm_resource_group.tfstate.name
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "tfstate" {
  name                  = "tfstate"
  storage_account_name  = azurerm_storage_account.tfstate.name
  container_access_type = "private"
}

output "sa_name" {
  value = azurerm_storage_account.tfstate.name
}
