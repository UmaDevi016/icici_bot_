@echo off
echo ========================================
echo Preparing Code for Public Deployment
echo ========================================
echo.

echo Step 1: Adding all files to Git...
git add .

echo.
echo Step 2: Committing changes...
git commit -m "Ready for public deployment with FAQ system"

echo.
echo Step 3: Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo SUCCESS! Code pushed to GitHub
echo ========================================
echo.
echo Next steps:
echo 1. Go to https://render.com or https://railway.app
echo 2. Sign up (FREE)
echo 3. Connect your GitHub repository
echo 4. Click Deploy
echo.
echo See DEPLOY_TO_RENDER.md for detailed instructions
echo.
pause
