import streamlit as st

st.markdown("""# 📊 Dataiku Administrative Insights Dashboard

## Overview

(All of the following is ChatGPT code)

This dashboard provides key administrative insights into the Dataiku platform to help platform owners, administrators, and governance teams monitor usage, performance, project activity, and compliance metrics.

---

## 🧭 Goals

- Monitor platform health and system performance
- Track user and project activity
- Identify inactive or stale projects
- Provide audit trails for security and governance
- Enable better resource planning and license usage insights

---

## 📁 Data Sources

- **Dataiku Internal APIs**
  - `/admin/monitoring`
  - `/projects`
  - `/users`
  - `/scenarios`
- **Backend Logs**
  - `backend.log`, `access.log`
- **Usage Metrics Dataset**
  - Custom SQL/visual recipes from usage tracking plugins
- **IT Infrastructure Metrics**
  - CPU, memory, and storage metrics from the host environment (via Prometheus/Grafana, or OS monitoring tools)

---

## 🧱 Dashboard Sections

### 1. 🏁 Platform Summary

- **Active Nodes**
- **Uptime**
- **Current Version**
- **License Expiration**
- **Last Backup Time**
- **Job Queue Depth**

### 2. 👥 User Analytics

- **Total Users / Active in Last 30 Days**
- **Admin vs Non-Admin Ratio**
- **Login Trends Over Time**
- **Top Users by Job Count**
- **Users with No Recent Activity**

### 3. 📦 Project Activity

- **Total Projects / Active Projects**
- **Projects by Team / Owner**
- **Orphan Projects (No Activity in 60+ Days)**
- **Top Projects by Job Count / Runtime**
- **Scheduled Scenario Success/Failure Rate**

### 4. ⚙️ System Performance

- **CPU & Memory Usage**
- **Disk Usage Over Time**
- **Average Job Duration**
- **Parallel Job Limit vs Actual Use**
- **Error Rates (by Job Type)**

### 5. 🛡️ Governance & Security

- **User Role Audit (Admins, Advanced Users)**
- **Project Permissions Breakdown**
- **Plugin Version Audit**
- **Scenarios with External Triggers**
- **API Key Usage**

---

## 📅 Refresh Schedule

| Data Source          | Frequency |
|----------------------|-----------|
| Dataiku APIs         | Hourly    |
| Log Ingestion        | Daily     |
| Infrastructure Stats | 5 min     |

---

## 🔧 Technical Stack

- **Dataiku DSS Dashboards** (Charts, Tiles, Webapps)
- **Custom Python Plugins** for API ingestion
- **SQL Recipes** for summarizing data
- **Optional:** Integration with Grafana for system metrics

---

## 🧩 Future Enhancements

- Slack/Email alerts for admin anomalies (e.g., low disk, API misuse)
- Heatmaps for user activity across time
- Audit trail visualizations (access logs)
- Comparison snapshots (month-over-month usage)

---

## 👤 Access & Permissions

> Only users in the `admin` or `platform-ops` group have full access to this dashboard. View-only access can be configured for compliance teams.

---

## 📌 Notes

- This dashboard is built to be modular. Each section can be imported as a Dataiku dashboard tab or a standalone webapp.
- For questions or enhancements, contact the **Platform Admin Team** at `platform-admins@yourcompany.com`.



""")