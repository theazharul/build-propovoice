#!/usr/bin/env python
import os
import re
import shutil
from pathlib import Path
import typer
import subprocess
from rich import print as rprint

app = typer.Typer()

current_dir = os.getcwd()
working_dir = Path(current_dir) / "propovoice_build"
env_file = os.path.expanduser("~") + "/.propovoice_env.txt"
pv_env_var = "PV_PLUGIN_DIR"
env_vars = {}
env_vars[pv_env_var] = None
plugin_dir = env_vars[pv_env_var]

@app.command()
def main():
    maybe_create_env_file_and_set_value()
    rprint(plugin_dir)
    maybe_create_working_dir()
    remove_all_from_working_dir()

def maybe_create_env_file_and_set_value():
    global plugin_dir, env_file, env_vars, pv_env_var
    # Check if the file exists and create it if not
    try:
        with open(env_file, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    var_name, var_value = line.split("=", 1)
                    env_vars[var_name] = var_value
    except FileNotFoundError:
        # The file doesn't exist, so create it
        with open(env_file, "w") as file:
            pass
            # You can initialize it with some default content
            # file.write(f"{pv_env_var}=/path/to/plugin\n")
            # env_vars = {pv_env_var: "/path/to/plugin"}

    if pv_env_var in env_vars:
        plugin_dir = env_vars[pv_env_var]
        is_reset = input(f"Your Plugin directory is <{plugin_dir}>. Do you want to reset it? (y/n): ")
        if is_reset.lower() == "y":
            # Reset the environment variable
            set_new_env_var_value()
    else:
        # Get the plugin directory from the user
        set_new_env_var_value()

def set_new_env_var_value():
    global env_file, env_vars, plugin_dir

    plugin_dir = Path(input("Please enter your WordPress Plugins directory path (e.g /home/user/var/www/wordpress/wp-content/plugins):\n"))
    env_vars["PV_PLUGIN_DIR"] = plugin_dir

    with open(env_file, "w") as newfile:
        for var_name, var_value in env_vars.items():
            newfile.write(f"{var_name}={var_value}\n")

def maybe_create_working_dir():
    global working_dir
    # Check if the directory already exists; if not, create it
    if not working_dir.exists():
        working_dir.mkdir(parents=True, exist_ok=True)
        rprint(f"[green]Directory '{working_dir}' created successfully.[/green]")
    else:
        rprint(f"[yellow]Directory '{working_dir}' already exists.[/yellow]")

def remove_all_from_working_dir():
    global working_dir
    # Remove everything inside the directory
    for item in os.listdir(working_dir):
        item_path = os.path.join(working_dir, item)
        if os.path.isfile(item_path):
            os.remove(item_path)  # Remove files
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)  # Remove subdirectories and their contents
    rprint(f"Contents of directory '{working_dir}' have been removed.")


if __name__ == "__main__":
    app()
