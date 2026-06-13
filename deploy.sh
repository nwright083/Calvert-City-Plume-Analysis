#!/bin/bash
# ==============================================================================
# deploy.sh - Auto-deploy Calvert City Plume simulation to GitHub Pages
# ==============================================================================
# This script automates publishing the generated index.html to the GitHub Pages
# repository (nwright083/Calvert-City-Plume-Analysis).
# ==============================================================================

# Exit immediately if any command fails
set -e

# Target GitHub Pages repository URL
PAGES_REPO="https://github.com/nwright083/Calvert-City-Plume-Analysis.git"
TEMP_DIR="pages_deploy_temp"

echo "=== Starting deployment to GitHub Pages ==="

# Clean up any leftover temp folder
if [ -d "$TEMP_DIR" ]; then
    echo "Cleaning up old temporary directories..."
    rm -rf "$TEMP_DIR"
fi

# 1. Clone only the latest commit to keep it extremely fast
echo "Cloning Pages repository..."
git clone --depth 1 "$PAGES_REPO" "$TEMP_DIR"

# 2. Verify local index.html exists
if [ ! -f "index.html" ]; then
    echo "Error: index.html not found in current directory. Please run the simulation first."
    rm -rf "$TEMP_DIR"
    exit 1
fi

# 3. Copy the generated index.html to the cloned repo
echo "Copying latest index.html to deployment folder..."
cp index.html "$TEMP_DIR/index.html"

# 4. Commit and push changes
cd "$TEMP_DIR"

# Check if there are actual changes to commit
if git diff --quiet index.html; then
    echo "No new changes detected in index.html. Deployment skipped."
else
    echo "Committing updates..."
    git add index.html
    git commit -m "Auto-deploy simulation update: $(date '+%Y-%m-%d %H:%M:%S')"
    
    echo "Pushing updates to GitHub..."
    git push origin main
    echo "=== Deployment successful! ==="
fi

# 5. Clean up temporary directory
cd ..
rm -rf "$TEMP_DIR"
echo "Tidied up temporary files."
