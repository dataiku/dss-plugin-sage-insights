import os
import importlib
import pandas as pd

from sage.base_data import client_handle  as dss_object
from sage.src import dss_folder


def run_modules(client, instance_name, dt):
    directory = dss_object.__path__[0]
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith(".py") and f != "__init__.py":
                module_name = f[:-3]
                path = root.replace(directory, "")
                fp = os.path.join(root, f)
                spec = importlib.util.spec_from_file_location(module_name, fp)
                results, data = [False, None]
                try:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    if hasattr(module, 'main'):
                        results, data = module.main(client)
                except Exception as e:
                    results, data = [False, None]
                    print(f"Error importing or running ({path}) {module_name}: {e}")
            if results:
                if "instance_name" not in data.columns:
                    data["instance_name"] = instance_name
                dt_year  = str(dt.year)
                dt_month = str(f'{dt.month:02d}')
                dt_day   = str(f'{dt.day:02d}')
                dss_folder.write_folder_output(
                    folder_name = "partitioned_data",
                    path = f"/{instance_name}/{path}/{module_name}/{dt_year}/{dt_month}/{dt_day}/data.csv",
                    data = data
                )
    return


def main(client, instance_name, dt):
    # Gather data
    run_modules(client, instance_name, dt)
    return


if __name__ == "__main__":
    main()