import json, uuid

def uid():
    return str(uuid.uuid4())

github_ds_id = uid()
crm_ds_id = uid()

overview_page = uid()
traffic_page = uid()
content_page = uid()
installs_page = uid()

dashboard = {
    "schema_version": 72,
    "title": "M365 Agent Templates - GitHub + Install Telemetry",
    "autoRefresh": {"enabled": True, "defaultInterval": "1h", "minInterval": "5m"},
    "parameters": [],
    "baseQueries": [],
    "dataSources": [
        {
            "id": github_ds_id,
            "name": "GitHubTelemetry",
            "clusterUri": "https://mcscatkustocluster.westus.kusto.windows.net",
            "database": "GitHubTelemetry",
            "kind": "manual-kusto"
        },
        {
            "id": crm_ds_id,
            "name": "CRMAnalytics",
            "clusterUri": "https://fdislandswebusby2.westus.kusto.windows.net",
            "database": "CRMAnalytics",
            "kind": "manual-kusto"
        }
    ],
    "pages": [
        {"name": "Overview", "id": overview_page},
        {"name": "GitHub Traffic", "id": traffic_page},
        {"name": "Popular Content & Referrers", "id": content_page},
        {"name": "CRM Installs", "id": installs_page}
    ],
    "queries": [],
    "tiles": []
}

def add_query(text, ds_id):
    qid = uid()
    dashboard["queries"].append({
        "id": qid,
        "text": text,
        "usedVariables": [],
        "dataSource": {"kind": "inline", "dataSourceId": ds_id}
    })
    return qid

def add_tile(page_id, query_id, title, vtype, x, y, w, h, vopts=None):
    # ADX requires min 4x4 tiles and "card" not "stat"
    if vtype == "stat":
        vtype = "card"
    w = max(w, 4)
    h = max(h, 4)
    dashboard["tiles"].append({
        "id": uid(),
        "pageId": page_id,
        "queryRef": {"kind": "query", "queryId": query_id},
        "title": title,
        "visualType": vtype,
        "layout": {"x": x, "y": y, "width": w, "height": h},
        "visualOptions": vopts or {}
    })

# ============ OVERVIEW PAGE ============

q = add_query("GitHubRepoStats | summarize TotalViews=max(TotalViews14d)", github_ds_id)
add_tile(overview_page, q, "Total Views (14d)", "card", 0, 0, 4, 4)

q = add_query("GitHubRepoStats | summarize UniqueVisitors=max(UniqueVisitors14d)", github_ds_id)
add_tile(overview_page, q, "Unique Visitors (14d)", "card", 4, 0, 4, 4)

q = add_query("GitHubRepoStats | summarize TotalClones=max(TotalClones14d)", github_ds_id)
add_tile(overview_page, q, "Total Clones (14d)", "card", 8, 0, 4, 4)

q = add_query("GitHubRepoStats | summarize UniqueCloners=max(UniqueCloners14d)", github_ds_id)
add_tile(overview_page, q, "Unique Cloners (14d)", "card", 12, 0, 4, 4)

q = add_query("GitHubRepoStats | summarize Stars=max(Stars)", github_ds_id)
add_tile(overview_page, q, "Stars", "card", 16, 0, 4, 4)

q = add_query("GitHubRepoStats | summarize Forks=max(Forks)", github_ds_id)
add_tile(overview_page, q, "Forks", "card", 20, 0, 4, 4)

q = add_query("GitHubTrafficDaily | order by Date asc | project Date, Views, Clones", github_ds_id)
add_tile(overview_page, q, "Daily Views & Clones", "line", 0, 4, 12, 8)

q = add_query("GitHubReferrers | order by Views desc | project Referrer, Views, UniqueVisitors", github_ds_id)
add_tile(overview_page, q, "Top Referrers", "bar", 12, 4, 12, 8)

q = add_query(
    "GitHubPopularContent"
    " | extend TemplateName = case("
    "     Path has '/Plan My Day', '📅 Plan My Day',"
    "     Path has '/Executive Briefing', '📊 Executive Briefing',"
    "     Path has '/Know My Customer', '🔍 Know My Customer',"
    "     Path has '/My Company Policy', '📋 My Company Policy',"
    "     Path has '/Request Tracker', '📝 Request Tracker',"
    "     Path == ' ' or Path == '', '🏠 Repo Home',"
    "     Path has '/tree/main' and not(Path has '/'), '📂 Root /tree/main',"
    "     strcat('📄 ', Path))"
    " | summarize Views=sum(Views), UniqueVisitors=sum(UniqueVisitors) by TemplateName"
    " | order by Views desc",
    github_ds_id)
add_tile(overview_page, q, "Views by Agent Template", "bar", 0, 12, 12, 8)

q = add_query("GitHubPopularContent | order by Views desc | project Path, Views, UniqueVisitors", github_ds_id)
add_tile(overview_page, q, "All Popular Paths (Raw)", "table", 12, 12, 12, 8)

# ============ GITHUB TRAFFIC PAGE ============

q = add_query("GitHubTrafficDaily | order by Date asc | project Date, Views, UniqueVisitors", github_ds_id)
add_tile(traffic_page, q, "Daily Page Views", "area", 0, 0, 12, 8)

q = add_query("GitHubTrafficDaily | order by Date asc | project Date, Clones, UniqueCloners", github_ds_id)
add_tile(traffic_page, q, "Daily Clones", "area", 12, 0, 12, 8)

q = add_query("GitHubTrafficDaily | order by Date desc | project Date, Views, UniqueVisitors, Clones, UniqueCloners", github_ds_id)
add_tile(traffic_page, q, "Daily Detail", "table", 0, 8, 24, 7)

# ============ CONTENT & REFERRERS PAGE ============

q = add_query(
    "GitHubPopularContent"
    " | extend TemplateName = case("
    "     Path has '/Plan My Day', '📅 Plan My Day',"
    "     Path has '/Executive Briefing', '📊 Executive Briefing',"
    "     Path has '/Know My Customer', '🔍 Know My Customer',"
    "     Path has '/My Company Policy', '📋 My Company Policy',"
    "     Path has '/Request Tracker', '📝 Request Tracker',"
    "     Path == ' ' or Path == '', '🏠 Repo Home',"
    "     strcat('📄 ', Path))"
    " | summarize Views=sum(Views), UniqueVisitors=sum(UniqueVisitors) by TemplateName"
    " | order by Views desc",
    github_ds_id)
add_tile(content_page, q, "Views by Agent Template", "bar", 0, 0, 12, 8)

q = add_query("GitHubReferrers | order by Views desc | project Referrer, Views, UniqueVisitors", github_ds_id)
add_tile(content_page, q, "Traffic Sources", "bar", 12, 0, 12, 8)

q = add_query(
    "GitHubPopularContent"
    " | extend TemplateName = case("
    "     Path has '/Plan My Day', '📅 Plan My Day',"
    "     Path has '/Executive Briefing', '📊 Executive Briefing',"
    "     Path has '/Know My Customer', '🔍 Know My Customer',"
    "     Path has '/My Company Policy', '📋 My Company Policy',"
    "     Path has '/Request Tracker', '📝 Request Tracker',"
    "     Path == ' ' or Path == '', '🏠 Repo Home',"
    "     strcat('📄 ', Path))"
    " | project TemplateName, Path, Views, UniqueVisitors"
    " | order by Views desc",
    github_ds_id)
add_tile(content_page, q, "Content Detail", "table", 0, 8, 12, 7)

q = add_query("GitHubReferrers | order by Views desc | project Referrer, Views, UniqueVisitors", github_ds_id)
add_tile(content_page, q, "Referrer Detail", "table", 12, 8, 12, 7)

# ============ CRM INSTALLS PAGE ============

CRM_UNION = (
    "let _OrgSolutions = OrgSolutionsInstalled"
    " | union cluster('fdislandswebeuams.westeurope.kusto.windows.net').database('CRMAnalytics').OrgSolutionsInstalled"
    " | union cluster('fdislandswebeudb3.northeurope.kusto.windows.net').database('CRMAnalytics').OrgSolutionsInstalled"
    " | union cluster('fdislandswebausyd.australiaeast.kusto.windows.net').database('CRMAnalytics').OrgSolutionsInstalled"
    " | union cluster('fdislandswebjptyo.japaneast.kusto.windows.net').database('CRMAnalytics').OrgSolutionsInstalled"
    " | union cluster('fdislandswebcayto.canadacentral.kusto.windows.net').database('CRMAnalytics').OrgSolutionsInstalled;"
    " let _OrgDetails = OrganizationDetails"
    " | union cluster('fdislandswebeuams.westeurope.kusto.windows.net').database('CRMAnalytics').OrganizationDetails"
    " | union cluster('fdislandswebeudb3.northeurope.kusto.windows.net').database('CRMAnalytics').OrganizationDetails"
    " | union cluster('fdislandswebausyd.australiaeast.kusto.windows.net').database('CRMAnalytics').OrganizationDetails"
    " | union cluster('fdislandswebjptyo.japaneast.kusto.windows.net').database('CRMAnalytics').OrganizationDetails"
    " | union cluster('fdislandswebcayto.canadacentral.kusto.windows.net').database('CRMAnalytics').OrganizationDetails;"
    " let _TenantNames = cluster('powerautomatefunbipme.eastus2.kusto.windows.net').database('SelfServiceData').dimTenant"
    " | where IsTestTenant == 0 | project TenantId, TenantName; "
)

q = add_query(
    CRM_UNION +
    "_OrgSolutions"
    " | where PublisherUniqueName == 'PowerCat'"
    " | where SolutionUniqueName startswith 'AgentLib_'"
    " | where Geo !in ('TST', 'TIP1', 'TIP2')"
    " | summarize InstallCount=dcount(OrganizationId)",
    crm_ds_id)
add_tile(installs_page, q, "Agent Template Installs (Unique Orgs)", "card", 0, 0, 6, 4)

q = add_query(
    CRM_UNION +
    "_OrgSolutions"
    " | where PublisherUniqueName == 'PowerCat'"
    " | where SolutionUniqueName startswith 'AgentLib_'"
    " | where Geo !in ('TST', 'TIP1', 'TIP2')"
    " | summarize Installs=dcount(OrganizationId) by SolutionUniqueName"
    " | order by Installs desc",
    crm_ds_id)
add_tile(installs_page, q, "Installs by Template", "bar", 6, 0, 9, 6)

q = add_query(
    CRM_UNION +
    "_OrgSolutions"
    " | where PublisherUniqueName == 'PowerCat'"
    " | where SolutionUniqueName startswith 'AgentLib_'"
    " | where Geo !in ('TST', 'TIP1', 'TIP2')"
    " | join kind=leftouter (_OrgDetails | project OrganizationId=Id, Geo) on OrganizationId"
    " | summarize Installs=dcount(OrganizationId) by Geo1"
    " | order by Installs desc",
    crm_ds_id)
add_tile(installs_page, q, "Installs by Geo", "pie", 15, 0, 9, 6)

q = add_query(
    CRM_UNION +
    "_OrgSolutions"
    " | where PublisherUniqueName == 'PowerCat'"
    " | where SolutionUniqueName startswith 'AgentLib_'"
    " | where Geo !in ('TST', 'TIP1', 'TIP2')"
    " | join kind=leftouter (_OrgDetails | project OrganizationId=Id, FriendlyName, DomainName, TenantId, Geo, CountryCode, UserCount) on OrganizationId"
    " | join kind=leftouter _TenantNames on TenantId"
    " | project SolutionUniqueName, SolutionVersion, TenantName, FriendlyName, DomainName, Geo, CountryCode, UserCount, InstalledOn"
    " | order by InstalledOn desc",
    crm_ds_id)
add_tile(installs_page, q, "Customer Install List", "table", 0, 6, 24, 9)


out = r"C:\Users\demora\dev\m365-agent-templates-metrics\adx-dashboard.json"
with open(out, "w") as f:
    json.dump(dashboard, f, indent=2)

print(f"Dashboard: {out}")
print(f"Pages: {len(dashboard['pages'])}")
print(f"Tiles: {len(dashboard['tiles'])}")
print(f"Queries: {len(dashboard['queries'])}")
