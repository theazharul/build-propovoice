#!/usr/bin/env python
import os
import shutil
from pathlib import Path
import typer
from rich import print as rprint

app = typer.Typer()

env_file = os.path.expanduser("~/.propovoice_env.txt")
pv_env_var = "PV_PLUGIN_DIR"

@app.command()
def main():
    env_vars = maybe_create_env_file_and_set_value()
    plugin_dir = env_vars[pv_env_var]
    rprint(plugin_dir)
    working_dir = maybe_create_working_dir()
    remove_all_from_working_dir(working_dir)

def maybe_create_env_file_and_set_value():
    if not os.path.exists(env_file):
        create_env_file(env_file)

    env_vars = read_env_file(env_file)
    if pv_env_var in env_vars:
        plugin_dir = env_vars[pv_env_var]
        is_reset = input(f"Your Plugin directory is <{plugin_dir}>. Do you want to reset it? (y/n): ")
        if is_reset.lower() == "y":
            set_new_env_var_value(env_file, env_vars)
    else:
        set_new_env_var_value(env_file, env_vars)

    return env_vars

def create_env_file(file_path):
    with open(file_path, "w") as file:
        pass

def read_env_file(file_path):
    env_vars = {}
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                var_name, var_value = line.split("=", 1)
                env_vars[var_name] = var_value
    return env_vars

def set_new_env_var_value(file_path, env_vars):
    plugin_dir = Path(input("Please enter your WordPress Plugins directory path (e.g /home/user/var/www/wordpress/wp-content/plugins):\n"))
    env_vars[pv_env_var] = str(plugin_dir)

    with open(file_path, "w") as newfile:
        for var_name, var_value in env_vars.items():
            newfile.write(f"{var_name}={var_value}\n")

def maybe_create_working_dir():
    working_dir = Path(os.getcwd()) / "propovoice_build"
    if not working_dir.exists():
        working_dir.mkdir(parents=True, exist_ok=True)
        rprint(f"[green]Directory '{working_dir}' created successfully.[/green]")
    else:
        rprint(f"[yellow]Directory '{working_dir}' already exists.[/yellow]")

    return working_dir

def remove_all_from_working_dir(working_dir):
    for item in working_dir.iterdir():
        if item.is_file():
            item.unlink()  # Remove files
        elif item.is_dir():
            shutil.rmtree(item)  # Remove subdirectories and their contents
    rprint(f"Contents of directory '{working_dir}' have been removed.")

if __name__ == "__main__":
    app()
