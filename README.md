# 📊 m365-agent-templates Metrics Toolkit

Telemetry tracking toolkit for [microsoft/m365-agent-templates](https://github.com/microsoft/m365-agent-templates) — the open-source home for M365 Copilot and Copilot Studio agent templates.

Covers the full telemetry picture across **Declarative Agents (DA)** distributed via GitHub and **Copilot Studio Agents (CA)** distributed via AppSource / Power Platform solutions.

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

---

## 📐 Telemetry Data Sources — Complete Reference

**DA** = Declarative Agent (M365 Agent Builder, distributed via GitHub).
**CA** = Copilot Studio Agent (Power Platform solution, distributed via AppSource / solution import).

### DA vs CA Data Source Matrix

| # | Data Point | DA Source | CA Source |
|---|-----------|----------|----------|
| 1 | GH Landing Page downloads | [✅ GitHub Releases API](#1-github-landing-page--downloads-by-agent-by-file-and-whole-repo) | [✅ GitHub Releases API](#1-github-landing-page--downloads-by-agent-by-file-and-whole-repo) |
| 2 | GH Repo traffic | [✅ GitHub Traffic API](#2-github-repo--traffic-whole-repo-only) | [✅ GitHub Traffic API](#2-github-repo--traffic-whole-repo-only) |
| 3 | Marketplace downloads | ❌ N/A | [✅ AppSource publisher analytics](#3-marketplace-downloads--copilot-agents-library) |
| 4 | TCT clicks (HPA templates) | [✅ TCT site analytics (TBD)](#4-clicks-via-tct-hpa-templates-site) | ❌ N/A |
| 5 | Agent Library in-app downloads | [✅ Custom telemetry (Code App)](#5-downloads-via-the-copilot-agents-library-in-app) | [✅ Custom telemetry (Code App)](#5-downloads-via-the-copilot-agents-library-in-app) |
| 6 | Sideloaded app installs | [✅ M365/Teams Admin (Justin dashboard)](#6-by-app-ids-for-sideloaded-apps) | ❌ N/A |
| 7 | MCS publisher installs | ❌ N/A | [✅ CRMAnalytics Kusto](#7-by-publisher-for-mcs-agents) |
| 8 | Agent Library app installs | ❌ N/A | [✅ CRMAnalytics Kusto + AppSource](#8-installs-of-the-copilot-agents-library-the-app-itself) |
| 9 | Individual agent installs | ❌ N/A (sideload = per-app tracking) | [✅ CRMAnalytics Kusto (two-layer)](#9-installs-of-individual-agents-via-the-copilot-agents-library) |
| 10 | CSK installs | ❌ N/A | [✅ CRMAnalytics Kusto](#10-installs-via-the-copilot-studio-kit) |

---

### 📥 DOWNLOADS

#### 1. GitHub Landing Page — Downloads by Agent, by File, and Whole Repo

| Field | Value |
|-------|-------|
| **Source** | GitHub Releases API |
| **Applies to** | DA + CA (both template types live in the same repo) |
| **API** | `GET /repos/microsoft/m365-agent-templates/releases` |
| **What you get** | Per-release, per-asset `download_count` — break down by agent (tag) and by file |
| **Retention** | Cumulative (all-time) ✅ |
| **Auth** | PAT with `repo` scope or `gh auth token` with push access |

> **⚠️ STATUS: No releases exist yet (0 releases as of Apr 2026).** All template .zips currently live in the repo tree, which means **downloads are NOT being tracked**. Releases must be created and all download links re-routed before this data source is active.

> **Critical:** Only Release assets have download counters. Files in the repo tree (.zip in a folder) are NOT tracked. All download links (aka.ms, README, SharePoint, field decks) must route to Release asset URLs or counts are invisible.

**Release asset URL pattern:**
```
https://github.com/microsoft/m365-agent-templates/releases/download/{tag}/{filename}
```

**Files to track per template (current repo tree paths → must become Release assets):**

| Template | Type | Repo Tree Path (current, NOT tracked) | .zip Filename | Planned Release Tag |
|----------|------|---------------------------------------|---------------|---------------------|
| Plan My Day | DA | `/Plan My Day/PlanMyDay_v1.0.0.0.zip` | `PlanMyDay_v1.0.0.0.zip` (36 KB) | `plan-my-day-v1.0.0` |
| My Company Policy | DA | `/My Company Policy/MyCompanyPolicy_1_0_0_0.zip` | `MyCompanyPolicy_1_0_0_0.zip` (80 KB) | `my-company-policy-v1.0.0` |
| Executive Briefing | DA | `/Executive Briefing/ExecutiveBriefingAgent_v1.0.0.0.zip` | `ExecutiveBriefingAgent_v1.0.0.0.zip` (36 KB) | `executive-briefing-v1.0.0` |
| Request Tracker | CA | `/Request Tracker/RequestTrackerAgent_1_0_0_0.zip` | `RequestTrackerAgent_1_0_0_0.zip` (211 KB) | `request-tracker-v1.0.0` |
| Know My Customer | CA | `/Know My Customer/KnowMyCustomer_1_0_0_1.zip` | `KnowMyCustomer_1_0_0_1.zip` (126 KB) | `know-my-customer-v1.0.0` |

**Additional trackable files per template:**

| File Type | Example Path | Useful For |
|-----------|-------------|------------|
| Setup Guide PDF | `/Plan My Day/Plan My Day Agent - Setup Guide.pdf` | Measures intent to deploy |
| Overview Deck PPTX | `/Plan My Day/Plan My Day Agent - Overview Deck.pptx` | Measures field/sales interest |
| Eval Test Plan PDF | `/Plan My Day/Plan My Day Agent - Evaluation Test Plan.pdf` | Measures serious evaluators |
| Word Template | `/Know My Customer/Know My Customer Agent - Word Template.docx` | Measures active customizers |

> **Action needed:** Create GitHub Releases with `gh release create`, attach all .zips as assets, and re-point all aka.ms / README / SharePoint links to Release asset URLs.

#### 2. GitHub Repo — Traffic (Whole Repo Only)

| Field | Value |
|-------|-------|
| **Source** | GitHub Traffic API |
| **Applies to** | DA + CA (repo = `microsoft/m365-agent-templates`, traffic is repo-wide covering all templates) |
| **Retention** | ⚠️ Rolling 14-day window — must collect weekly to preserve history |
| **Auth** | Requires **push access** to the repo (read-only tokens get 403) |

**Endpoints:**

| Endpoint | Data |
|----------|------|
| `GET /repos/{owner}/{repo}/traffic/views` | Daily page views + unique visitors |
| `GET /repos/{owner}/{repo}/traffic/clones` | Daily clones + unique cloners |
| `GET /repos/{owner}/{repo}/traffic/popular/paths` | Top 10 most-viewed paths |
| `GET /repos/{owner}/{repo}/traffic/popular/referrers` | Top referral sources |

**Expected popular paths (per-template breakdown):**

The popular paths endpoint returns the top 10 viewed pages. Template-specific paths to watch:

| Path | Template |
|------|----------|
| `/microsoft/m365-agent-templates` | Repo landing page (all) |
| `/microsoft/m365-agent-templates/tree/main/Plan%20My%20Day` | Plan My Day (DA) |
| `/microsoft/m365-agent-templates/tree/main/My%20Company%20Policy` | My Company Policy (DA) |
| `/microsoft/m365-agent-templates/tree/main/Executive%20Briefing` | Executive Briefing (DA) |
| `/microsoft/m365-agent-templates/tree/main/Request%20Tracker` | Request Tracker (CA) |
| `/microsoft/m365-agent-templates/tree/main/Know%20My%20Customer` | Know My Customer (CA) |

**Clone caveats:**
- "Download ZIP" (green Code button) counts as a clone, not a tracked download
- Clones include CI/GitHub Actions — no way to filter bots from real users
- "Unique cloners" = distinct IP addresses, not GitHub accounts
- Each ephemeral CI runner = new IP = new "unique"

**Metric trust levels:**

| Metric | Use For | Bot/CI Risk |
|--------|---------|-------------|
| Unique visitors (views) | Awareness/reach | 🟢 Low |
| Release downloads | **Actual adoption (best signal)** | 🟢 Low |
| Referrers | Attribution (where humans came from) | 🟢 Clean |
| Unique cloners | Developer interest | 🟡 Medium (CI inflates) |
| Total clones | Vanity only | 🔴 High (CI inflates heavily) |

#### 3. Marketplace Downloads — Copilot Agents Library

| Field | Value |
|-------|-------|
| **Source** | AppSource / Marketplace publisher analytics |
| **Applies to** | CA (the Agent Library app is a Power Platform solution) |
| **Marketplace URL** | [`microsoftpowercatarch.agentlibrary-preview`](https://marketplace.microsoft.com/en-us/product/dynamics-365/microsoftpowercatarch.agentlibrary-preview) |
| **Publisher ID** | `microsoftpowercatarch` |
| **Offer ID** | `agentlibrary-preview` |
| **Flight Code** | `048a8669f61d44538b22ff5adf102788` |
| **Status** | Preview (flight-gated) |

AppSource provides its own analytics dashboard for publishers. This tracks the Agent Library *app itself*, not individual templates within it.

**Plugin/referrer attribution (TBD):** If the Agent Library Code App opens the AppSource URL (e.g., via a button or iframe), AppSource analytics *may* capture the referrer URL — but this depends on whether the request is a browser-initiated navigation (referrer visible) vs. a server-side/API call (referrer not visible). Code Apps run in a Managed Host iframe which may further strip referrer headers. **Action:** Test whether AppSource publisher analytics shows referrer breakdown, and whether requests originating from the Code App are distinguishable from organic marketplace traffic.

#### 4. Clicks via TCT (HPA Templates Site)

| Field | Value |
|-------|-------|
| **Source** | TCT site analytics (TBD — likely 1DS / App Insights on the TCT web surface) |
| **Applies to** | DA (HPA templates linked from TCT) |
| **Deep links** | TCT → Agent Gallery per agent: `planMyDay`, `knowMyCustomer`, `executiveBriefing`, `myCompanyPolicy`, `requestTracker` |
| **Status** | Deep links ready (Mehdi) but integration pending alignment |

Click tracking depends on TCT's own telemetry implementation. Confirm with Mehdi/Chithra what analytics are instrumented on those deep links.

#### 5. Downloads via the Copilot Agents Library (In-App)

| Field | Value |
|-------|-------|
| **Source** | Agent Library Code App (custom telemetry) |
| **Applies to** | Both DA and CA — the Agent Library app serves as a catalog for both types |
| **Current state** | Code Apps CSP blocks direct 1DS telemetry — must route through Dataverse Custom APIs |
| **DA flow** | User clicks "Customize & Download" / "Use Agent Builder" / "Build with Visual Studio" → download triggers |
| **CA flow** | User clicks deploy → solution import into their environment |

---

### 📦 INSTALLS

#### 6. By App IDs for Sideloaded Apps

| Field | Value |
|-------|-------|
| **Source** | M365 Admin / Teams Admin Center telemetry |
| **Applies to** | DA only — M365 Agent Builder DAs are sideloaded as Teams app packages |
| **Install method** | Sideload via Teams or Teams Admin Center |
| **Tracking** | By specific App IDs embedded in each DA's `manifest.json` |
| **Status** | 🚧 Justin is creating a dashboard — no self-serve source yet |

No zero-setup API exists to programmatically sideload. `POST /appCatalogs/teamsApps` requires `AppCatalog.Submit` or `AppCatalog.ReadWrite.All`. Install tracking requires M365 admin telemetry or Teams usage reports.

#### 7. By Publisher for MCS Agents

| Field | Value |
|-------|-------|
| **Source** | **CRMAnalytics Kusto** (CA) |
| **Kusto database** | `CRMAnalytics` across 11 global clusters |
| **Primary cluster** | `fdislandswebusby2.westus.kusto.windows.net` |
| **Key tables** | `OrgSolutionsInstalled`, `SolutionImport`, `OrganizationDetails` |
| **Filter** | `PublisherUniqueName == "<MCS publisher name>"` |
| **Retention** | `OrgSolutionsInstalled` = rolling 7d snapshot; `SolutionImport` = 180d history |
| **Access** | BIC-DataAccess-US/EU via [myaccess.microsoft.com](https://myaccess.microsoft.com); VPN required |

CA-specific — DAs don't go through Dataverse solution import.

#### 8. Installs of the Copilot Agents Library (the App Itself)

| Field | Value |
|-------|-------|
| **Source** | **CRMAnalytics Kusto** (CA) + AppSource publisher analytics |
| **Kusto filter** | `SolutionUniqueName` for the Agent Library solution (confirm exact name via `pac application list`) |
| **AppSource** | Publisher dashboard analytics for `microsoftpowercatarch.agentlibrary-preview` |
| **Kusto tables** | `OrgSolutionsInstalled` (current state), `SolutionImport` (historical events) |

Two signals: Kusto tells you which orgs/tenants have it installed. AppSource tells you the download/install funnel from the marketplace listing.

#### 9. Installs of Individual Agents via the Copilot Agents Library

| Field | Value |
|-------|-------|
| **Source** | **CRMAnalytics Kusto** (CA) |
| **Layer 1 — Install signal** | `SolutionUniqueName startswith "AgentLib_"` in `OrgSolutionsInstalled` / `SolutionImport` |
| **Layer 2 — Durable usage** | Bot schema names in `ChatbotDetails` (immutable, survives solution moves) |

**Why two layers:** Users may move agents to their own solutions after import, breaking solution-level tracking. Bot schema names are **immutable** and persist regardless.

**Solution names → Bot schema mapping:**

| Template | Solution Name | Bot Schema (Durable) |
|----------|---------------|---------------------|
| Daily Planner | `AgentLib_DailyPlanner` | `cat_dailyplanner` |
| Customer Researcher | `AgentLib_CustomerResearcher` | `cat_customerresearcher` |
| Executive Insights | `AgentLib_ExecutiveInsights` | `cat_executiveinsights` |
| Company Policy Q&A | `AgentLib_CompanyPolicyQA` | `cat_companypolicyqa` |
| Request Tracker | `AgentLib_RequestTracker` | `cat_requesttracker` |

**Layer 1 KQL:**
```kql
OrgSolutionsInstalled
| where SolutionUniqueName startswith "AgentLib_"
| where PublisherUniqueName == "PowerCat"
| summarize Environments = dcount(OrganizationId) by SolutionUniqueName, SolutionVersion
| order by Environments desc
```

**Layer 2 KQL (durable):**
```kql
ChatbotDetails
| where BotSchemaName in (
    "cat_dailyplanner", "cat_customerresearcher", "cat_executiveinsights",
    "cat_companypolicyqa", "cat_requesttracker"
)
| summarize Environments = dcount(OrganizationId), Bots = count() by BotSchemaName
| order by Environments desc
```

#### 10. Installs via the Copilot Studio Kit

| Field | Value |
|-------|-------|
| **Source** | **CRMAnalytics Kusto** (CA) |
| **Kusto filter** | `PublisherUniqueName == "PowerCat"` AND `SolutionUniqueName startswith "CopilotStudio"` |
| **Component Library** | `SolutionUniqueName startswith "CopilotStudioKit_"` |
| **Per-feature MAU** | **PPUXAnalytics Kusto** (13 clusters) — Canvas app page loads mapped to CSK page names via `SolutionComponentInfo` |

CA-specific. Full CSK install base query excludes 5 known test tenants.

---

### 🔧 GitHub API Quick Reference

```
Base: https://api.github.com/repos/microsoft/m365-agent-templates

GET /releases                          → per-asset download_count (cumulative, all-time)
GET /traffic/views                     → daily views + unique visitors (14d rolling)
GET /traffic/clones                    → daily clones + unique cloners (14d rolling)
GET /traffic/popular/paths             → top 10 viewed paths (14d rolling)
GET /traffic/popular/referrers         → top referral sources (14d rolling)
```

**Auth header:**
```
Authorization: Bearer <token>
Accept: application/vnd.github+json
X-GitHub-Api-Version: 2022-11-28
```

**Quick check (PowerShell):**
```powershell
$headers = @{
    Authorization = "Bearer $env:GITHUB_TOKEN"
    Accept = "application/vnd.github+json"
    "X-GitHub-Api-Version" = "2022-11-28"
}
$base = "https://api.github.com/repos/microsoft/m365-agent-templates"

# Views
Invoke-RestMethod "$base/traffic/views" -Headers $headers | ConvertTo-Json

# Clones
Invoke-RestMethod "$base/traffic/clones" -Headers $headers | ConvertTo-Json

# Release download counts
Invoke-RestMethod "$base/releases" -Headers $headers |
  ForEach-Object { "$($_.tag_name): $(($_.assets | Measure-Object download_count -Sum).Sum) downloads" }
```

### 🔧 Kusto Quick Reference

| System | Table | Filter | DA/CA |
|--------|-------|--------|-------|
| CRMAnalytics | `OrgSolutionsInstalled` | `SolutionUniqueName startswith "AgentLib_"` | CA |
| CRMAnalytics | `SolutionImport` | `solutionName startswith "AgentLib_"` | CA |
| CRMAnalytics | `ChatbotDetails` | `BotSchemaName in ("cat_dailyplanner", ...)` | CA |
| CRMAnalytics | `OrganizationDetails` | Join on OrganizationId | CA |
| PPUXAnalytics | `OutgoingRequest` | AppId from `SolutionComponentInfo` | CA |
| `powerautomatefunbipme` | `dimTenant` | `IsTestTenant == 0` | CA |

**CRMAnalytics global union (11 clusters):**

| Geo | Cluster URI |
|-----|-------------|
| 🇺🇸 NA | `fdislandswebusby2.westus.kusto.windows.net` |
| 🇪🇺 EMEA-West | `fdislandswebeuams.westeurope.kusto.windows.net` |
| 🇪🇺 EMEA-North | `fdislandswebeudb3.northeurope.kusto.windows.net` |
| 🇦🇺 Oceania | `fdislandswebausyd.australiaeast.kusto.windows.net` |
| 🇯🇵 Japan | `fdislandswebjptyo.japaneast.kusto.windows.net` |
| 🇨🇦 Canada | `fdislandswebcayto.canadacentral.kusto.windows.net` |
| 🇫🇷 France | `fdislandswebfrfrc.francecentral.kusto.windows.net` |
| 🇩🇪 Germany | `fdislandswebdegec.germanywestcentral.kusto.windows.net` |
| 🇨🇭 Switzerland | `fdislandswebchzrh.switzerlandnorth.kusto.windows.net` |
| 🇳🇴 Norway | `fdislandswebnoeno.norwayeast.kusto.windows.net` |
| 🇸🇪 Sweden | `fdislandswebsecse.swedencentral.kusto.windows.net` |

**PPUXAnalytics clusters (13):**

| Geo | Cluster URI |
|-----|-------------|
| US | `ppuxunitedstates.centralus.kusto.windows.net` |
| Europe | `ppuxeurope.westeurope.kusto.windows.net` |
| UK | `ppuxunitedkingdom.uksouth.kusto.windows.net` |
| Germany | `ppuxgermany.germanywestcentral.kusto.windows.net` |
| France | `ppuxfrance.francecentral.kusto.windows.net` |
| Switzerland | `ppuxswitzerland.switzerlandnorth.kusto.windows.net` |
| Norway | `ppuxnorway.norwayeast.kusto.windows.net` |
| Australia | `ppuxaustralia.australiaeast.kusto.windows.net` |
| Japan | `ppuxjapan.japaneast.kusto.windows.net` |
| Canada | `ppuxcanada.canadacentral.kusto.windows.net` |
| India | `ppuxindia.centralindia.kusto.windows.net` |
| Asia | `ppuxasia.southeastasia.kusto.windows.net` |
| UAE | `ppuxuae.uaenorth.kusto.windows.net` |

**Access:** BIC-DataAccess-US/EU entitlements via [myaccess.microsoft.com](https://myaccess.microsoft.com). VPN required for all fdislands clusters.

### ⚠️ Known Gotchas

**GitHub:**
- Traffic API requires **push access** — read-only tokens get 403
- Traffic data is a **rolling 14-day window** — collect weekly to preserve history
- `gh auth token` may lack `repo` scope — create classic PAT if needed
- Clones include CI/GitHub Actions — no way to filter bots from real users
- "Download ZIP" button counts as a clone but repo tree .zips have NO download counters
- Only Release assets have download counters — all download links must route to Release assets
- "Unique cloners" = IP addresses, not accounts — CI runners inflate unique counts

**Kusto:**
- Cannot use `let db = cluster(...).database(...); db.Table` — must inline full cluster paths
- `SolutionImport` uses `publisherName` but `SolutionUninstall` uses `uniquePublisherName` (different column names!)
- `SolutionImport` has `hasImportFailed` (bool) but `SolutionUninstall` has `isSuccess` (inverted logic!)
- All Kusto clusters require Microsoft corpnet (VPN)

**Code App telemetry:**
- Code Apps CSP blocks direct 1DS telemetry — must route through Custom APIs

---

## ⚠️ Download Tracking — The Critical Rule

GitHub only tracks downloads for **Release assets**. Files in the repo tree (the .zip files inside each template folder) are **NOT counted** when downloaded.

**The rule:** Every download link — aka.ms, SharePoint, field decks, README — must point to a **GitHub Release asset URL** (or an aka.ms redirect to one). If someone copies the .zip to SharePoint and shares that link, those downloads are invisible.

| Source | ✅ Do | ❌ Don't |
|--------|------|---------|
| README.md | Link to Release asset or aka.ms | Link to blob in repo tree |
| SharePoint page | aka.ms → Release asset | Upload .zip to SPO library |
| Field deck / email | aka.ms → Release asset | Attach .zip directly |
| Agent Library app | "Download" → Release asset URL | Serve from Dataverse/blob |

See the [teaching guide](github-telemetry-guide.html) section 10a for the full breakdown and `gh release create` commands.

## 🔑 Prerequisites

- GitHub PAT with `repo` scope (traffic endpoints need push access)
- PowerShell 7+ and `gh` CLI
- For Fabric notebook: access to "Power CAT Team" workspace
- For Kusto: BIC-DataAccess-US/EU entitlements + VPN

## 👤 Team

Built by the Copilot Advisory Team (CAT) at Microsoft.
