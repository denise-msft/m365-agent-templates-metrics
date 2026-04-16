# 📊 m365-agent-templates Metrics Toolkit

Telemetry tracking toolkit for [microsoft/m365-agent-templates](https://github.com/microsoft/m365-agent-templates) — the open-source home for M365 Copilot and Copilot Studio agent templates.

## 🚀 Quick Start

```powershell
# Set your token (need push access to the repo)
$env:GITHUB_TOKEN = (gh auth token)

# Run the CLI dashboard
.\m365-agent-templates-metrics.ps1
```

## 📦 What's in This Repo

| File | What It Does |
|------|-------------|
| **[github-telemetry-guide.html](github-telemetry-guide.html)** | 📖 **Start here** — comprehensive teaching guide (just open in browser) |
| [m365-agent-templates-metrics.ps1](m365-agent-templates-metrics.ps1) | CLI dashboard — terminal output with bar charts |
| [dashboard.html](dashboard.html) | Static HTML dashboard with Chart.js (dark GitHub theme, 4 KPIs, 6 charts) |
| [AgentTemplatesMetrics.ipynb](AgentTemplatesMetrics.ipynb) | Fabric/Spark notebook for saving to Delta lakehouse (historical trends) |
| [m365-agent-templates-add-view-badges.ps1](m365-agent-templates-add-view-badges.ps1) | Generates hits.sh view-tracking badges for README files |

## 🤖 Agent Templates We Track

| Template | Type | GitHub Folder |
|----------|------|---------------|
| 📅 Plan My Day | Declarative Agent | [/Plan My Day](https://github.com/microsoft/m365-agent-templates/tree/main/Plan%20My%20Day) |
| 📋 My Company Policy | Declarative Agent | [/My Company Policy](https://github.com/microsoft/m365-agent-templates/tree/main/My%20Company%20Policy) |
| 📊 Executive Briefing | Declarative Agent | [/Executive Briefing](https://github.com/microsoft/m365-agent-templates/tree/main/Executive%20Briefing) |
| 📝 Request Tracker | Custom Agent (CS) | [/Request Tracker](https://github.com/microsoft/m365-agent-templates/tree/main/Request%20Tracker) |
| 🔍 Know My Customer | Custom Agent (CS) | [/Know My Customer](https://github.com/microsoft/m365-agent-templates/tree/main/Know%20My%20Customer) |

## ⚠️ Download Tracking — The Critical Rule

GitHub only tracks downloads for **Release assets**. Files in the repo tree (the .zip files inside each template folder) are **NOT counted** when downloaded.

**The rule:** Every download link — aka.ms, SharePoint, field decks, README — must point to a **GitHub Release asset URL** (or an aka.ms redirect to one). If someone copies the .zip to SharePoint and shares that link, those downloads are invisible.

See the [teaching guide](github-telemetry-guide.html) section 10a for the full breakdown and `gh release create` commands.

## 🔑 Prerequisites

- GitHub PAT with `repo` scope (traffic endpoints need push access)
- PowerShell 7+ and `gh` CLI
- For Fabric notebook: access to "Power CAT Team" workspace

## 👤 Team

Built by the Copilot Advisory Team (CAT) at Microsoft.
