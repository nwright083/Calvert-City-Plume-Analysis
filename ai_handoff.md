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
- **HYSPLIT Mode**: Animates particles along interpolated paths using downsampled HYSPLIT trajectory data compiled by Python. 
  - **Performance Optimization**: Bypasses client-side wind advection, particle spawning, and initial page-load sandbox deposition recalculations. This reduces CPU load from 100% to near-idle, resolving computer overheating/fan noise.
- **Sandbox Mode** (Default): Runs a client-side real-time animation loop advecting particles from industrial point sources across a **20×20 wind grid** (up from 10×10) using bilinear interpolation. Each grid cell now also carries **IQR-based spread values (`sLat`/`sLon`)** derived from actual HYSPLIT particle statistics. The sandbox uses these to fan particles out to match the real HYSPLIT dispersion footprint, rather than just following the median wind vector.

### 3. Wind Field Data Contract
The Python `build_wind_grid_for_filter()` function now exports per-cell `{"dLat", "dLon", "sLat", "sLon"}` where `sLat`/`sLon` is the IQR half-range of particle displacements in that cell-hour. The JS `interpolateGrid()` bilinearly interpolates all four values. In `advect()` and `recalculateDeposition()`, spread drives fan-out: `spreadLat = max(ageTurb, sLat * SPREAD_KICK)`, ensuring the streaming particles fill the same geographic footprint as the HYSPLIT deposition heatmap.

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

### Heatmap Accumulation & Normalization Fix (June 23, 2026 — Antigravity/Gemini)
1. **Time-progressive gamma normalization**: Added `DEP_GAMMA = 0.5` constant. Replaced the sandbox rendering path in `renderDepositionHeatmap()` to use `Math.pow(rel, DEP_GAMMA) * timeProgress` where `timeProgress = Math.min(1.0, playbackTime / 24.0)`. This lifts faint, distant cell intensities so the broad plume extent stays visible over time instead of shrinking to a blob near the source.
2. **Live Tooltip Queries**: Fixed the mouse-move tooltip else-branch to branch based on `particleSource`. If not in HYSPLIT mode, it queries `liveDepGrid` directly using the 0.002-degree cell grid keys and computes intensity using the progressive gamma formula. If in HYSPLIT mode, it falls back to the static reference grid from `PLUME_DATA.deposition_grid`.
3. **Both engines kept in sync**: All changes applied identically to `calvert_plume_engine.py` and `calvert_plume_engine_one_day.py`.

### Unified Physics-Coupled Deposition Model (June 23, 2026 — Claude Sonnet Round 3)
1. **Mass-based emergent lifespan**: Each sandbox particle now carries `mass: 1.0` at birth. Near-surface particles (ht < 30m) lose mass each tick via `fraction = min(0.15, vd * dtSec / 30.0)`, where `vd` comes from the chemical's entry in `PLUME_DATA.chemical_properties`. Particles vanish when `mass ≤ DEP_MASS_FLOOR = 0.05`. A `SAFETY_MAX_AGE = 720` min backstop prevents calm-air particles from accumulating forever. The "Particle Lifespan" slider is removed — lifespan is now fully physics-driven by chemistry and met.
2. **Live deposition accumulator**: Deposited mass is written to `liveDepGrid` (a `Map<cellKey, mass>`) in `advect()`. `renderDepositionHeatmap()` reads `liveDepGrid` directly when in sandbox mode, growing the heatmap in real time as particles deposit — the heatmap is now the running sum of exactly where visible dots have deposited. Resets on day rollover, restart, and source switch.
3. **Particle fade by mass**: In `drawParticles()`, sandbox particle `ageFade = (p.mass - DEP_MASS_FLOOR) / (1 - DEP_MASS_FLOOR)` — particles fade naturally as they deposit rather than fading uniformly over a timer.
4. **Default = live deposition**: Boot sequence no longer precomputes or switches to the HYSPLIT grid. The dropdown options are relabeled: "Live Deposition (Physics)" (default) and "HYSPLIT Residence Footprint (Reference)". Switching back to sandbox resets the live accumulator instead of running the heavy batch precompute.
5. **Both engines kept in sync**: All changes applied identically to `calvert_plume_engine.py` and `calvert_plume_engine_one_day.py`.
6. **Tuning knobs** (in-line, not user-facing): `DEP_MASS_FLOOR`, `SAFETY_MAX_AGE`, and the `fraction` cap (`0.15`) in `advect()`.

### Particle Lifespan, Pan-Tether & Lag Fixes (June 23, 2026 — Claude Sonnet Round 2)
1. **Particle Lifespan Decoupled**: Added `SANDBOX_LIFESPAN_MINUTES = 360` constant (separate from HYSPLIT's `MAX_PARTICLE_AGE_MINUTES = 120` / khmax). Sandbox particles now live 6 hours by default so plumes stay visible over the full day envelope, matching the HYSPLIT deposition footprint. Lifespan slider widened from 30–240 min to 60–1440 min. Spawn rate inversely scaled by `lifespanScale = 120 / getSandboxLifespan()` so particle budget (and frame cost) stays flat regardless of lifespan setting.
2. **Deposition Heatmap Pan-Tether Fix**: Added `map.on('move', ...)` handler that calls `depositionHeatLayer._reset()` on every move tick, mirroring the particle canvas behavior. The heatmap now stays locked to the basemap during pan instead of snapping back on `moveend`.
3. **Late-Day Lag Fix**: Replaced the sim-time throttle (`0.1 sim-hours`) with a real-time throttle (`120ms` via `performance.now() - lastDepRenderMs`). At 60 Hours/Min the old throttle triggered ~10 heatmap rebuilds/sec late in the day; the new throttle caps it at ~8 rebuilds/sec regardless of playback speed.
4. **Both engines kept in sync**: All changes applied identically to `calvert_plume_engine.py` and `calvert_plume_engine_one_day.py`.

### Sandbox Coverage Alignment + Triangulation Fix (June 23, 2026 — Claude Sonnet Round 1)
1. **Triangulation Bug Fixed**: Canvas particle batching was connecting arc start points with straight lines before filling, creating large facility-colored triangles across the map. Fixed by adding `ctx.moveTo(x + r, y)` before each `ctx.arc()` call in both the fill pass and glow-halo pass of `drawParticles()`.
2. **Wind Grid Enriched with HYSPLIT Spread**:
   - Python `build_wind_grid_for_filter()` now exports `sLat`/`sLon` (IQR half-range of per-cell particle displacements) alongside `dLat`/`dLon` in every grid cell. IDW interpolation for unpopulated cells also propagates spread.
   - `GRID_SIZE` raised from 10 to 20 for finer spatial resolution.
   - JS `interpolateGrid()` bilinearly interpolates `sLat`/`sLon`.
   - JS `getWind()` blends and returns spread alongside median displacement.
   - `MAX_WIND_PER_HR` raised from 0.10° to 0.18° to allow real HYSPLIT transport distances.
   - `advect()` and `recalculateDeposition()` now use `spreadLat = max(ageTurb, sLat * 1.2)` so sandbox particles fan out to match the HYSPLIT deposition footprint while still streaming from point sources.
3. **Global Particles Toggle**: Added "💨 Show Particles" checkbox to the control panel (above the Deposition Heatmap toggle). Independently toggles particle visibility without affecting the deposition heatmap.
4. **Both engines kept in sync**: All changes applied identically to `calvert_plume_engine.py` and `calvert_plume_engine_one_day.py`.

---

## 📝 Current Task & Next Steps

### 🎯 NEXT JOB: Daily Automated Simulation & Weather Page Integration
This is the primary next job:
1. **Decouple Plume Data**: Modify [calvert_plume_engine.py](file:///Users/nawrig04/plume-analysis/calvert_plume_engine.py) to add a command-line flag for generating standalone JSON files (e.g. `data/plume-YYYY-MM-DD.json`) instead of baking data directly into [index.html](file:///Users/nawrig04/plume-analysis/index.html).
2. **Local macOS Daemon Setup**: Set up a macOS `launchd` plist to run the simulation engine automatically at night (running for the previous day's date, downloading weather via `Herbie`, running HYSPLIT), write the daily JSON file, and execute [sync.sh](file:///Users/nawrig04/plume-analysis/sync.sh) to push the updates to the GitHub repository.
3. **Weather Forecast Page Integration**: Update the Leaflet map on the main weather variable analysis forecast webpage to include a toggleable layer or tab for the plume simulation. This frontend will fetch `data/plume-YYYY-MM-DD.json` based on a date slider and overlay particles and deposition heatmaps on top of the weather map.

### 🔍 Verification Required (Current Sandbox Prototype)
- [ ] Open the regenerated `index.html` (single-day simulation) and verify that the live deposition heatmap correctly accumulates over time without disappearing or collapsing to a source blob.
- [ ] Hover over deposited areas in sandbox mode and confirm the tooltip displays live-updating mass accumulation values ($g/m^2$) matching the on-screen gradient.

### 🗺️ Other Future Improvements (From [future_ideas.md](file:///Users/nawrig04/plume-analysis/future_ideas.md))
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
