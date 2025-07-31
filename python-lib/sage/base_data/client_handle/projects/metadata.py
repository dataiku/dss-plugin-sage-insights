import pandas as pd
from sage.src.dss_funcs import get_nested_value


def main(client):
    df = pd.DataFrame()
    for project in client.list_projects():
        d = {}
        
        # Poll Data
        d["projectKey"] = project.get("projectKey", False)
        d["project_name"] = project.get("name", False)
        d["project_login"] = project.get("ownerLogin", False)
        d["project_login_dn"] = get_nested_value(project, ["ownerDisplayName"])
        d["lastModifiedBy"] = get_nested_value(project, ["versionTag", "lastModifiedBy", "login"])
        d["lastModifiedOn"] = get_nested_value(project, ["versionTag", "lastModifiedOn"])
        d["creationBy"] = get_nested_value(project, ["creationTag", "lastModifiedBy", "login"])
        d["creationOn"] = get_nested_value(project, ["creationTag", "lastModifiedOn"])
        d["shortDesc"] = project.get("shortDesc", False)
        d["tags"] = project.get("tags", False)

        # turn to dataframe
        tdf = pd.DataFrame([d])
        if df.empty:
            df = tdf
        else:
            df = pd.concat([df, tdf], ignore_index=True)
    
    # Imported projects missing creation values - temp fix for now
    df.loc[df["creationBy"] == False, "creationBy"] = df["lastModifiedBy"]
    df.loc[df["creationOn"] == 0, "creationOn"] = df["lastModifiedOn"]

    # Clean dates
    for c in ["lastModifiedOn", "creationOn"]:
        df[c] = pd.to_datetime(df[c], unit="ms", utc=True)
        df[c] = pd.to_datetime(df[c], utc=True)
        df[c] = df[c].fillna(pd.to_datetime("1970-01-01", utc=True))
        df[c] = df[c].dt.strftime("%Y-%m-%d %H:%M:%S.%f")

    return df