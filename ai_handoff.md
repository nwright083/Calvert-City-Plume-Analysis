# AI Handoff & Collaboration Guide

This document is a shared state file for **Antigravity (Gemini)**, **Claude Code**, and any other AI developers working on this project. 
Please read this file at the start of your session to get up to speed, and update it at the end of your session with your latest changes and the next steps.

---

## 🎯 Project Overview & Mission
The **Calvert City Plume Analysis Sandbox** is an interactive web-based visualization dashboard and backend simulation pipeline modeling atmospheric chemical dispersion from industrial point sources in Calvert City, Kentucky.

- **Objective**: Provide a highly accurate, performant, and visual representation of chemical plume trajectories and soil/water deposition accumulation.
- **Key Feature**: Combines a physical model (HYSPLIT trajectories run offline) with a client-side real-time interactive sandbox.

---

## 📂 Repository Architecture & Deployment

### Git Worktree Setup (CRITICAL)
To avoid git checkout conflicts and prevent downloading/deleting gigabytes of meteorology and air monitor data files:
1. **Root Directory (`/`)**: Main workspace checked out to the `main` branch. This contains all raw data (`.ARL` met files, raw monitoring CSVs) and code. Pushes to the local **Gitea** home server.
2. **`web-deploy-worktree/`**: Git worktree checked out to the `web-deploy` branch. Pushes to **GitHub** for GitHub Pages.
3. **Sync Pipeline**: **ALWAYS use `./sync.sh`** to commit and deploy changes. This script automatically syncs Gitea and copies clean code + `index.html` to the worktree to push to GitHub.

### Main Scripts
- [calvert_plume_engine.py](file:///Users/nawrig04/plume-analysis/calvert_plume_engine.py): The main Python simulation script. Generates the final self-contained [index.html](file:///Users/nawrig04/plume-analysis/index.html) by embedding simulation and deposition data.
- [calvert_plume_engine_one_day.py](file:///Users/nawrig04/plume-analysis/calvert_plume_engine_one_day.py): A helper script for running a single-day test/development simulation.
- [sync.sh](file:///Users/nawrig04/plume-analysis/sync.sh): Automated commit, synchronization, and deployment script.

---

## ⚙️ Technical Architecture & Key Systems

### 1. HYSPLIT Dispersion & Deposition Calculation (Python)
- Due to a Mac-specific HYSPLIT concentration grid calculation crash (SIGFPE), the engine runs HYSPLIT in stable **particle-only mode** and performs offline binning of particles in Python.
- During post-processing, low-level particles (height $\le$ 100m) are binned into 0.02-degree grid cells.
- Surface deposition mass is accumulated by weighting each particle's contribution by its parent facility's chemical emissions and deposition velocities ($V_d$), with linear height-based scaling.
- The chemical properties database (molecular weight, fixed deposition velocity $V_d$, reactivity, and Henry's Law solubility constant $H$) is used to weight the deposition.

### 2. Dual-Mode Particle Visualization (JavaScript)
The frontend ([index.html](file:///Users/nawrig04/plume-analysis/index.html)) supports two particle rendering sources:
- **HYSPLIT Mode** (Default when data is present): Animates particles along interpolated paths using downsampled HYSPLIT trajectory data compiled by Python. 
  - **Performance Optimization**: Bypasses client-side wind advection, particle spawning, and initial page-load sandbox deposition recalculations. This reduces CPU load from 100% to near-idle, resolving computer overheating/fan noise.
- **Sandbox Mode**: Runs a client-side real-time animation loop advecting particles across a coarse 10x10 wind grid using bilinear interpolation.

---

## 📈 Recent Implementations (Last updated: June 23, 2026)

### HYSPLIT Particle Alignment & Fan Performance Fixes
1. **Python Engine Data Export**:
   - Modified `parse_gis_file_by_hour()` to parse `PTYP` and map chemical names to individual particles.
   - Implemented deterministic downsampling of particle trajectories and exported them as a timeline under the `"particles"` key in the output JSON.
2. **Frontend Interpolation Engine**:
   - Added `updateHysplitParticles(playbackTime)` to interpolate particle coordinates (lat, lon, height, age) linearly between hourly HYSPLIT dumps.
   - Modified `tick()` to skip spawning, advecting, and client-side wind calculation in HYSPLIT mode.
   - Bypassed heavy `recalculateDeposition()` during initial page boot when HYSPLIT deposition grid is available.
   - Integrated visibility/chemical checkboxes to filter HYSPLIT particles instantly.
   - Updated map tooltip to query HYSPLIT particle attributes (chemical name, release type, height, age) in HYSPLIT mode.
3. **Synchronization**:
   - Ensured changes are mirrored in both `calvert_plume_engine.py` and `calvert_plume_engine_one_day.py`.

---

## 📝 Current Task & Next Steps

### 🔍 Immediate Verification Required
- [ ] Open the regenerated `index.html` in a web browser to verify that the flying particles match the deposition heatmap perfectly.
- [ ] Verify that CPU usage stays low and fans do not run hot during playback.

### 🗺️ Future Improvements (From [future_ideas.md](file:///Users/nawrig04/plume-analysis/future_ideas.md))
- Fix the **Industrial Point Sources legend dropdown scrolling** (needs Leaflet click/scroll propagation disabled).
- Fix the **Particle Density Scaling** bug (summing emissions uses `"lbs_year"` instead of `"total_lbs"` in `write_setup_file()`).
- Verify and correct geolocation coordinates for facilities using satellite imagery.
- Add crowd-sourced smell report overlays.

---

## 🤖 Guide for AI Developers (How to Handoff)
1. **Always read this file first** to understand what the current focus is.
2. **Read [future_ideas.md](file:///Users/nawrig04/plume-analysis/future_ideas.md)** for detailed feature descriptions and bugs.
3. **When you complete a task**:
   - Update this file's **Recent Implementations** section with what you did.
   - Update the **Current Task & Next Steps** section.
4. **Deploy changes**:
   - Add any new files (such as this handoff file) to `sync.sh` if they should be copied to the `web-deploy-worktree`.
   - Run `./sync.sh` to ensure both Gitea and GitHub repositories are fully updated before finishing your session.
