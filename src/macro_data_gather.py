import dataiku
import pandas as pd
import io
import tomllib

from sage.src import dss_folder

def run_macro(client, instance_name, config_data, key):
    pkey = client.list_project_keys()[0]
    project_handle = client.get_project(pkey)
    macro = project_handle.get_macro(runnable_type=config_data[key]["id"])
    if config_data[key]["params"]:
        macro_run = macro.run(wait=True, params=config_data[key]["params"])
    else:
        macro_run = macro.run(wait=True)
    result = macro.get_result(run_id=macro_run)
    if result.reason != "OK":
        print(f"Error on {instance_name} :: {results.reason}")
        return pd.DataFrame()
    string_buffer = io.StringIO(result.data.decode())
    df = pd.read_html(string_buffer)[0]
    return df

def main(client, instance_name, dt):
    # load config if doing parallel
    path = "../project-lib-resources/macro_configs.toml"
    try:
        with open(path, "rb") as f:
            config_data = tomllib.load(f)
    except:
        config_data = {}
    if not config_data:
        return

    # Loop and run
    for key in config_data:
        try:
            df = run_macro(client, instance_name, config_data, key)
        except Exception as e:
            print(f"Error on {instance_name} :: {key} - {e}")
            continue
        if df.empty:
            continue
        module_name = config_data[key]["id"]
        module_name = module_name.split("-")[-1]
        if "instance_name" not in df.columns:
            df["instance_name"] = instance_name
        dt_year  = str(dt.year)
        dt_month = str(f'{dt.month:02d}')
        dt_day   = str(f'{dt.day:02d}')
        category = config_data[key]["category"]
        dss_folder.write_folder_output(
            folder_name = "partitioned_data",
            path = f"/{instance_name}/{category}/{module_name}/{dt_year}/{dt_month}/{dt_day}/data.csv",
            data = df
        )
    return


if __name__ == "__main__":
    main()