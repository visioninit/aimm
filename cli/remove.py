import os
import sys
import json
from typing import Optional
import typer

from cli import base_funcs as base_funcs, aimmApp

app = aimmApp.app

@app.command()
def remove(name_version: Optional[str] = typer.Argument(None)):
    """
    Remove a model from local aimodels.json.
    """
    if name_version is None:
        typer.echo("Usage: aimm remove [OPTIONS] NAME\n"
                   "Try 'aimm remove --help' for help.\n\n"
                   "Error: Missing argument 'NAME_VERSION'.")
        sys.exit(1)
    # removes name:version from aimodels.json
    name, version = base_funcs.lowercase_name_version(name_version)
    
    # if aimodels.json doesn't exist exit
    if not os.path.exists("aimodels.json"):
        typer.echo("Error: aimodels.json not found, please run the aimm init")
        sys.exit(1)
    
    # parse aimodels.json as a json
    try:
        with open("aimodels.json", "r") as f:
            aimodels = json.load(f)
    except Exception as e:
        typer.echo(f"Error: {e}")
        sys.exit(1)

    # remove name and version from aimodels.json if there
    if version is None:
        for package_name, package_version in aimodels.items():
            if package_name.lower() == name:
                if len(package_version) > 1:
                    typer.echo(f"Multiple versions of {name} in aimodels.json, please specify a version.")
                    while True:
                        typer.echo(f"Available versions: {package_version}")
                        input_version = typer.prompt("Version to remove")
                        input_version = input_version.lower()
                        if input_version in package_version:
                            version = input_version
                            break
    for package_name, package_version in aimodels.items():
        # case insensitive
        if package_name.lower() == name and any(v.lower() == version for v in package_version):
            aimodels[package_name].remove(version)
            base_funcs.update_ai_models_lock(name, version, None, "remove")
            typer.echo(f"Removed {name_version} from aimodels.json")
            for package in aimmApp.installed["packages"]:
                if package["name"].lower() == name and package["version"].lower() == version:
                    typer.echo(f'The package is still available system-wide, to uninstall (delete files):\n\t aimm uninstall {package["name"]}:{package["version"]}')
                    break
            break
    else:
        typer.echo(f"{name_version} not found in aimodels.json")
        sys.exit(1)
        
    try:
        with open("aimodels.json", "w") as f:
            # prettify json
            json.dump(aimodels, f, indent=4)
    except Exception as e:
        typer.echo(f"Error: {e}")
        sys.exit(1)
