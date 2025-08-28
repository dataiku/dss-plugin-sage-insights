
def user_login(df):
    # Remove scenarios, job and NaN's
    if "message.scenarioId" in df.columns:
        df = df[df["message.scenarioId"].isna()]
    if "message.jobId" in df.columns:
        df = df[df["message.jobId"].isna()]
    df = df[df["message.authSource"] == "USER_FROM_UI"]
    df = df.dropna(subset=["message.authUser"])
    df = df.dropna(axis=1, how='all')

    # Only the columns we need
    try:
        df = df[["timestamp", "message.callPath", "message.msgType", "message.authUser", "message.projectKey"]]
    except:
        print("RETURN")