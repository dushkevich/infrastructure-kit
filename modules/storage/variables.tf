variable "project_name" {
  type = string
  validation {
    condition = 
    error_message = 
  }
}

variable "location" {
  type = string
  validation {
    condition = 
    error_message = "The region is invalid, please select from the folowing list: https://learn.microsoft.com/en-us/azure/reliability/regions-list"
  }
}

locals {
  rg_name = format()
  sa_name = format()
  container_name = format()

  blob_names = 
}