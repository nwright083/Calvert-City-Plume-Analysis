#!/bin/bash

# Stop the script immediately if any command fails
set -e

echo "🚀 Starting automated sync pipeline..."

# ----------------------------------------------------
# STEP 1: Sync EVERYTHING (Data + Code) to Gitea (origin)
# ----------------------------------------------------
echo "📦 Staging all changes on main..."
git add .

# Check if there are actually changes to commit on main so the script doesn't exit with error
if ! git diff-index --quiet HEAD --; then
    echo "💾 Committing data and code updates on main..."
    git commit -m "Automated backup: data and code updates"
else
    echo "✅ No new changes to commit on main."
fi

echo "🏠 Pushing everything to Gitea home server..."
git push origin main

# ----------------------------------------------------
# STEP 2: Sync ONLY Code to GitHub Pages (github)
# ----------------------------------------------------
echo "🌐 Updating web-deploy branch in worktree..."

# Ensure we copy the files into the worktree directory
cp calvert_plume_engine.py web-deploy-worktree/
cp calvert_plume_engine_one_day.py web-deploy-worktree/
cp fetch_aqs_data.py web-deploy-worktree/
cp api2arl.cfg web-deploy-worktree/
cp future_ideas.md web-deploy-worktree/
cp README.md web-deploy-worktree/
cp index.html web-deploy-worktree/

# Switch context to the worktree
cd web-deploy-worktree

echo "📝 Staging changes in web-deploy-worktree..."
git add .

# Commit the updated scripts on the web branch
if ! git diff-index --quiet HEAD --; then
    echo "💾 Committing clean scripts for web deployment..."
    git commit -m "Automated deploy: updating public scripts"
else
    echo "✅ No web script changes detected."
fi

echo "🚀 Pushing clean codebase to GitHub..."
git push github web-deploy:main

# Go back to the main repository root
cd ..

echo "🎉 All done! Gitea and GitHub are perfectly synced."