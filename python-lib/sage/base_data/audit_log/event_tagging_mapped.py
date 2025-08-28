# ----------------------------------------------------------------
# USER_MAINTENANCE
# ----------------------------------------------------------------
def tag_user_maintenance():
    category = "USER_MAINTENANCE"
    d = {
        "audit_msg_base": [
            "user"
        ]
    }
    return category, d


# ----------------------------------------------------------------
# ADMINISTRATION
# ----------------------------------------------------------------
def tag_administration():
    category = "ADMINISTRATION"
    d = {
        "audit_msg_base": [
            "admin", "security", "dss", "instance", "instances"
        ]
    }
    return category, d
    
    
# ----------------------------------------------------------------
# READING_LISTING
# ----------------------------------------------------------------
def tag_reading_listing():
    category = "READING_LISTING"
    d = {
        "audit_msg_substring": [
            "-list", "-read"
        ],
        "audit_msg_base": [
            "list", "catalog", "samples", "insight", "lineage", "load",
            "connection"
        ]
    }
    return category, d


# ----------------------------------------------------------------
# STATISTIC_ANALYTICS
# ----------------------------------------------------------------
def tag_statistic_analytics():
    category = "STATISTIC_ANALYTICS"
    d = {
        "audit_msg_substring": [
            "-eda_"
        ],
        "audit_msg_base": [
            "analyse", "analysis", "statistics", "metrics", "data",
            "checks", "pml", "conditional", "custom"
        ]
    }
    return category, d


# ----------------------------------------------------------------
# MLOPS
# ----------------------------------------------------------------
def tag_mlops():
    category = "MLOPS"
    d = {
        "audit_msg_substring": [
            "-modal-", "-evaluation-", "--prediction_scoring"
        ],
        "audit_msg_base": [
            "model", "ml", "mltask", "clustering", "prediction",
            "experiment", "labeling", "compare", "doctor", "interactive",
            "learning", "license", "me", "modelevaluationstore", "render",
            "start", "stop", "solution", "compute", "saved", "savedmodel",
            "evaluation", "mlflow", "set_run_inference_info", "modelcomparisons"
        ]
    }
    return category, d


# ----------------------------------------------------------------
# GENAI_LLM
# ----------------------------------------------------------------
def tag_genai_llm():
    category = "GENAI_LLM"
    d = {
        "audit_msg_substring": [
            "-answers", "-generate", "-prompt", "-nlp_llm",
            "-embed_documents"
        ],
        "audit_msg_base": [
            "ai", "agent", "knowledge", "llm", "prompt", "explain",
            "explanation", "dynamic", "docextract", "datastory", "generate",
            "answers", "nlp_llm", "embed_documents"
        ]
    }
    return category, d


# ----------------------------------------------------------------
# CODING
# ----------------------------------------------------------------
def tag_coding():
    category = "CODING"
    d = {
        "audit_msg_substring": [
            "code_studio", "codestudio", "-python-", "-code-env-",
            "-notebook", "-python", "-sql", "-spark"
        ],
        "audit_msg_base": [
            "code", "sql", "sparksql", "notebook", "notebooks",
            "jupyter", "streaming", "studio"
        ]
    }
    return category, d


# ----------------------------------------------------------------
# PLUGINS
# ----------------------------------------------------------------
def tag_plugins():
    category = "PLUGINS"
    d = {
        "audit_msg_base": [
            "plugin", "plugindev", "plugins"
        ]
    }
    return category, d


# ----------------------------------------------------------------
# CHARTS_DASHBOARD
# ----------------------------------------------------------------
def tag_charts_dashboard():
    category = "CHARTS_DASHBOARD"
    d = {
        "audit_msg_base": [
            "chart", "dashboard", "dashboards", "connect"
        ]
    }
    return category, d


# ----------------------------------------------------------------
# DATASET
# ----------------------------------------------------------------
def tag_dataset():
    category = "DATASET"
    d = {
        "audit_msg_base": [
            "dataset"
        ]
    }
    return category, d


# ----------------------------------------------------------------
# WIKI_ARTICAL_DISCUSSIONS
# ----------------------------------------------------------------
def tag_wiki_artical_discuissions():
    category = "WIKI_ARTICAL_DISCUSSIONS"
    d = {
        "audit_msg_base": [
            "article", "discussion", "wiki", "report", "discussions"
        ]
    }
    return category, d


# ----------------------------------------------------------------
# FOLDERS
# ----------------------------------------------------------------
def tag_folders():
    category = "FOLDERS"
    d = {
        "audit_msg_base": [
            "folder", "managed", "managedfolder"
        ]
    }
    return category, d


# ----------------------------------------------------------------
# WEBAPPS
# ----------------------------------------------------------------
def tag_webapps():
    category = "WEBAPPS"
    d = {
        "audit_msg_substring": [
            "-webapp-"
        ],
        "audit_msg_base": [
            "webapp"
        ]
    }
    return category, d


# ----------------------------------------------------------------
# GIT
# ----------------------------------------------------------------
def tag_git():
    category = "GIT"
    d = {
        "audit_msg_base": [
            "git", "projects"
        ]
    }
    return category, d


# ----------------------------------------------------------------
# SCENARIOS
# ----------------------------------------------------------------
def tag_scenarios():
    category = "SCENARIOS"
    d = {
        "audit_msg_base": [
            "scenarios", "schedule", "job", "gantt", "scenario", "refresh",
            "runnable", "runs"
        ]
    }
    return category, d


# ----------------------------------------------------------------
# DEPLOYER
# ----------------------------------------------------------------
def tag_deployer():
    category = "DEPLOYER"
    d = {
        "audit_msg_base": [
            "unified", "publish", "deployer", "deployment", "monitoring",
            "projectdeployer"
        ]
    }
    return category, d


# ----------------------------------------------------------------
# AUTOMATION
# ----------------------------------------------------------------
def tag_automation():
    category = "AUTOMATION"
    d = {
        "audit_msg_base": [
            "automation", "design"
        ]
    }
    return category, d


# ----------------------------------------------------------------
# PREPARE
# ----------------------------------------------------------------
def tag_prepare():
    category = "PREPARE"
    d = {
        "audit_msg_base": [
            "prepare", "shaker", "smartdate", "patternbuilder"
        ]
    }
    return category, d


# ----------------------------------------------------------------
# MISC_RECIPES
# ----------------------------------------------------------------
def tag_misc_recipes():
    category = "MISC_RECIPES"
    d = {
        "audit_msg_base": [
            "download", "export", "worksheets_export", "import",
            "table"
        ]
    }
    return category, d


# ----------------------------------------------------------------
# VISUAL_RECIPES
# ----------------------------------------------------------------
def tag_visual_recipes():
    category = "VISUAL_RECIPES"
    d = {
        "audit_msg_base": [
            "recipe", "geo", "regular", "fuzzy"
        ]
    }
    return category, d


# ----------------------------------------------------------------
# FLOW
# ----------------------------------------------------------------
def tag_flow():
    category = "FLOW"
    d = {
        "audit_msg_base": [
            "flow", "copy", "test",
            "rightpanelrecipe_actions_insertrecipe",
            "rightpanelrecipe_actions_snipandreconnect"
            
        ]
    }
    return category, d


# ----------------------------------------------------------------
# PROJECTS
# ----------------------------------------------------------------
def tag_projects():
    category = "PROJECTS"
    d = {
        "audit_msg_base": [
            "project", "tutorial"
        ]
    }
    return category, d


# ----------------------------------------------------------------
# GOVERN
# ----------------------------------------------------------------
def tag_govern():
    category = "GOVERN"
    d = {
        "audit_msg_base": [
            "govern"
        ]
    }
    return category, d


# ----------------------------------------------------------------
# APPLICATION_DESIGNER
# ----------------------------------------------------------------
def tag_application_designer():
    category = "APPLICATION_DESIGNER"
    d = {
        "audit_msg_base": [
            "app", "apps", "application"
        ]
    }
    return category, d


# ----------------------------------------------------------------
# WORKSPACES
# ----------------------------------------------------------------
def tag_workspaces():
    category = "WORKSPACES"
    d = {
        "audit_msg_base": [
            "workspaces", "workspace"
        ]
    }
    return category, d


# ----------------------------------------------------------------
# APIS
# ----------------------------------------------------------------
def tag_apis():
    category = "APIS"
    d = {
        "audit_msg_base": [
            "api"
        ]
    }
    return category, d


# ----------------------------------------------------------------
# CONTAINERS
# ----------------------------------------------------------------
def tag_containers():
    category = "CONTAINERS"
    d = {
        "audit_msg_base": [
             "clusters", "container", "containers", "kubernetes", 
        ]
    }
    return category, d


# EOF