import zipfile, json, os

output_path = os.path.expanduser(r'~\dev\m365-agent-templates-metrics\AgentTemplatesTelemetry.pbit')

def utf16le(text):
    return b'\xff\xfe' + text.encode('utf-16-le')

github_cluster = 'https://mcscatkustocluster.westus.kusto.windows.net'
crm_cluster = 'https://fdislandswebusby2.westus.kusto.windows.net'

def adx_m(cluster, db, query):
    return [
        'let',
        f'    Source = AzureDataExplorer.Contents("{cluster}", "{db}", "{query}", [MaxRows=null, MaxSize=null, NoTruncate=null, AdditionalSetStatements=null])',
        'in',
        '    Source'
    ]

# Cross-cluster KQL for agent template installs
crm_install_kql = (
    'let _OrgSolutions = OrgSolutionsInstalled'
    ' | union cluster(\\"fdislandswebeuams.westeurope.kusto.windows.net\\").database(\\"CRMAnalytics\\").OrgSolutionsInstalled'
    ' | union cluster(\\"fdislandswebeudb3.northeurope.kusto.windows.net\\").database(\\"CRMAnalytics\\").OrgSolutionsInstalled'
    ' | union cluster(\\"fdislandswebausyd.australiaeast.kusto.windows.net\\").database(\\"CRMAnalytics\\").OrgSolutionsInstalled'
    ' | union cluster(\\"fdislandswebjptyo.japaneast.kusto.windows.net\\").database(\\"CRMAnalytics\\").OrgSolutionsInstalled'
    ' | union cluster(\\"fdislandswebcayto.canadacentral.kusto.windows.net\\").database(\\"CRMAnalytics\\").OrgSolutionsInstalled;'
    ' let _OrgDetails = OrganizationDetails'
    ' | union cluster(\\"fdislandswebeuams.westeurope.kusto.windows.net\\").database(\\"CRMAnalytics\\").OrganizationDetails'
    ' | union cluster(\\"fdislandswebeudb3.northeurope.kusto.windows.net\\").database(\\"CRMAnalytics\\").OrganizationDetails'
    ' | union cluster(\\"fdislandswebausyd.australiaeast.kusto.windows.net\\").database(\\"CRMAnalytics\\").OrganizationDetails'
    ' | union cluster(\\"fdislandswebjptyo.japaneast.kusto.windows.net\\").database(\\"CRMAnalytics\\").OrganizationDetails'
    ' | union cluster(\\"fdislandswebcayto.canadacentral.kusto.windows.net\\").database(\\"CRMAnalytics\\").OrganizationDetails;'
    ' let _TenantNames = cluster(\\"powerautomatefunbipme.eastus2.kusto.windows.net\\")'
    '.database(\\"SelfServiceData\\").dimTenant'
    ' | where IsTestTenant == 0 | project TenantId, TenantName;'
    ' _OrgSolutions'
    ' | where PublisherUniqueName == \\"PowerCat\\"'
    ' | where SolutionUniqueName startswith \\"AgentLib_\\" or SolutionUniqueName startswith \\"CopilotStudio\\"'
    ' | where Geo !in (\\"TST\\", \\"TIP1\\", \\"TIP2\\")'
    ' | join kind=leftouter (_OrgDetails | project OrganizationId=Id, FriendlyName, DomainName, TenantId, Geo, CountryCode, UserCount) on $left.OrganizationId == $right.OrganizationId'
    ' | join kind=leftouter _TenantNames on TenantId'
    ' | project SolutionUniqueName, SolutionVersion, OrganizationId, FriendlyName, DomainName, TenantName, Geo, CountryCode, UserCount, InstalledOn, IsManaged'
)

model = {
    "name": "AgentTemplatesTelemetry",
    "compatibilityLevel": 1567,
    "model": {
        "culture": "en-US",
        "dataAccessOptions": {
            "legacyRedirects": True,
            "returnErrorValuesAsNull": True
        },
        "defaultPowerBIDataSourceVersion": "powerBI_V3",
        "sourceQueryCulture": "en-US",
        "tables": [
            {
                "name": "GitHubTrafficDaily",
                "columns": [
                    {"name": "CollectedDate", "dataType": "dateTime", "sourceColumn": "CollectedDate"},
                    {"name": "Date", "dataType": "dateTime", "sourceColumn": "Date"},
                    {"name": "Views", "dataType": "int64", "sourceColumn": "Views"},
                    {"name": "UniqueVisitors", "dataType": "int64", "sourceColumn": "UniqueVisitors"},
                    {"name": "Clones", "dataType": "int64", "sourceColumn": "Clones"},
                    {"name": "UniqueCloners", "dataType": "int64", "sourceColumn": "UniqueCloners"}
                ],
                "partitions": [{
                    "name": "GitHubTrafficDaily",
                    "dataView": "full",
                    "source": {
                        "type": "m",
                        "expression": adx_m(github_cluster, "GitHubTelemetry", "GitHubTrafficDaily")
                    }
                }]
            },
            {
                "name": "GitHubPopularContent",
                "columns": [
                    {"name": "CollectedDate", "dataType": "dateTime", "sourceColumn": "CollectedDate"},
                    {"name": "Path", "dataType": "string", "sourceColumn": "Path"},
                    {"name": "Views", "dataType": "int64", "sourceColumn": "Views"},
                    {"name": "UniqueVisitors", "dataType": "int64", "sourceColumn": "UniqueVisitors"}
                ],
                "partitions": [{
                    "name": "GitHubPopularContent",
                    "dataView": "full",
                    "source": {
                        "type": "m",
                        "expression": adx_m(github_cluster, "GitHubTelemetry", "GitHubPopularContent")
                    }
                }]
            },
            {
                "name": "GitHubReferrers",
                "columns": [
                    {"name": "CollectedDate", "dataType": "dateTime", "sourceColumn": "CollectedDate"},
                    {"name": "Referrer", "dataType": "string", "sourceColumn": "Referrer"},
                    {"name": "Views", "dataType": "int64", "sourceColumn": "Views"},
                    {"name": "UniqueVisitors", "dataType": "int64", "sourceColumn": "UniqueVisitors"}
                ],
                "partitions": [{
                    "name": "GitHubReferrers",
                    "dataView": "full",
                    "source": {
                        "type": "m",
                        "expression": adx_m(github_cluster, "GitHubTelemetry", "GitHubReferrers")
                    }
                }]
            },
            {
                "name": "GitHubRepoStats",
                "columns": [
                    {"name": "CollectedDate", "dataType": "dateTime", "sourceColumn": "CollectedDate"},
                    {"name": "Stars", "dataType": "int64", "sourceColumn": "Stars"},
                    {"name": "Forks", "dataType": "int64", "sourceColumn": "Forks"},
                    {"name": "Watchers", "dataType": "int64", "sourceColumn": "Watchers"},
                    {"name": "OpenIssues", "dataType": "int64", "sourceColumn": "OpenIssues"},
                    {"name": "TotalViews14d", "dataType": "int64", "sourceColumn": "TotalViews14d"},
                    {"name": "UniqueVisitors14d", "dataType": "int64", "sourceColumn": "UniqueVisitors14d"},
                    {"name": "TotalClones14d", "dataType": "int64", "sourceColumn": "TotalClones14d"},
                    {"name": "UniqueCloners14d", "dataType": "int64", "sourceColumn": "UniqueCloners14d"}
                ],
                "partitions": [{
                    "name": "GitHubRepoStats",
                    "dataView": "full",
                    "source": {
                        "type": "m",
                        "expression": adx_m(github_cluster, "GitHubTelemetry", "GitHubRepoStats")
                    }
                }]
            },
            {
                "name": "CRMAgentInstalls",
                "columns": [
                    {"name": "SolutionUniqueName", "dataType": "string", "sourceColumn": "SolutionUniqueName"},
                    {"name": "SolutionVersion", "dataType": "string", "sourceColumn": "SolutionVersion"},
                    {"name": "OrganizationId", "dataType": "string", "sourceColumn": "OrganizationId"},
                    {"name": "FriendlyName", "dataType": "string", "sourceColumn": "FriendlyName"},
                    {"name": "DomainName", "dataType": "string", "sourceColumn": "DomainName"},
                    {"name": "TenantName", "dataType": "string", "sourceColumn": "TenantName"},
                    {"name": "Geo", "dataType": "string", "sourceColumn": "Geo"},
                    {"name": "CountryCode", "dataType": "string", "sourceColumn": "CountryCode"},
                    {"name": "UserCount", "dataType": "int64", "sourceColumn": "UserCount"},
                    {"name": "InstalledOn", "dataType": "dateTime", "sourceColumn": "InstalledOn"},
                    {"name": "IsManaged", "dataType": "boolean", "sourceColumn": "IsManaged"}
                ],
                "partitions": [{
                    "name": "CRMAgentInstalls",
                    "dataView": "full",
                    "source": {
                        "type": "m",
                        "expression": adx_m(crm_cluster, "CRMAnalytics", crm_install_kql)
                    }
                }]
            }
        ],
        "annotations": [
            {"name": "PBI_QueryOrder", "value": json.dumps(["GitHubTrafficDaily", "GitHubPopularContent", "GitHubReferrers", "GitHubRepoStats", "CRMAgentInstalls"])},
            {"name": "PBIDesktopVersion", "value": "2.140.1045.0 (25.04)"}
        ]
    }
}

diagram = {"version": "1.0", "pages": [], "scrollPosition": {"x": 0, "y": 0}}

report_layout = {
    "id": 0,
    "reportId": "00000000-0000-0000-0000-000000000001",
    "config": json.dumps({
        "version": "5.53",
        "themeCollection": {"baseTheme": {"name": "CY24SU06", "version": "5.53", "type": 2}},
        "activeSectionIndex": 0,
        "defaultDrillFilterOtherVisuals": True,
        "linguisticSchemaSyncVersion": 2,
        "settings": {
            "useStylableVisualContainerHeader": True,
            "exportDataMode": 1,
            "useDefaultAggregateDisplayName": True
        }
    }),
    "filters": "[]",
    "resourcePackages": [],
    "sections": [
        {
            "name": "Overview",
            "displayName": "Overview",
            "displayOption": 1,
            "width": 1280,
            "height": 720,
            "filters": "[]",
            "ordinal": 0,
            "visualContainers": [],
            "config": json.dumps({"name": "Overview", "layouts": [{"id":0, "position": {"x":0,"y":0,"width":1280,"height":720}}]})
        },
        {
            "name": "GitHubTraffic",
            "displayName": "GitHub Traffic",
            "displayOption": 1,
            "width": 1280,
            "height": 720,
            "filters": "[]",
            "ordinal": 1,
            "visualContainers": [],
            "config": json.dumps({"name": "GitHubTraffic", "layouts": [{"id":0, "position": {"x":0,"y":0,"width":1280,"height":720}}]})
        },
        {
            "name": "CRMInstalls",
            "displayName": "CRM Agent Installs",
            "displayOption": 1,
            "width": 1280,
            "height": 720,
            "filters": "[]",
            "ordinal": 2,
            "visualContainers": [],
            "config": json.dumps({"name": "CRMInstalls", "layouts": [{"id":0, "position": {"x":0,"y":0,"width":1280,"height":720}}]})
        }
    ],
    "publicCustomVisuals": []
}

settings = {"QueriesMetadata": {}, "Version": 1}
metadata = {"version": 2, "checksum": ""}

content_types = '''<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="json" ContentType="application/json" />
  <Default Extension="xml" ContentType="application/xml" />
</Types>'''

with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.writestr('[Content_Types].xml', content_types)
    zf.writestr('Version', '2.0')
    zf.writestr('SecurityBindings', b'')
    zf.writestr('DataModelSchema', utf16le(json.dumps(model, indent=2)))
    zf.writestr('DiagramLayout', utf16le(json.dumps(diagram)))
    zf.writestr('Report/Layout', utf16le(json.dumps(report_layout)))
    zf.writestr('Settings', utf16le(json.dumps(settings)))
    zf.writestr('Metadata', utf16le(json.dumps(metadata)))

print(f'Created: {output_path}')
print(f'Size: {os.path.getsize(output_path):,} bytes')
print(f'Tables: GitHubTrafficDaily, GitHubPopularContent, GitHubReferrers, GitHubRepoStats, CRMAgentInstalls')
print(f'Pages: Overview, GitHub Traffic, CRM Agent Installs')
