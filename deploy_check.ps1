#!/usr/bin/env pwsh
# OpenFunds Deployment Check

Write-Host ""
Write-Host "OpenFunds Deployment Preparation" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check required files
Write-Host "Checking deployment files..." -ForegroundColor Yellow
Write-Host ""

$files = @(
    "app.py",
    "requirements.txt",
    ".streamlit/config.toml",
    "packages.txt",
    ".gitignore",
    "models/fast_similarity.py",
    "models/fast_predictor.py"
)

$allGood = $true
foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "  OK: $file" -ForegroundColor Green
    } else {
        Write-Host "  MISSING: $file" -ForegroundColor Red
        $allGood = $false
    }
}

Write-Host ""

if (-not $allGood) {
    Write-Host "Some required files are missing!" -ForegroundColor Red
    exit 1
}

Write-Host "All required files present!" -ForegroundColor Green
Write-Host ""

# Check git status
Write-Host "Checking git status..." -ForegroundColor Yellow
Write-Host ""

$gitStatus = git status --porcelain 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "Not a git repository or git not installed" -ForegroundColor Yellow
} elseif ([string]::IsNullOrWhiteSpace($gitStatus)) {
    Write-Host "All changes committed!" -ForegroundColor Green
} else {
    Write-Host "Uncommitted changes found:" -ForegroundColor Yellow
    Write-Host $gitStatus -ForegroundColor Gray
    Write-Host ""
    Write-Host "Run these commands to commit:" -ForegroundColor Cyan
    Write-Host "   git add ." -ForegroundColor White
    Write-Host "   git commit -m Production-ready" -ForegroundColor White
    Write-Host "   git push origin main" -ForegroundColor White
    Write-Host ""
}

# Deployment instructions
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "DEPLOYMENT INSTRUCTIONS" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your app is ready to deploy to Streamlit Cloud (FREE)!" -ForegroundColor White
Write-Host ""
Write-Host "Step 1: Ensure code is pushed to GitHub" -ForegroundColor Yellow
Write-Host "   Repository: https://github.com/abhishekbiradar07/Openfunds.v2" -ForegroundColor Gray
Write-Host ""
Write-Host "Step 2: Go to Streamlit Cloud" -ForegroundColor Yellow
Write-Host "   Visit: https://share.streamlit.io/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Step 3: Sign in with GitHub" -ForegroundColor Yellow
Write-Host "   Click Continue with GitHub and authorize" -ForegroundColor Gray
Write-Host ""
Write-Host "Step 4: Deploy New App" -ForegroundColor Yellow
Write-Host "   Click New app button and fill in:" -ForegroundColor Gray
Write-Host "   - Repository: abhishekbiradar07/Openfunds.v2" -ForegroundColor White
Write-Host "   - Branch: main" -ForegroundColor White
Write-Host "   - Main file: app.py" -ForegroundColor White
Write-Host "   - App URL: openfunds-v2" -ForegroundColor White
Write-Host ""
Write-Host "Step 5: Click Deploy button" -ForegroundColor Yellow
Write-Host "   Wait 2-5 minutes for deployment" -ForegroundColor Gray
Write-Host ""
Write-Host "Step 6: Your app will be live at:" -ForegroundColor Yellow
Write-Host "   https://openfunds-v2.streamlit.app" -ForegroundColor Cyan
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "FEATURES INCLUDED:" -ForegroundColor Green
Write-Host "   - Similar Campaigns Detection (1.5ms)" -ForegroundColor White
Write-Host "   - AI Success Prediction (<1ms)" -ForegroundColor White
Write-Host "   - Personalized Feedback" -ForegroundColor White
Write-Host "   - Color-coded Scores" -ForegroundColor White
Write-Host "   - Professional UI/UX" -ForegroundColor White
Write-Host ""
Write-Host "Documentation:" -ForegroundColor Yellow
Write-Host "   - DEPLOYMENT_GUIDE.md - Complete guide" -ForegroundColor Gray
Write-Host "   - README_AI_FEATURES.md - AI features docs" -ForegroundColor Gray
Write-Host ""
Write-Host "Ready to deploy!" -ForegroundColor Green
Write-Host ""
