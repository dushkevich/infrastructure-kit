#!/usr/bin/env python3

# import os
# import sys
import re
import argparse

import subprocess
import time
import random
import string
import json
from pathlib import Path
import configparser


def main(args):
    tfvars, enabled_modules = load_config("config.config")
    project_name = tfvars.get("project_name")
    if args.apply:
        apply(tfvars, enabled_modules, project_name)
    elif args.destroy:
        destroy(project_name)
    else:
        print("Usage: kit.py <options>\n-a for applying -d for delition")


def destroy(project_name):
    # for module in enabled_modules:
    #     subprocess.run(["terraform", "apply", "-destroy", f"-target=module.{module}", f"-var-file={project_name}.tfvars", "-auto-approve"], check=True)

    init_providers()
    with open("terraform.tf", "a") as f: f.write('\nterraform {\n  backend "local" {\n  }\n}')
    subprocess.run(["terraform", "init", "-migrate-state=true", "-force-copy"], check=True)

    subprocess.run(["terraform", "apply", "-destroy", f"-var-file={project_name}.tfvars", "-auto-approve"], check=True)

    subprocess.run(["rm", "-f", f"{project_name}.tfvars", "main.tf", "tfstate.config", "terraform.*", ".terraform.lock.hcl", "output.txt"])
    subprocess.run(["rm", "-rf", ".terraform"])


def apply(tfvars, enabled_modules, project_name):

    random_string = ''.join(random.choices(string.ascii_lowercase, k=6))
    with open(f'{project_name}.tfvars', "w") as f:
        for key, value in tfvars.items():
            if key == "source_files":
                f.write(f'{key} = {json.dumps(list_source_files(value))}')
            else:
                f.write(f'{key} = "{value}"\n')
    print("Succesfully generated tfvars file")

    enabled_modules.insert(0, "remote-state")
    with open("main.tf", "w") as f:
        for var in tfvars:
            f.write(f'variable "{var}" ''{ type = any }\n')
        f.write('\n\n')
        for mod in enabled_modules:
            block = generate_module_block(mod, tfvars, random_string)
            f.write(block + "\n\n")
    print("Modules succesfully referenced in main.tf")

    init_tfstate(project_name)
    create_tfstate_config(project_name, random_string)

    time.sleep(30)

    run_apply(project_name) 


def init_tfstate(project_name):
    init_providers()
    subprocess.run(["terraform", "init"], check=True)
    subprocess.run(["terraform", "apply", "-target=module.remote-state", f"-var-file={project_name}.tfvars", "-auto-approve"], check=True)

    with open("terraform.tf", "a") as f: f.write('\nterraform {\n  backend "azurerm" {\n  }\n}')
    

def run_apply(project_name):  
    subprocess.run(["terraform", "init", "-backend-config=tfstate.config", "-migrate-state=true", "-force-copy"], check=True)
    # subprocess.run(["terraform", "plan", f"-var-file={project_name}.tfvars"], check=True)

    time.sleep(20)

    subprocess.run(["terraform", "apply", f"-var-file={project_name}.tfvars", "-auto-approve"], check=True)
    with open("output.txt", "w") as f: subprocess.run(["terraform", "output"], stdout=f, stderr=subprocess.STDOUT)


def init_providers():
    with open("terraform.tf", "w") as f: f.write('terraform {\n  required_version = ">=1.0"\n\n  required_providers {\n    azurerm = {\n      source  = "hashicorp/azurerm"\n      version = "~> 3.0"\n    }\n  }\n}')
    with open("terraform.tf", "a") as f: f.write('\n\nprovider "azurerm" {\n  features {}\n}')


def create_tfstate_config(name, random_string): ## I think there could be more elegant way
    with open("tfstate.config", "w") as f:
        f.write(f'resource_group_name = "rg-tfstate-{name}"\nstorage_account_name = "sa{name}{random_string}"\n')
        f.write(f'container_name = "tfstate"\nkey = "tfstate"')


def load_config(config_path):
    # check the config file and return necessary values
    config = configparser.ConfigParser()
    config.read(config_path)
    
    tfvars = dict(config["tfvars"]) if "tfvars" in config else {}


    enabled_modules = []
    if "modules" in config:
        for module, flag in config["modules"].items():
            if flag.strip().lower() == "true":
                enabled_modules.append(module)

    return tfvars, enabled_modules


def generate_module_block(name, tfvars, random_string):
    # generate modules block
    lines = [f'module "{name}" {{']
    lines.append(f'  source = "./modules/{name}"')
    for key, value in tfvars.items():
        if name == "remote-state" and key not in ["project_name", "location"]:
                lines.append(f'  random_string = "{random_string}"')
                lines.append("}")
                return "\n".join(lines)

        lines.append(f'  {key} = var.{key}')

    # if extra_vars:
    #     for key, value in extra_vars.items():
    #         lines.append(f'  {key} = "{value}"')
    lines.append("}")

    if name != "remote-state":
        output = extract_output(name)
        for o in output:
            lines.append(f'\noutput "{o}" {{')
            lines.append(f'  value = module.{name}.{o}\n}}')
    return "\n".join(lines)


def extract_output(module):
    with open(f"./modules/{module}/output.tf", "r") as f:
        content = f.read()

    return re.findall(r'output\s+"([^"]+)"\s*\{', content)


def list_source_files(path):
    src_path = Path(path)
    if not src_path.exists():
        raise FileNotFoundError(f"Could not find {path}")

    files = [
        f"{src_path}/{file.name}" for file in src_path.iterdir() ## very bad and impossible to scail
    ]

    return files

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ability to apply or destroy")
    parser.add_argument("-a", "--apply", action="store_true", help="Apply resources")
    parser.add_argument("-d", "--destroy", action="store_true", help="Destroy resources")
    args = parser.parse_args()

    main(args)
