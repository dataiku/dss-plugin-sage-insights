
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
        df = df[["timestamp", "date", "message.callPath", "message.msgType", "message.authUser", "message.projectKey", "instance_name"]]
    except:
        print("RETURN")
        
    for i,grp in df.groupby("date"):
        # Login Users
        login_users = grp[grp["message.msgType"] == "application-open"]["message.authUser"].unique()
        login_users_df = pd.DataFrame([login_users], columns=["viewing_user_logins"])
        login_users_df["timestamp"] = pd.to_datetime(i)
        login_users_df["instance_name"] = df["instance_name"].iloc[0]

        # Active Users
        tdf = grp[grp["message.authUser"].isin(login_users)]
        action_words = ["save", "create", "analysis", "clear", "run"] # Action Words -- Focus on
        pattern = "|".join(action_words)
        tdf = tdf[tdf["message.msgType"].str.contains(pattern, na=False)]
        remove_strings = ["list", "dataset-clear-samples", "dataset-save-schema", "project-save-variables"] # Vague Words -- Remove
        pattern = "|".join(remove_strings)
        tdf = tdf[~tdf["message.msgType"].str.contains(pattern, na=False)]
        active_users = tdf["message.authUser"].unique()
        active_users_df = pd.DataFrame([active_users], columns=["developer_user_logins"])
        active_users_df["timestamp"] = pd.to_datetime(i)
        active_users_df["instance_name"] = df["instance_name"].iloc[0]