## 🧱 Dashboard Sections

if st.session_state.instance_name == "mazzei_designer":
    if st.button("rerun"):
        st.rerun()
        
### 1. 🏁 Platform Summary

- **Active Nodes**
- **Uptime**
- **Current Version**
- **License Expiration**
- **Last Backup Time**
- **Job Queue Depth**


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




