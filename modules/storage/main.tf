

resource "azurerm_resource_group" "storage" {
  name     = local.rg_name
  location = var.location
}

resource "azurerm_storage_account" "storage" {
  name                     = local.sa_name
  account_tier             = "Standard"
  account_replication_type = "LRS" // make it more customizable 
  location                 = azurerm_resource_group.storage.location
  resource_group_name      = azurerm_resource_group.storage.name
}

resource "azurerm_storage_blob" "storage" {
  for_each = local.blob_map

  name         = each.value.name // 
  source       = each.key        // 
  content_type = each.value.content_type
  # content_md5            = local.content_md5
  type                   = "Block"
  storage_account_name   = azurerm_storage_account.storage.name
  storage_container_name = local.container_name

  depends_on = [azurerm_storage_account.storage]
}

resource "azurerm_storage_account_static_website" "storage" {
  storage_account_id = azurerm_storage_account.storage.id
  index_document     = local.index
  # error_404_document = local.error

  depends_on = [azurerm_storage_account.storage]
}
