<#
.SYNOPSIS
    Fetches release download counts and traffic stats for microsoft/m365-agent-templates.

.DESCRIPTION
    Uses the GitHub REST API to pull:
      - Release asset download counts (per asset, per release)
      - Traffic: page views, unique visitors, popular content, clones, referrers
    Requires a GitHub PAT with repo scope (traffic stats need push access).

.PARAMETER Token
    GitHub Personal Access Token. If not provided, checks $env:GITHUB_TOKEN.

.EXAMPLE
    .\m365-agent-templates-metrics.ps1
    .\m365-agent-templates-metrics.ps1 -Token "ghp_xxxx"
#>

param(
    [string]$Token = $env:GITHUB_TOKEN
)

$Owner = "microsoft"
$Repo  = "m365-agent-templates"
$BaseUrl = "https://api.github.com/repos/$Owner/$Repo"

if (-not $Token) {
    Write-Host "`n⚠️  No token found. Set `$env:GITHUB_TOKEN or pass -Token." -ForegroundColor Yellow
    Write-Host "   Traffic stats require a PAT with 'repo' scope and push access.`n" -ForegroundColor Yellow
    exit 1
}

$Headers = @{
    "Accept"               = "application/vnd.github+json"
    "Authorization"        = "Bearer $Token"
    "X-GitHub-Api-Version" = "2022-11-28"
}

function Invoke-GitHubApi {
    param([string]$Url)
    try {
        Invoke-RestMethod -Uri $Url -Headers $Headers -ErrorAction Stop
    } catch {
        $status = $_.Exception.Response.StatusCode.value__
        if ($status -eq 403) {
            Write-Host "   ❌ 403 Forbidden — your token may lack push access for traffic stats." -ForegroundColor Red
        } elseif ($status -eq 404) {
            Write-Host "   ❌ 404 Not Found — check repo name or token permissions." -ForegroundColor Red
        } else {
            Write-Host "   ❌ Error ($status): $($_.Exception.Message)" -ForegroundColor Red
        }
        return $null
    }
}

# ─────────────────────────────────────────────
# 1. RELEASE DOWNLOAD COUNTS
# ─────────────────────────────────────────────
Write-Host "`n╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  📦  RELEASE ASSET DOWNLOAD COUNTS                      ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

$page = 1
$allReleases = @()
do {
    $releases = Invoke-GitHubApi "$BaseUrl/releases?per_page=100&page=$page"
    if ($null -eq $releases) { break }
    $allReleases += $releases
    $page++
} while ($releases.Count -eq 100)

if ($allReleases.Count -eq 0) {
    Write-Host "   No releases found.`n" -ForegroundColor Yellow
} else {
    $totalDownloads = 0
    foreach ($release in $allReleases) {
        $releaseTotal = ($release.assets | Measure-Object -Property download_count -Sum).Sum
        $totalDownloads += $releaseTotal

        $tag = $release.tag_name
        $name = $release.name
        $date = ([datetime]$release.published_at).ToString("yyyy-MM-dd")
        $prerelease = if ($release.prerelease) { " [pre-release]" } else { "" }

        Write-Host "  🏷️  $name ($tag) — $date$prerelease" -ForegroundColor White
        Write-Host "     Release total: $releaseTotal downloads" -ForegroundColor DarkGray

        if ($release.assets.Count -eq 0) {
            Write-Host "     (no uploaded assets)" -ForegroundColor DarkGray
        } else {
            foreach ($asset in $release.assets) {
                $size = [math]::Round($asset.size / 1MB, 2)
                Write-Host "     📄 $($asset.name)  →  $($asset.download_count) downloads  ($size MB)" -ForegroundColor Green
            }
        }
        Write-Host ""
    }

    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host "  🎯 TOTAL DOWNLOADS ACROSS ALL RELEASES: $totalDownloads" -ForegroundColor Cyan
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan
}

# ─────────────────────────────────────────────
# 2. TRAFFIC: PAGE VIEWS
# ─────────────────────────────────────────────
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║  👁️  TRAFFIC — PAGE VIEWS (last 14 days)                ║" -ForegroundColor Magenta
Write-Host "╚══════════════════════════════════════════════════════════╝`n" -ForegroundColor Magenta

$views = Invoke-GitHubApi "$BaseUrl/traffic/views"
if ($views) {
    Write-Host "  Total views:  $($views.count)" -ForegroundColor White
    Write-Host "  Unique visitors: $($views.uniques)`n" -ForegroundColor White
    Write-Host "  Daily breakdown:" -ForegroundColor DarkGray
    foreach ($day in $views.views) {
        $date = ([datetime]$day.timestamp).ToString("yyyy-MM-dd")
        $bar = "█" * [math]::Min($day.count, 50)
        Write-Host "    $date  $($day.count.ToString().PadLeft(5))  $($day.uniques.ToString().PadLeft(4)) uniq  $bar" -ForegroundColor Yellow
    }
    Write-Host ""
}

# ─────────────────────────────────────────────
# 3. TRAFFIC: CLONES
# ─────────────────────────────────────────────
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║  📋  TRAFFIC — CLONES (last 14 days)                    ║" -ForegroundColor Magenta
Write-Host "╚══════════════════════════════════════════════════════════╝`n" -ForegroundColor Magenta

$clones = Invoke-GitHubApi "$BaseUrl/traffic/clones"
if ($clones) {
    Write-Host "  Total clones: $($clones.count)" -ForegroundColor White
    Write-Host "  Unique cloners: $($clones.uniques)`n" -ForegroundColor White
    foreach ($day in $clones.clones) {
        $date = ([datetime]$day.timestamp).ToString("yyyy-MM-dd")
        $bar = "█" * [math]::Min($day.count, 50)
        Write-Host "    $date  $($day.count.ToString().PadLeft(5))  $($day.uniques.ToString().PadLeft(4)) uniq  $bar" -ForegroundColor Yellow
    }
    Write-Host ""
}

# ─────────────────────────────────────────────
# 4. POPULAR CONTENT (most viewed files/paths)
# ─────────────────────────────────────────────
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║  🔥  POPULAR CONTENT (last 14 days)                     ║" -ForegroundColor Magenta
Write-Host "╚══════════════════════════════════════════════════════════╝`n" -ForegroundColor Magenta

$popular = Invoke-GitHubApi "$BaseUrl/traffic/popular/paths"
if ($popular) {
    $rank = 1
    foreach ($item in $popular) {
        Write-Host "  #$rank  $($item.path)" -ForegroundColor White
        Write-Host "       Views: $($item.count)  |  Unique: $($item.uniques)" -ForegroundColor Green
        $rank++
    }
    Write-Host ""
}

# ─────────────────────────────────────────────
# 5. TOP REFERRERS
# ─────────────────────────────────────────────
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║  🔗  TOP REFERRERS (last 14 days)                       ║" -ForegroundColor Magenta
Write-Host "╚══════════════════════════════════════════════════════════╝`n" -ForegroundColor Magenta

$referrers = Invoke-GitHubApi "$BaseUrl/traffic/popular/referrers"
if ($referrers) {
    foreach ($ref in $referrers) {
        Write-Host "  $($ref.referrer)" -ForegroundColor White
        Write-Host "       Views: $($ref.count)  |  Unique: $($ref.uniques)" -ForegroundColor Green
    }
    Write-Host ""
}

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host "  ✅ Done! Data fetched at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor DarkGray
Write-Host "  ℹ️  Traffic stats cover the last 14 days only." -ForegroundColor DarkGray
Write-Host "  ℹ️  Release download counts are cumulative (all-time).`n" -ForegroundColor DarkGray
