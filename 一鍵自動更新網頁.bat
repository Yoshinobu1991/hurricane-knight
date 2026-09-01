@echo off
cd /d "c:\Users\Admir\Desktop\Project\Hurricane Knight"
echo Adding files to git...
git add .
echo Committing changes...
git commit -m "Auto-update website"
echo Pushing to GitHub...
git push origin main
echo Done!
pause
