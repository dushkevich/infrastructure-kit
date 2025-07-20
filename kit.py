#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import argparse

MODULES = {
    "storage": {
        "source": "./modules/storage",
        "config": {
            "project_name": "var.project_name",
            "location": "var.location"
        }
    }
}

def config():
    # check the config file and return necessary values
    with open("config.yaml", "r"):
        


def create_tfvars():
    # create tfvars file 


def generate_module_block():
    # generate modules block
    lines = [f'module "{name}" {{', f' source = "{module["source"]}"']
              '}}']



def main():

    with open("config.yaml") as f:
        config = 



main()