


module "storage" {
  source       = "modules/storage"
  project_name = var.project_name
  location     = var.location
}
