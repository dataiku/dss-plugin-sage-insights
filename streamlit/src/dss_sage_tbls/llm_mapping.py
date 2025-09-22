from sage.src import dss_duck


def main():
    query = """
        WITH llm_mesh AS (
            SELECT 
                instance_name,
                project_key,
                agents_versions_toolsUsingAgentSettings_llmId as llms_mesh_id,
                'AGENTS' AS llms_mesh_source
            FROM agents_metadata
            UNION ALL
            SELECT 
                instance_name,
                project_key,
                knowledge_banks_embeddingLLMId as llms_mesh_id,
                'KBS' AS llms_mesh_source
            FROM knowledge_banks_metadata
            UNION ALL
            SELECT 
                instance_name,
                project_key,
                recipes_params_llmid as llms_mesh_id,
                'RECIPES' AS llms_mesh_source
            FROM recipes_metadata
        )
        SELECT 
            llm_mesh.instance_name,
            llm_mesh.project_key,
            llm_mesh.llms_mesh_source,
            llm_mesh.llms_mesh_id,
            llms_metadata.llms_friendlyName,
            llms_metadata.llms_friendlyNameShort
        FROM llm_mesh
        LEFT JOIN llms_metadata
            ON (llm_mesh.llms_mesh_id = llms_metadata.llms_id
            AND llm_mesh.instance_name = llms_metadata.instance_name)
        WHERE llm_mesh.llms_mesh_id <> ''
    """
    df = dss_duck.query_duckdb_direct(query=query)
    cols = ["llms_conn", "llms_conn_name", "llms_model", "llms_model_version"]
    if df["llms_mesh_id"].str.split(":", expand=True).columns.stop == 5:
        cols = ["llms_conn", "llms_conn_name", "llms_model", "llms_model_version", "llms_model_version"]
    df[cols] = df["llms_mesh_id"].str.split(":", expand=True)
    df = df[df["llms_mesh_id"] != "False"]
    df = df.dropna(subset=["llms_mesh_id"])
    return df