$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)

$python = if (Test-Path ".\.venv\Scripts\python.exe") {
    ".\.venv\Scripts\python.exe"
} else {
    "python"
}

Write-Host "Running compile check..."
& $python -m compileall -q app main.py tests

Write-Host "Running unit tests..."
& $python -m unittest discover -s tests -v

Write-Host "All checks passed."