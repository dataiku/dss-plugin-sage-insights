import dataiku
import dataikuapi
from datetime import datetime
import tomllib
import pandas as pd

from sage.src import dss_folder
from sage.src import dss_funcs
from sage.src import instance_data_gather
from sage.src import project_data_gather
from sage.src import macro_data_gather

def main():
    # Datetime
    dt = datetime.utcnow()

    # load config if doing parallel
    config_data = dss_funcs.get_custom_config("/python/sage_custom/api_configs.toml")
    if config_data:
        for key in config_data:
            client = dataikuapi.DSSClient(host=config_data[key]["url"], api_key=config_data[key]["api"])
            instance_name = dss_funcs.get_dss_name(client)
            instance_data_gather.main(client, instance_name, dt)
            project_data_gather.main(client, instance_name, dt)
            macro_data_gather.main(client, instance_name, dt)

    else:
        client = dataiku.api_client()
        instance_name = dss_funcs.get_dss_name(client)
        instance_data_gather.main(client, instance_name, dt)
        project_data_gather.main(client, instance_name, dt)
        macro_data_gather.main(client, instance_name, dt)


    # Create the base datasets
    dss_funcs.stack_partition_data()
    return

if __name__ == "__main__":
    main()