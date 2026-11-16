<#
Install the x-skills pack for any agent that reads Agent Skills (SKILL.md).

  .\install.ps1                  # ~/.agents/skills and ~/.claude/skills
  .\install.ps1 -Target agents   # Codex, Gemini CLI, GitHub Copilot
  .\install.ps1 -Target claude   # Claude Code, Cursor, GitHub Copilot
  .\install.ps1 -Target C:\path  # any other skills folder
  .\install.ps1 -Uninstall       # remove what this script installed
  .\install.ps1 -Force           # also replace x-* skills it didn't install

It only replaces a skill folder that it installed before (marked with a
.x-skills file), so your own skills with the same name are left alone.
#>
param(
  [string]$Target = "all",
  [switch]$Uninstall,
  [switch]$Force
)
$ErrorActionPreference = "Stop"

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Src = Join-Path $Here "skills"
$Version = (Get-Content (Join-Path $Here ".claude-plugin\plugin.json") -Raw | ConvertFrom-Json).version
$UserHome = if ($env:USERPROFILE) { $env:USERPROFILE } else { [Environment]::GetFolderPath("UserProfile") }

switch ($Target) {
  "all"    { $Dirs = @((Join-Path $UserHome ".agents\skills"), (Join-Path $UserHome ".claude\skills")) }
  "agents" { $Dirs = @((Join-Path $UserHome ".agents\skills")) }
  "claude" { $Dirs = @((Join-Path $UserHome ".claude\skills")) }
  default  { $Dirs = @($Target) }
}

$count = 0
$skipped = 0
foreach ($dir in $Dirs) {
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  foreach ($skill in Get-ChildItem -Directory $Src) {
    $dest = Join-Path $dir $skill.Name
    $marker = Join-Path $dest ".x-skills"
    if ($Uninstall) {
      if (Test-Path $marker) { Remove-Item -Recurse -Force $dest; $count++ }
      continue
    }
    if ((Test-Path $dest) -and -not (Test-Path $marker) -and -not $Force) {
      Write-Output "skip  $dest (not installed by x-skills; use -Force to replace)"
      $skipped++
      continue
    }
    if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
    Copy-Item -Recurse $skill.FullName $dest
    Set-Content -Path $marker -Value "x-skills $Version" -Encoding ascii
    $count++
  }
  if ($Uninstall) { Write-Output "removed -> $dir" } else { Write-Output "installed -> $dir" }
}

if ($Uninstall) {
  Write-Output "Removed $count skill folders. Your ~/.x-skills/ files were kept."
  exit 0
}

# The voice file every skill reads. Never overwrite one that exists.
$XHome = Join-Path $UserHome ".x-skills"
New-Item -ItemType Directory -Force -Path (Join-Path $XHome "drafts") | Out-Null
$Voice = Join-Path $XHome "voice.md"
if (-not (Test-Path $Voice)) {
  Copy-Item (Join-Path $Src "x-post\assets\voice-template.md") $Voice
  Write-Output "created ~/.x-skills/voice.md (fill it in, or let x-post ask you)"
}

if (-not (Get-Command python3 -ErrorAction SilentlyContinue) -and -not (Get-Command python -ErrorAction SilentlyContinue)) {
  Write-Output "note: Python 3.8+ is needed for the x-human checker (scripts/xcheck.py)."
}
Write-Output "Done: $count skill folders installed, $skipped skipped."
