import streamlit as st
import dataiku

from sage.src import dss_duck

st.set_page_config(initial_sidebar_state="collapsed")
st.set_page_config(layout="centered")

# -----------------------------------------------------------------------------
# Build SQL Query Statement and Query, 
try:
    df = dss_duck.query_duckdb_direct("SELECT * FROM partition")
    partition = df.iloc[0, 0]
except:
    partition = None

# -----------------------------------------------------------------------------
# Homepage
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

---

## 🔃 Refresh Sage Data

""")

if st.button("Refresh"):
    dss_duck.initialize_duckdb(force=True)