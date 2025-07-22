import streamlit as st
import dataiku
from sage.src import dss_funcs, dss_folder

local_client = dss_funcs.build_local_client()
project_handle = local_client.get_default_project()
sage_project_key = project_handle.project_key

try:
    df = dss_folder.read_local_folder_input(
        sage_project_key = sage_project_key,
        project_handle = project_handle,
        folder_name = "base_data",
        path = "/partition.csv"
    )
    partition = df.iloc[0, 0]
except:
    partition = "ERROR - Failed to read or find file."
# -----------------------------------------------------------------------------
# Home Page
st.markdown(f"""# 📊 Dataiku Sage Dashboard

## Overview

This dashboard provides key administrative insights into the Dataiku platform to help platform owners, administrators, and governance teams monitor usage, performance, project activity, and compliance metrics.

* **Latest Snapshot Partition:** {partition}

---

## 🧭 Goals (TBD)

- Monitor platform health and system performance
- Track user and project activity
- Identify inactive or stale projects
- Provide audit trails for security and governance
- Enable better resource planning and license usage insights


---

## 📅 Refresh Schedule

| Data Source           | Frequency |
|-----------------------|-----------|
| Log Ingestion         | Daily     |
| Insights & Statistics | Instant   |

---

## 👤 Access & Permissions

> Only users in the `administrative` group have full access to this dashboard.

---

## 📌 Notes

- This dashboard is built to be modular. Designed for ease of use and scale.
- For questions or enhancements, contact the **Platform Admin Team** at `Stephen.Mazzei@dataiku.com`.
""")