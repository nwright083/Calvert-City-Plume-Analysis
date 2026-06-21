# Calvert City Plume Analysis Sandbox

This repository contains the HYSPLIT dispersion modeling engine and web visualization dashboard for the Calvert City chemical facility emissions.

---

## 🚀 Syncing and Deployment (CRITICAL)

To prevent git checkout conflicts and avoid deleting/re-downloading gigabytes of meteorology and monitor CSV files, this repository uses a **Git Worktree** structure.

**Whenever you need to push or sync changes, ALWAYS run the automated sync script. Do NOT switch branches or run manual git pushes.**

```bash
./sync.sh
```

### Repository Architecture:
1. **Root Directory (`/`)**: Stays permanently checked out to the `main` branch. This contains all code, scripts, and the large CSV datasets. Pushes everything to your **Gitea** home server.
2. **`web-deploy-worktree/`**: A Git worktree subdirectory checked out to the `web-deploy` branch. The sync script automatically copies clean code and the regenerated `index.html` here and pushes it to **GitHub** for GitHub Pages. This folder is ignored in the `main` branch's `.gitignore`.
