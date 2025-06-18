import dataiku
import os
import importlib
import pandas as pd
from datetime import datetime

from sage.base_data import client_handle  as dss_object
from sage.src import dss_folder


def run_modules(client, dt):
    directory = dss_object.__path__[0]
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith(".py") and f != "__init__.py":
                module_name = f[:-3]
                path = root.replace(directory, "")
                fp = os.path.join(root, f)
                spec = importlib.util.spec_from_file_location(module_name, fp)
                results = False
                try:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    if hasattr(module, 'main'):
                        results = module.main(client)
                except Exception as e:
                    results = [False, None]
                    print(f"Error importing or running ({path}) {module_name}: {e}")
            if results[0]:
                dt_year  = str(dt.year)
                dt_month = str(f'{dt.month:02d}')
                dt_day   = str(f'{dt.day:02d}')
                dss_folder.write_folder_output(
                    folder_name = "partitioned_data",
                    path = f"{path}/{module_name}/{dt_year}/{dt_month}/{dt_day}/data.csv",
                    data = results[1]
                )
                dss_folder.write_folder_output(
                    folder_name = "base_data",
                    path = f"{path}/{module_name}.csv",
                    data = results[1]
                )
    return


def main():
    dt = datetime.utcnow()
    client = dataiku.api_client()
    run_modules(client, dt)
    return


if __name__ == "__main__":
    main()