@echo off
REM Quick Network Test Script for Quantum Secure Chat

echo ========================================
echo Quantum Secure Chat - Network Test
echo ========================================
echo.

REM Test if backend is running
echo Testing backend connection...
curl -s -o nul -w "Backend Status: %%{http_code}\n" http://192.168.29.109:8000/
echo.

REM Get the local PC IP
echo Your Local PC IP Address:
for /f "tokens=4" %%a in ('route print ^| find "0.0.0.0"') do echo %%a
echo.

REM Show how to access locally
echo ========================================
echo LOCAL ACCESS (same network):
echo - Backend API: http://192.168.29.109:8000/api
echo - Frontend Web: http://localhost:8080
echo.

REM Instructions
echo ========================================
echo NEXT STEPS FOR GLOBAL DEPLOYMENT:
echo.
echo 1. Read: GLOBAL_DEPLOYMENT_GUIDE.md
echo.
echo 2. Option A - EASIEST (No Git Required):
echo    - Drag frontend/build/web folder to https://netlify.com
echo    - Deploy backend to https://render.com
echo    - Update BACKEND_URL in api_service.dart
echo.
echo 3. Option B - Using GitHub (More Professional):
echo    - Create GitHub repo
echo    - Deploy frontend to https://vercel.com
echo    - Deploy backend to https://render.com
echo.
echo ========================================
pause
