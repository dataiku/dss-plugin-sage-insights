import pandas as pd
from sage.src.dss_funcs import get_nested_value


def main(client):
    cols = [
        "project_key", "project_name", "login", "login_displayname",
        "lastModifiedBy", "lastModifiedOn", "creationBy", "creationOn",
        "shortDesc", "tags"
    ]
    df = pd.DataFrame(columns=cols)
    for project in client.list_projects():
        projectKey = project.get("projectKey", False)
        ownerLogin = project.get("ownerLogin", False)
        name = project.get("name", False)
        ownerDisplayName = get_nested_value(project, ["ownerDisplayName"])
        lastModifiedBy = get_nested_value(project, ["versionTag", "lastModifiedBy", "login"])
        lastModifiedOn = get_nested_value(project, ["versionTag", "lastModifiedOn"])
        creationBy = get_nested_value(project, ["creationTag", "lastModifiedBy", "login"])
        creationOn = get_nested_value(project, ["creationTag", "lastModifiedOn"])
        shortDesc = project.get("shortDesc", False)
        tags = project.get("tags", False)
        d = [
            projectKey, name, ownerLogin, ownerDisplayName,
            lastModifiedBy, lastModifiedOn, creationBy, creationOn,
            shortDesc, tags
        ]
        tdf = pd.DataFrame([d], columns=cols)
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

    return [True, df]


if __name__ == "__main__":
    main()