import dataiku
import re
from datetime import datetime

from sage.src import dss_funcs
from sage.src import instance_data_gather
from sage.src import project_data_gather

def main():
    # Initialize
    r = dss_funcs.get_dss_commits()

    # Get Instance Name
    client = dataiku.api_client()
    instance_info = client.get_instance_info()
    instance_name = instance_info.node_name.lower()
    instance_name = re.sub(r'[^a-zA-Z0-9]', ' ', instance_name)
    instance_name = re.sub(r'\s+', '_', instance_name)

    # Datetime
    dt = datetime.utcnow()

    # Loop pver and gather all the instance level data
    instance_data_gather.main(client, instance_name, dt)
    
    # Loop over and gather all the project level data and then stack
    project_data_gather.main(client, instance_name, dt)

    return

if __name__ == "__main__":
    main()