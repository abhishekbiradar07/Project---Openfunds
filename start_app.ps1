#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Start OpenFunds Streamlit app for testing AI features
.DESCRIPTION
    Launches the Streamlit application so you can test the new AI features
#>

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║          Starting OpenFunds with AI Features ✨                   ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "🔍 AI Features Included:" -ForegroundColor Green
Write-Host "  ✅ Similar Campaigns Detection (1.5ms)" -ForegroundColor Gray
Write-Host "  ✅ AI Success Prediction (<1ms)" -ForegroundColor Gray
Write-Host "  ✅ Personalized Feedback" -ForegroundColor Gray
Write-Host "  ✅ Color-coded Scores (🟢🟡🔴)" -ForegroundColor Gray
Write-Host ""

Write-Host "📋 To Test:" -ForegroundColor Yellow
Write-Host "  1. Go to 'Create Campaign' page" -ForegroundColor Gray
Write-Host "  2. Fill in campaign details" -ForegroundColor Gray
Write-Host "  3. Click 'Check for Similar Campaigns' (optional)" -ForegroundColor Gray
Write-Host "  4. Click 'Create Campaign'" -ForegroundColor Gray
Write-Host "  5. See instant AI Success Analysis! 🎉" -ForegroundColor Gray
Write-Host ""

Write-Host "🚀 Starting Streamlit..." -ForegroundColor Magenta
Write-Host ""

# Start Streamlit
streamlit run app.py

Write-Host ""
Write-Host "Application stopped." -ForegroundColor Yellow
