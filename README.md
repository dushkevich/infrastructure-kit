# Infrastructure‑Kit

A modular, reusable, production‑ready IaC starter kit for Azure, built on Terraform.  
Provides an opinionated “one‑click” abstraction layer so teams can spin up common infrastructure patterns without wrestling with low‑level HCL.

---

> ⚠️ **Under construction**  
> Currently supports Static Websites. More blueprints coming soon!

---

## 🚀 Blueprints (“Options”)

Each blueprint bundles all the necessary Terraform modules, defaults, and deployment steps:

1. **Static Website**  
   - Azure Storage + CDN  ([module](./modules/storage/main.tf))
   - CI/CD pipeline (GitHub Actions)  (Under construction)
   Requires: `source_files` path in config.config pointing to your site assets (e.g., ./www)
2. **Serverless API**  
   - Azure Function + Networking  
   - Optional backing database (Cosmos DB / Azure SQL)  
   - CI/CD pipeline  
3. **Containerized Web App**  
   - AKS cluster + networking  
   - Container registry  
   - CI/CD pipeline  
4. **Three‑Tier Web App**  
   - Frontend (App Service)  
   - API layer (Functions or App Service)  
   - Database (Cosmos DB / SQL)  
   - Virtual Network + NAT / Firewall  
   - CI/CD pipeline  

---

## ⚙️ How It Works

1. **Configure**  
   - Create/edit `config.config` with your project settings and toggle desired blueprints. 

1. **Generate**  
   - `./kit.py --apply` 
   - → Generates:
     - `main.tf` with only the enabled modules  
     - `<project_name>.tfvars` populated from your config  
     - `terraform.tf` & `tfstate.config` for remote state backend  

1. **Deploy**  
   - Automatically runs:  
     - `terraform init`  (local state)  
     - `terraform apply` (remote‑state bootstrap)  
     - `terraform init`  (remote state)
     - `terraform apply` (full stack)  

1. **State Management**
    - Local init & bootstrap: The toolkit first initializes Terraform locally to create the Azure Storage account and container that will host your state file.

    - Remote backend: Once the storage resources exist, it re-initializes Terraform with `-backend-config=tfstate.config` and `-migrate-state=true` to move the state file into Azure Blob Storage.

    This ensures your Terraform state is stored centrally, safely locked, and shareable across your team.

1. **Teardown**  
   - `./kit.py --destroy`  
   - → Destroys all resources and cleans up generated files.

---

## 🛠️ Quick Start

1. **Clone the repo**  
   ```bash
   git clone https://github.com/dushkevich/infrastructure-kit.git
   cd infrastructure‑kit
   chmod +x kit.py
   ```

1. **Prerequisites**

    * Azure subscription (even a Free tier is OK)

    * Azure CLI installed and authenticated: `az login`

1. **Edit config.config**

```ini

[tfvars]
project_name = myapp
location     = eastus
source_files = ./www

[modules]
storage    = true
networking = false
compute    = false
security   = false
```

1. **Deploy/destroy**

```bash
./kit.py --apply
```
Destroy

```bash
./kit.py --destroy
```

## 📂 Project Layout
```arduino
.
├── kit.py
├── config.config.example
├── modules/
│   ├── storage/ (static_website)
│   ├── serverless_api/
│   ├── container_web/
│   └── three_tier/
└── README.md
```

## 🔧 Requirements
Python 3.6+

Terraform 1.10+

Azure CLI (for authentication)

## 🤝 Contributing
Fork the repo

Create a feature branch (git checkout -b feature/xyz)

Add or update a module under modules/

Update README.md and config.config.example

Open a Pull Request

## 📄 License
This project is licensed under the Apache 2.0.

```pgsql
Feel free to tweak wording, add badges (CI build status, Terraform registry links), or screenshots as you like!
```