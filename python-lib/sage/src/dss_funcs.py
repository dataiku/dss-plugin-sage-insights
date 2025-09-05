import sys
sys.dont_write_bytecode = True

import dataiku
import dataikuapi
import os
import re
import importlib
import pandas as pd
from sage.src import dss_folder


# ---------- DATAIKU CLIENT HANDLES -----------------------------
def build_local_client():
    client = dataiku.api_client()
    return client


def build_remote_client(host, api_key, ignore_certs=False):
    if ignore_certs:
        client = dataikuapi.DSSClient(host, api_key, insecure_tls=True)
    else:
        client = dataikuapi.DSSClient(host, api_key)
    return client


def get_dss_name(client):
    instance_info = client.get_instance_info()
    try:
        instance_name = instance_info.node_name.lower()
    except:
        instance_name = instance_info.node_id.lower()
    instance_name = re.sub(r'[^a-zA-Z0-9]', ' ', instance_name)
    instance_name = re.sub(r'\s+', '_', instance_name)
    return instance_name


def get_dss_name_id_mapping(client):
    instance_info = client.get_instance_info()
    instance_name = get_dss_name(client)
    try:
        instance_name_base = instance_info.node_name
    except:
        instance_name_base = instance_info.node_id
    instance_id_base = instance_info.node_id
    mapping = [instance_name, instance_name_base, instance_id_base]
    return mapping


# ---------- DATA GATHER MODULES -----------------------------
def run_modules(self, dss_objs, handle, client_d = {}, project_key = None):
    results = []
    directory = dss_objs.__path__[0]
    for root, _, files in os.walk(directory):
        for f in files:
            if not f.endswith(".py") or f == "__init__.py":
                continue
            module_name = f[:-3]
            path = root.replace(directory, "")
            fp = os.path.join(root, f)
            try:
                spec = importlib.util.spec_from_file_location(module_name, fp)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'main'):
                    df = module.main(handle, client_d)
                    results.append([project_key, path, module_name, "load/run", True, None])
            except Exception as e:
                df = pd.DataFrame()
                results.append([project_key, path, module_name, "load/run", False, e])
            if df.empty:
                results.append([project_key, path, module_name, "load/run", False, "DF CAME BACK EMPTY"])
                continue # nothing to write, skip
            instance_name = get_dss_name(build_local_client())
            if "instance_name" not in df.columns:
                df["instance_name"] = instance_name
            try:
                remote_client = build_remote_client(self.sage_project_url, self.sage_project_api, self.ignore_certs)
                dt_year  = str(self.dt.year)
                dt_month = str(f'{self.dt.month:02d}')
                dt_day   = str(f'{self.dt.day:02d}')
                write_path = f"/{instance_name}/{path}/{module_name}/{dt_year}/{dt_month}/{dt_day}/data.csv"
                if project_key:
                    write_path = f"/{instance_name}/{path}/{module_name}/{dt_year}/{dt_month}/{dt_day}/{project_key}_data.csv"
                dss_folder.write_remote_folder_output(self, remote_client, write_path, df)
                results.append([project_key, path, module_name, "write/save", True, None])
            except Exception as e:
                results.append([project_key, path, module_name, "write/save", False, e])
    return results


def get_nested_value(data, keys, dt=False):
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            if dt:
                return pd.to_datetime(0, unit="ms")
            else:
                return False
    return current


def rename_and_move_first(project_handle: "dataikuapi.dss.project.DSSProject", df: pd.DataFrame, old: str, new: str) -> pd.DataFrame:
    if old in df.columns:
        df = df.rename(columns={old: new})
    else:
        df[new] = project_handle.project_key
    if new in df.columns:
        cols = [new] + [c for c in df.columns if c != new]
        df = df[cols]
    df.columns = df.columns.str.replace(".", "_", regex=False)
    return df


# ---------- STREAMLIT MODULES -----------------------------
def collect_modules(module):
    import streamlit as st
    d = {}
    directory = module.__path__[0]
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith(".py") and f != "__init__.py":
                module_name = f[:-3]
                path = root.replace(directory, "")
                fp = os.path.join(root, f)
                delimiters = r'[-_]'
                words = re.split(delimiters, module_name)
                capitalized_words = [word.capitalize() for word in words]
                final_string = " ".join(capitalized_words)
                d[final_string] = [module_name, fp]
    return d


def collect_display_data(load_modules):
    display_data = []
    modules = collect_modules(load_modules)
    for key in modules.keys():
        r_type = key.split(" ")
        r_type = r_type[0].lower()
        display_data.append(key)
    return modules, display_data


def load_insights(module_name, fp, filters = {}):
    results = {}
    spec = importlib.util.spec_from_file_location(module_name, fp)
    try:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, 'main'):
            results = module.main(filters)
    except Exception as e:
        import streamlit as st
        st.error(f"Error importing or running ({fp}) {module_name}: {e}")
        results = {}
        return results
    return results