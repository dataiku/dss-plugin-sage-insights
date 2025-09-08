import pandas as pd

conn_mapping = {
    "llm_mesh": [
        "MistralAI", "Pinecone", "CustomLLM", "AzureLLM", "Bedrock",
        "HuggingFaceLocal", "VertexAILLM", "StabilityAI", "Cohere",
        "SageMaker-GenericLLM", "AzureAISearch", "Anthropic",
        "DatabricksLLM", "SnowflakeCortex", "AzureOpenAI", "OpenAI"
    ]
}

reverse_lookup = {
    value: tag
    for tag, values in conn_mapping.items()
    for value in values
}


def main(client, client_d = {}):
    connections = client.list_connections_names(connection_type="all")
    dfs = []
    for conn in connections:
        conn_handle = client.get_connection(name=conn)
        settings = conn_handle.get_settings()
        d = settings.settings
        dfs.append(pd.json_normalize(d))
    df = pd.concat(dfs, ignore_index=True)
    df.columns = df.columns.str.replace(".", "_", regex=False)
    df["connection_category"] = df["type"].map(reverse_lookup).fillna("other")

    return df