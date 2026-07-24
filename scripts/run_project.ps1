$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$env:HOSSAIN_GROUP_DATA_ROOT = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
if (Get-Command py -ErrorAction SilentlyContinue) {
    py .\generate_powerbi_project.py
} else {
    python .\generate_powerbi_project.py
}
Start-Process (Join-Path $PSScriptRoot "..\powerbi\Hossain_Group_Turnover.pbip")
