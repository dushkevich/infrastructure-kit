#!/usr/bin/env python3

import os
import sys
import subprocess
import time
import argparse
import random
import string
import json
from pathlib import Path
import configparser


def main():

    tfvars, enabled_modules = load_config("config.config")
    project_name = tfvars.get("project_name")
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

    time.sleep(200)

    run_plan() 

def init_tfstate(project_name):

    subprocess.run(["terraform", "init"], check=True)
    subprocess.run(["terraform", "apply", "-target=module.remote-state", f"-var-file={project_name}.tfvars", "-auto-approve"], check=True) ## !!!!! default.tfvars!!!!
    with open("terraform.tf", "a") as f: f.write('\nterraform {\n  backend "azurerm" {\n  }\n}')
    

def run_plan(project_name):
    subprocess.run(["terraform", "init", "-backend-config=tfstate.config", "-reconfigure"], check=True)
    # subprocess.run(["terraform", "init", "-backend-config=tfstate.config"], check=True)
    subprocess.run(["terraform", "plan", f"-var-file={project_name}.tfvars"], check=True)

def create_tfstate_config(name, random_string): ## I think there could me more elegant way
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
    return "\n".join(lines)

def list_source_files(path):
    src_path = Path(path)
    if not src_path.exists():
        raise FileNotFoundError(f"Could not find {path}")

    files = [
        f"{src_path}/{file.name}" for file in src_path.iterdir() ## wery bad and impossible to scail
    ]

    return files

main()
