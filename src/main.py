from sage.src import instance_data_gather
from sage.src import project_data_gather

def main():
    # Loop pver and gather all the instance level data
    instance_data_gather.main()
    
    # Loop over and gather all the project level data and then stack
    project_data_gather.main()

    return

if __name__ == "__main__":
    main()