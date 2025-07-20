// Module for creating remote state

resource "azurerm_resource_group" "tfstate" {
  name = 
  location = 
}

resource "azurerm_storage_account" "tfstate" {
  name = 
  location = azurerm_resource_group.tfstate.location
  resource_group_name = azurerm_resource_group.tfstate.name
  account_tier = 
  account_replication_type = 
}

resource "azurerm_storage_container" "tfstate" {
  name = 
  storage_account_id = azurerm_storage_account.tfstate.id
  container_access_type = "private"
}