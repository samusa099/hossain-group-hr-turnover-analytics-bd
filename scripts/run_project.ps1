$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
if (Get-Command py -ErrorAction SilentlyContinue) {
    py .\generate_powerbi_project.py
} else {
    python .\generate_powerbi_project.py
}
Start-Process (Join-Path $PSScriptRoot "..\powerbi\Hossain_Group_Turnover.pbip")
