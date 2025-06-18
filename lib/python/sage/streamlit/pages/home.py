import streamlit as st

st.markdown("""# 📊 Dataiku Administrative Sage Dashboard

## Overview

This dashboard provides key administrative insights into the Dataiku platform to help platform owners, administrators, and governance teams monitor usage, performance, project activity, and compliance metrics.

---

## 🧭 Goals

- Monitor platform health and system performance
- Track user and project activity
- Identify inactive or stale projects
- Provide audit trails for security and governance
- Enable better resource planning and license usage insights


---

## 📅 Refresh Schedule

| Data Source          | Frequency |
|----------------------|-----------|
| Dataiku APIs         | Hourly    |
| Log Ingestion        | Daily     |
| Infrastructure Stats | 5 min     |

---

## 👤 Access & Permissions

> Only users in the `admin` or `platform-ops` group have full access to this dashboard. View-only access can be configured for compliance teams.

---

## 📌 Notes

- This dashboard is built to be modular. Each section can be imported as a Dataiku dashboard tab or a standalone webapp.
- For questions or enhancements, contact the **Platform Admin Team** at `platform-admins@yourcompany.com`.



""")