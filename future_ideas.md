# Calvert City Plume Dispersion - Future Ideas & Roadmap

This document serves as a living roadmap of future ideas, improvements, and bug fixes for the Calvert City Plume Dispersion simulation project. These tasks are organized by category and rated by relative implementation difficulty.

---
# sync test - verified pipeline functionality

## 1. Quick Fixes & UI Enhancements

### 🟢 Fix Industrial Point Sources Dropdown Scrolling (Bug)
* **Status**: 🔴 Not Implemented (Bug)
* **Difficulty**: Easy
* **Description**: Currently, scrolling within the "Industrial Point Sources" legend panel is unresponsive or intercepts the map zoom.
* **Proposed Solution**: 
  * In `index.html`, Leaflet intercepts mousewheel and click events on panel overlays. We need to disable event propagation to the map container by invoking Leaflet's `L.DomEvent.disableScrollPropagation(element)` and `L.DomEvent.disableClickPropagation(element)` on the legend and control panels.
  * Verify that `.facility-list` has proper max-height or height constraints so that `overflow-y: auto` triggers correctly.

### 🟢 Fix Particle Density Scaling Bug
* **Status**: 🔴 Pending Fix (Bug Identified)
* **Difficulty**: Easy
* **Description**: The particle count scaling for different facilities evaluates to the floor of 10 particles/hour because of a key mismatch (`"lbs_year"` vs `"total_lbs"`) in `write_setup_file()`.
* **Proposed Solution**:
  * Update `write_setup_file()` in `calvert_plume_engine.py` to use `"total_lbs"` instead of `"lbs_year"` when summing facility emissions.

---

## 2. Coordinates & Data Accuracy

### 🟢 Verify and Correct Geolocation Coordinates for All Facilities
* **Status**: 🟡 Partially Implemented
* **Difficulty**: Easy to Medium
* **Description**: Coordinates in the simulation do not align perfectly with real-world structures on Google satellite view.
* **Proposed Solution**:
  * Cross-reference each facility's address/name on Google Maps to find the exact coordinates of key stacks or fugitive release boundaries.
  * Update the coordinates in the `FACILITIES` dictionary in `calvert_plume_engine.py` (and coordinate harvesting rules) to ensure plumes originate from the correct gate or stack location.

### 🟢 Plume Emission Data Cleaning & Filtering
* **Status**: 🟡 Partially Implemented
* **Difficulty**: Easy
* **Description**: Some chemical numbers look abnormally high (e.g. Methanol at 700,000 lbs/year) which could indicate we are showing total waste managed or process totals instead of strictly fugitive/stack air emissions.
* **Proposed Solution**:
  * Review `calvert_plume_engine.py` parsing function `parse_tri_csv()` to ensure it strictly extracts columns `"5.1 - fugitive air"` and `"5.2 - stack air"` from the TRI CSV and doesn't accidentally pull total release quantities.
  * Implement an automatic filter/threshold system to exclude non-air releases or warn users of anomalous spikes in the dataset.

---

## 3. Advanced Simulation & Physics

### 🟡 Set Facility Operating / Working Schedules
* **Status**: 🔴 Not Implemented
* **Difficulty**: Medium
* **Description**: Stacks are currently assumed to release emissions at a constant rate 24/7 (annual emissions / 8760 hours). Real facilities have specific operating shifts or batch cycles.
* **Proposed Solution**:
  * Add a scheduling configuration parameter to each facility in `calvert_plume_engine.py`.
  * Modify the HYSPLIT `CONTROL` file emission hours and rates generator to emit only during specified working hours (e.g., Monday–Friday, 8:00 AM – 5:00 PM), dividing annual emissions by the active working hours instead of the entire year.

### 🟡 Stagnant Wind / Wind Speed Sensitivity Tuning
* **Status**: 🔴 Not Implemented
* **Difficulty**: Medium
* **Description**: Plumes in Calvert City sometimes pool or stay stagnant compared to other models (like Pittsburgh), suggesting we may need to adjust wind speed sensitivity or turbulence settings.
* **Proposed Solution**:
  * Investigate HYSPLIT grid dispersion parameter tuning (e.g., tweaking boundary layer turbulence parameterization).
  * Look into scaling wind speeds or modeling finer-resolution microclimates if the HRRR model consistently underestimates local river-valley wind speeds.

### 🔴 Minute-level HYSPLIT Dispersion Data
* **Status**: 🔴 Not Implemented
* **Difficulty**: Hard
* **Description**: Currently, particles are dumped hourly. Having sub-hourly or minute-level particle updates would make the simulation visual flow much smoother.
* **Proposed Solution**:
  * Adjust HYSPLIT's `SETUP.cfg` and `CONTROL` configurations to dump particle positions at shorter intervals (e.g., every 5 or 10 minutes).
  * Determine if HRRR meteorological data can be interpolated by HYSPLIT to support smooth sub-hourly calculations.

### 🟡 Model Plume Rise & Buoyant Stacks
* **Status**: 🔴 Not Implemented
* **Difficulty**: Medium
* **Description**: Emissions currently release at a fixed height of 15m. Real industrial stacks emit gases with thermal and momentum buoyancy, which rises above the physical stack top.
* **Proposed Solution**:
  * Modify the `CONTROL` file generator to accept and output stack properties (diameter, exit temperature, exit velocity) for each facility.
  * Configure HYSPLIT's internal plume rise algorithms to dynamically compute buoyancy and momentum plumes.

### 🟡 Split Stack vs. Fugitive Emissions
* **Status**: 🔴 Not Implemented
* **Difficulty**: Medium
* **Description**: Facilities combine fugitive (ground-level) and stack (elevated) emissions into a single 15m release.
* **Proposed Solution**:
  * Parse fugitive and stack emissions separately from the TRI CSV.
  * Model elevated stack releases as point sources and ground-level fugitive leaks as area sources in the HYSPLIT run configurations.

### 🔴 Chemical-Specific Particle Deposition (Dry/Wet Scavenging)
* **Status**: 🔴 Not Implemented
* **Difficulty**: Hard
* **Description**: Currently, all emissions are simulated as a non-depositing tracer gas. Heavy molecules like ethylene dichloride (which is heavier than air) or water-soluble gases drop out of the plume via gravitational settling, dry deposition, or rain washout, polluting the ground and water.
* **Proposed Solution**:
  * Define specific dry deposition velocities, molecular weight, and wet scavenging coefficients (Henry's Law constants, below-cloud washout ratio) for target chemical species in the `CONTROL` file.
  * Enable gravity settling for heavier particulates and gas-phase dry/wet deposition parameters inside the HYSPLIT physics configurations.

### 🔴 Soil & Water Accumulation Heatmaps (Deposition Mapping)
* **Status**: 🔴 Not Implemented
* **Difficulty**: Hard
* **Description**: Trace deposition over multiple days to show where chemicals build up in the local environment, particularly identifying whether nearby water bodies (like the Tennessee/Ohio River) or sensitive land areas are receiving high deposition loads.
* **Proposed Solution**:
  * Configure HYSPLIT to output deposition grids (`cdump` file with deposition concentration).
  * Parse the deposition grid outputs in the Python engine and compile cumulative deposit grids.
  * Render an interactive Leaflet heatmap overlay in the HTML dashboard representing cumulative pollutant accumulation over the course of the simulation.

---

## 4. Air Monitors & Smell Reports

### 🟡 Add Smell Report Data Overlays
* **Status**: 🔴 Not Implemented
* **Difficulty**: Medium
* **Description**: Overlay crowd-sourced odor/smell reports on the map visualization to see if simulated plumes align with real-world complaints.
* **Proposed Solution**:
  * Design a parser to ingest smell report CSVs (containing timestamp, latitude, longitude, odor description, and intensity).
  * Add a new map layer in `index.html` displaying these smell reports as interactive icons that fade in and out according to their timestamp.

### 🔴 Visualize Air Quality Monitor Emissions & Reverse-Dispersion
* **Status**: 🔴 Not Implemented
* **Difficulty**: Hard
* **Description**: Add the air quality monitoring dataset from 2025. Simulate particles emitting from the monitor locations themselves to represent measured concentrations or back-trace odor plumes.
* **Proposed Solution**:
  * Ingest the 2025 air monitoring data and render monitor locations on the map.
  * For dates with high monitored concentrations, emit tracer particles from the monitors to visually map the zone of influence, or run reverse-HYSPLIT trajectories to find candidate industrial sources.

---

## 5. System Accessibility & Usability

### 🟡 Change Dates Dynamically in the HTML (Year-long Archive)
* **Status**: 🟡 Partially Implemented
* **Difficulty**: Medium
* **Description**: Currently, `index.html` only supports pre-baked simulation dates (currently March 8–14, 2025). The user wants to change dates to any day in a full year.
* **Proposed Solution**:
  * Run the python plume simulation engine for an entire year to generate a compressed historical JSON archive.
  * Update the HTML date picker to fetch/load these daily data fragments dynamically (e.g. via separate lightweight daily JSON files loaded via AJAX/fetch) to avoid bloated file sizes.

### 🔴 Self-contained Web GUI Application (HYSPLIT-as-a-Service)
* **Status**: 🔴 Not Implemented
* **Difficulty**: Hard
* **Description**: Build a user-friendly app where anyone can download HYSPLIT, input coordinates, upload custom TRI data, customize simulation variables (particle size, density, opacity), and run the simulation automatically.
* **Proposed Solution**:
  * Create a desktop or local web application (e.g. using Electron, Streamlit, or React/Node) that handles downloading/packaging HYSPLIT executables.
  * Build a clean GUI interface to manage all simulation settings, run the underlying python commands, and output the visualization file.
