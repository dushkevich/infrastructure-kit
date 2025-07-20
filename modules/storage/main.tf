

resource "azurerm_resource_group" "storage" {
  name = local.rg_name
  location = var.location
}

resource "azurerm_storage_account" "storage" {
  name = local.sa_name
  location = azurerm_resource_group.storage.location
  resource_group_name = azurerm_resource_group.storage.name
  account_tier = 
  account_replication_type = 
}

resource "azurerm_storage_container" "storage" {
  name = local.container_name
  storage_account_id = azurerm_storage_account.storage.id
  container_access_type = 
}

resource "azurerm_storage_blob" "storage" {
  name = 
  storage_account_name = azurerm_storage_account.storage.name
  storage_container_name = azurerm_storage_container.storage.name
  source = 
  content_type = 
  content_md5 = 
  type = 
}

resource "azurerm_storage_account_static_website" "storage" {
  storage_account_id = azurerm_storage_account.storage.id
  index_document = 
  error_404_document = 
}