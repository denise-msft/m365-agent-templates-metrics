<#
.SYNOPSIS
    Generates view-tracking badges for all folder READMEs in the m365-agent-templates repo.

.DESCRIPTION
    Scans the repo for folders containing README.md files and outputs the badge markdown
    to add to each one. Uses hits.sh for real-time view tracking.

    Can also be pointed at a local clone to auto-insert badges into READMEs.

.PARAMETER Token
    GitHub PAT. Falls back to $env:GITHUB_TOKEN.

.PARAMETER LocalRepoPath
    Path to a local clone. If provided, badges are inserted directly into README files.

.PARAMETER DryRun
    Show what would be changed without modifying files (only applies with -LocalRepoPath).

.EXAMPLE
    # Just show the badge markdown to copy-paste
    .\m365-agent-templates-add-view-badges.ps1

    # Auto-insert into a local clone
    .\m365-agent-templates-add-view-badges.ps1 -LocalRepoPath "C:\repos\m365-agent-templates"

    # Preview changes without modifying
    .\m365-agent-templates-add-view-badges.ps1 -LocalRepoPath "C:\repos\m365-agent-templates" -DryRun
#>

param(
    [string]$Token = $env:GITHUB_TOKEN,
    [string]$LocalRepoPath,
    [switch]$DryRun
)

$Owner = "microsoft"
$Repo  = "m365-agent-templates"
$BaseUrl = "https://api.github.com/repos/$Owner/$Repo"
$RepoUrl = "https://github.com/$Owner/$Repo"
$BadgeMarker = "<!-- view-tracking-badge -->"

if (-not $Token) {
    Write-Host "`n⚠️  No token found. Set `$env:GITHUB_TOKEN or pass -Token." -ForegroundColor Yellow
    exit 1
}

$Headers = @{
    "Accept"               = "application/vnd.github+json"
    "Authorization"        = "Bearer $Token"
    "X-GitHub-Api-Version" = "2022-11-28"
}

function Get-FoldersWithReadme {
    param([string]$Path = "")

    $url = "$BaseUrl/contents/$Path"
    $items = Invoke-RestMethod -Uri $url -Headers $Headers -ErrorAction Stop
    $results = @()

    foreach ($item in $items) {
        if ($item.type -eq "dir") {
            # Check if this folder has a README.md
            try {
                $folderContents = Invoke-RestMethod -Uri "$BaseUrl/contents/$($item.path)" -Headers $Headers -ErrorAction Stop
                $hasReadme = $folderContents | Where-Object { $_.name -eq "README.md" }
                if ($hasReadme) {
                    $results += $item.path
                }
                # Recurse into subfolders
                $results += Get-FoldersWithReadme -Path $item.path
            } catch {
                # Skip inaccessible folders
            }
        }
    }
    return $results
}

function Get-BadgeMarkdown {
    param([string]$FolderPath)

    $trackingPath = "$RepoUrl/tree/main/$FolderPath"
    $encodedPath = $trackingPath -replace "://", "/" -replace "/", "%2F"

    # Visible badge
    $visibleBadge = "[![Views](https://hits.sh/$trackingPath.svg?label=views&color=0078D4)](https://hits.sh/$trackingPath/)"

    # Hidden badge (transparent, no label)
    $hiddenBadge = "![](https://hits.sh/$trackingPath.svg?view=today-total&style=flat-square&label=&color=ffffff&labelColor=ffffff)"

    return @{
        Visible = $visibleBadge
        Hidden  = $hiddenBadge
        Path    = $FolderPath
    }
}

# ─────────────────────────────────────────────
# Scan the repo
# ─────────────────────────────────────────────
Write-Host "`n🔍 Scanning $Owner/$Repo for folders with README.md files...`n" -ForegroundColor Cyan

# Always include root README
$foldersWithReadme = @(".")
$foldersWithReadme += Get-FoldersWithReadme

Write-Host "  Found $($foldersWithReadme.Count) README(s) to add tracking badges to:`n" -ForegroundColor Green
foreach ($f in $foldersWithReadme) {
    $displayPath = if ($f -eq ".") { "/ (root)" } else { "/$f/" }
    Write-Host "    📄 $displayPath" -ForegroundColor White
}

# ─────────────────────────────────────────────
# Generate or insert badges
# ─────────────────────────────────────────────
Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor DarkGray

if ($LocalRepoPath) {
    # ── LOCAL MODE: Insert badges directly ──
    Write-Host "📝 Inserting badges into local clone: $LocalRepoPath`n" -ForegroundColor Cyan

    foreach ($folder in $foldersWithReadme) {
        $readmePath = if ($folder -eq ".") {
            Join-Path $LocalRepoPath "README.md"
        } else {
            Join-Path $LocalRepoPath "$folder\README.md"
        }

        if (-not (Test-Path $readmePath)) {
            Write-Host "  ⚠️  $readmePath not found, skipping." -ForegroundColor Yellow
            continue
        }

        $content = Get-Content $readmePath -Raw
        if ($content -match [regex]::Escape($BadgeMarker)) {
            Write-Host "  ✅ $folder — badge already present, skipping." -ForegroundColor DarkGray
            continue
        }

        $badge = Get-BadgeMarkdown -FolderPath $(if ($folder -eq ".") { "" } else { $folder })

        # For root, use the repo URL directly
        $trackingUrl = if ($folder -eq ".") {
            "$RepoUrl"
        } else {
            "$RepoUrl/tree/main/$folder"
        }
        $badgeLine = "$BadgeMarker`n[![Views](https://hits.sh/$trackingUrl.svg?label=views&color=0078D4)](https://hits.sh/$trackingUrl/)"

        $newContent = "$badgeLine`n`n$content"

        if ($DryRun) {
            Write-Host "  🔍 [DRY RUN] Would add to $folder/README.md:" -ForegroundColor Yellow
            Write-Host "     $badgeLine`n" -ForegroundColor DarkGray
        } else {
            Set-Content -Path $readmePath -Value $newContent -NoNewline
            Write-Host "  ✅ $folder/README.md — badge added!" -ForegroundColor Green
        }
    }

    if (-not $DryRun) {
        Write-Host "`n🎉 Done! Now commit and push:" -ForegroundColor Cyan
        Write-Host "   cd $LocalRepoPath" -ForegroundColor White
        Write-Host "   git add -A && git commit -m 'Add view tracking badges to READMEs' && git push`n" -ForegroundColor White
    }

} else {
    # ── DISPLAY MODE: Show copy-paste markdown ──
    Write-Host "📋 Copy-paste these lines at the TOP of each README.md:`n" -ForegroundColor Cyan

    foreach ($folder in $foldersWithReadme) {
        $displayPath = if ($folder -eq ".") { "README.md (root)" } else { "$folder/README.md" }
        $trackingUrl = if ($folder -eq ".") {
            "$RepoUrl"
        } else {
            "$RepoUrl/tree/main/$folder"
        }

        Write-Host "  ── $displayPath ──" -ForegroundColor White
        Write-Host ""
        Write-Host "  Visible badge (shows count):" -ForegroundColor DarkGray
        Write-Host "  $BadgeMarker" -ForegroundColor Green
        Write-Host "  [![Views](https://hits.sh/$trackingUrl.svg?label=views&color=0078D4)](https://hits.sh/$trackingUrl/)" -ForegroundColor Green
        Write-Host ""
        Write-Host "  Hidden badge (transparent, stealth tracking):" -ForegroundColor DarkGray
        Write-Host "  $BadgeMarker" -ForegroundColor Yellow
        Write-Host "  ![](https://hits.sh/$trackingUrl.svg?view=today-total&style=flat-square&label=&color=ffffff&labelColor=ffffff)" -ForegroundColor Yellow
        Write-Host "`n"
    }
}

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host "  ℹ️  Badges are powered by hits.sh — free, no signup needed." -ForegroundColor DarkGray
Write-Host "  ℹ️  View your dashboard: https://hits.sh/github.com/$Owner/$Repo/" -ForegroundColor DarkGray
Write-Host "  ℹ️  Re-run this script anytime to pick up new folders.`n" -ForegroundColor DarkGray
