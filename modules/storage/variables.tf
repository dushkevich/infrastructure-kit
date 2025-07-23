variable "project_name" { // HAVE TO ADD VALIDATION
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

variable "source_files" { // fix, it have to be a list, as I understand
  type = list(string)
  # validation {
  #   condition     = false
  #   error_message = "value"
  # }
}

locals {
  # region = {

  # }
  # short_location = 
  rg_name        = format("rg-static-%s", var.project_name)
  sa_name        = format("sastatic%s94", var.project_name) // there is 94 at the end of the sa_name !!!!!!!
  container_name = "web"

  content_types = {
    html = "text/html"
    css  = "text/css"
    js   = "application/javascript"
    json = "application/json"
    png  = "image/png"
    jpg  = "image/jpeg"
    svg  = "image/svg+xml"
    txt  = "text/plain"
  }

  blob_map = { for f in var.source_files : f => {
    name         = basename(f)
    extension    = split(".", basename(f))[-1]
    content_type = lookup(local.content_types, split(".", basename(f))[-1], "text/html")
    # content_md5 = 
    }
  }

  index = "index.html" #split("/", var.source_files)[-1]
  # error =
}
