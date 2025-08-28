
def user_login(df):
    # Remove scenarios, job and NaN's
    if "message.scenarioId" in df.columns:
        df = df[df["message.scenarioId"].isna()]
    if "message.jobId" in df.columns:
        df = df[df["message.jobId"].isna()]
    df = df[df["message.authSource"] == "USER_FROM_UI"]
    df = df.dropna(subset=["message.authUser"])
    df = df.dropna(axis=1, how='all')

    # loop topics and save data
    try:
        df = df[["message.callPath", "message.msgType", "message.authUser", "message.projectKey"]]
    except:
        df = pd.DataFrame(columns=["message.callPath", "message.msgType", "message.authUser", "message.projectKey"])
    df = df.drop_duplicates()
    df["instance_name"] = instance_name
    df["timestamp"] = today
    try:
        write_path = f"/{instance_name}/users/audit/{dt_year}/{dt_month}/{dt_day}/data.csv"
        dss_folder.write_remote_folder_output(self, remote_client, write_path, df)
        results.append(["write/save", True, None])
    except Exception as e:
        results.append(["write/save - All", False, e])
    return 