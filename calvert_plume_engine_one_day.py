# ==============================================================================
# GLOBAL CONFIGURATION COMPONENT (CALVERT CITY PLUME SANDBOX)
# ==============================================================================
# --- MULTI-DATE BATCH PROCESSING CONTROLS ---
START_DATE = "2025-03-08"  # YYYY-MM-DD format for batch week initialization
END_DATE = "2025-03-08"    # Consecutive 7-day simulation window end date
WEATHER_CACHE_DIR = "~/hysplit/weather_cache"  # Persistent directory for NOAA HRRR grids
WEATHER_BOX_RADIUS_KM = 50  # Bounding box size for local weather cropping

# --- LOCAL TRI EMISSIONS DATA PATH ---
import os
_WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__)) + "/"
_DRIVE_DIR = "/Users/nawrig04/Library/CloudStorage/GoogleDrive-wrightnicholas4@gmail.com/My Drive/Med school/SRSP Project/Plume Analysis/"

# Prefer local workspace copy; fall back to Google Drive only if local is missing
_local_tri = os.path.join(_WORKSPACE_DIR, "Marshall County Facility Release.csv")
LOCAL_TRI_CSV_PATH = _local_tri if os.path.exists(_local_tri) else os.path.join(_DRIVE_DIR, "Marshall County Facility Release.csv")

# --- DEFAULT ACTIVE HIGH-PRIORITY WHITELIST ---
# Chemicals on this list default to CHECKED (active) on map load. All other chemicals default to UNCHECKED.
DEFAULT_ACTIVE_CHEMICALS = [
    "VINYL CHLORIDE", "CHLORINE", "TRICHLOROETHYLENE", "1,3-BUTADIENE",
    "HYDROGEN FLUORIDE", "HYDROCHLORIC ACID", "AMMONIA", "CHLOROFORM",
    "BENZENE", "ETHYLENE OXIDE"
]

# --- UNIVERSAL EPA AIR QUALITY MONITORING CONTROLS ---
TARGET_STATE = "Kentucky"
TARGET_COUNTIES = ["Marshall", "McCracken", "Livingston"]
# Prefer local workspace; fall back to Google Drive only if local EPA CSVs are missing
BASE_DATA_DIR = _WORKSPACE_DIR if os.path.exists(_WORKSPACE_DIR + "hourly_88101_2025.csv") else _DRIVE_DIR

EPA_MONITOR_CONFIG = {
    "PM2.5": {"path": BASE_DATA_DIR + "hourly_88101_2025.csv", "good": 12.0, "mod": 35.4, "unhealthy": 55.4},
    "VOCs": {"path": BASE_DATA_DIR + "hourly_VOCS_2025.csv", "good": 50.0, "mod": 150.0, "unhealthy": 300.0},
    "Ozone": {"path": BASE_DATA_DIR + "hourly_44201_2025.csv", "good": 0.054, "mod": 0.070, "unhealthy": 0.085},
    "SO2": {"path": BASE_DATA_DIR + "hourly_42401_2025.csv", "good": 35.0, "mod": 75.0, "unhealthy": 185.0},
    "NO2": {"path": BASE_DATA_DIR + "hourly_42602_2025.csv", "good": 53.0, "mod": 100.0, "unhealthy": 360.0},
    "HAPs": {"path": BASE_DATA_DIR + "hourly_HAPS_2025.csv", "good": 2.0, "mod": 10.0, "unhealthy": 25.0},
    "PM10": {"path": BASE_DATA_DIR + "hourly_81102_2025.csv", "good": 54.0, "mod": 154.0, "unhealthy": 254.0},
    "NONOxNOy": {"path": BASE_DATA_DIR + "hourly_NONOxNOy_2025.csv", "good": 53.0, "mod": 100.0, "unhealthy": 360.0}
}


# --- ENGINE MODIFIERS & PHYSICS ---
EMISSION_MULTIPLIER = 1.0  # Scales final output mass (e.g., 10.0 simulates a major leak)
RELEASE_HEIGHT_METERS = 15  # Starting vertical height in meters inside the HYSPLIT grid

# --- RENDERING & WEB VISUALIZATION CONTROLS ---
PARTICLES_PER_UNIT_EMISSION = 50  # Density multiplier for visual stream counts
MAX_PARTICLE_AGE_MINUTES = 120  # Lifespan of particle on canvas before complete opacity fade
BASE_PARTICLE_RADIUS_PIXELS = 2.5  # Drawing size of individual dots on the map canvas
MAP_ZOOM_LEVEL = 12  # Default Leaflet initial zoom view setting

# # --- DYNAMIC PLUG-AND-PLAY FACILITIES MATRIX ---
# To add a new facility, simply paste a new key-value block below matching the format.
# csv_match_name: The prefix of the facility name as it appears in the TRI CSV export.
# The entire pipeline will dynamically scale to accommodate new entries automatically.
#
# --- HOW TO CONFIGURE OPERATING HOURS SCHEDULES ---
# By default, facilities operate "continuous" (24/7). If a facility operates on a 
# limited shift/discontinuous basis, you can define a shift schedule like this:
#
#     "schedule": {
#         "type": "shift",
#         "start_hour": 8.0,  # 8:00 AM (24-hour decimal float)
#         "end_hour": 17.0    # 5:00 PM (24-hour decimal float)
#     }
#
FACILITIES = {
    "Westlake Vinyls": {
        "coords": (37.0345, -88.3512),
        "color": "#FF00FF",
        "tri_id": "42029WSTLK2468I",
        "csv_match_name": "WESTLAKE VINYLS INC",
        "mock_fallback": {"stack_lbs": 206864, "fugitive_lbs": 0},
        "schedule": "continuous"
    },
    "Westlake PVC Plant": {
        "coords": (37.0430, -88.3410),
        "color": "#DA70D6",
        "tri_id": "42029PCFCWJOHNS",
        "csv_match_name": "WESTLAKE VINYLS INC. - PVC",
        "mock_fallback": {"stack_lbs": 153757, "fugitive_lbs": 0},
        "schedule": "continuous"
    },
    "Arkema Inc": {
        "coords": (37.0548, -88.3670),
        "color": "#00FFFF",
        "tri_id": "42029PNNWLALTON",
        "csv_match_name": "ARKEMA",
        "mock_fallback": {"stack_lbs": 125106, "fugitive_lbs": 0},
        "schedule": "continuous"
    },
    "CC Metals & Alloys": {
        "coords": (37.0540, -88.3510),
        "color": "#FF4444",
        "tri_id": "42029SKWLLHIGHW",
        "csv_match_name": "CC METALS",
        "mock_fallback": {"stack_lbs": 58943, "fugitive_lbs": 0},
        "schedule": "continuous"
    },
    "Cymetech Corp": {
        "coords": (37.0330, -88.3350),
        "color": "#FF8C00",
        "tri_id": "42029CYMTC2468I",
        "csv_match_name": "CYMETECH",
        "mock_fallback": {"stack_lbs": 41, "fugitive_lbs": 0},
        "schedule": "continuous"
    },
    "Estron Chemicals": {
        "coords": (37.0420, -88.3500),
        "color": "#32CD32",
        "tri_id": "42029STRNCHIGHW",
        "csv_match_name": "ESTRON",
        "mock_fallback": {"stack_lbs": 24131, "fugitive_lbs": 0},
        "schedule": "continuous"
    },
    "Evonik Corp": {
        "coords": (37.0380, -88.3520),
        "color": "#FF1493",
        "tri_id": "42029DGSSCRTE28",
        "csv_match_name": "EVONIK",
        "mock_fallback": {"stack_lbs": 160390, "fugitive_lbs": 0},
        "schedule": "continuous"
    },
    "ISP Chemicals": {
        "coords": (37.0390, -88.3510),
        "color": "#00FF7F",
        "tri_id": "42029GFCHMHIGHW",
        "csv_match_name": "ISP CHEMICALS",
        "mock_fallback": {"stack_lbs": 241986, "fugitive_lbs": 0},
        "schedule": "continuous"
    },
    "Lubrizol Advanced Materials": {
        "coords": (37.0350, -88.3340),
        "color": "#9370DB",
        "tri_id": "42029NVNNC2468I",
        "csv_match_name": "LUBRIZOL",
        "mock_fallback": {"stack_lbs": 24386, "fugitive_lbs": 0},
        "schedule": "continuous"
    },
    "Sekisui Specialty Chemicals": {
        "coords": (37.0410, -88.3380),
        "color": "#FFD700",
        "tri_id": "42029CLNSL408NM",
        "csv_match_name": "SEKISUI",
        "mock_fallback": {"stack_lbs": 720080, "fugitive_lbs": 0},
        "schedule": "continuous"
    },
    "Wacker Chemical": {
        "coords": (37.0440, -88.3480),
        "color": "#1E90FF",
        "tri_id": "4202WWCKRC412NR",
        "csv_match_name": "WACKER",
        "mock_fallback": {"stack_lbs": 111346, "fugitive_lbs": 0},
        "schedule": "continuous"
    },
    "Carbide Industries": {
        "coords": (37.0522, -88.3414),
        "color": "#FFFF00",
        "tri_id": "42029THCRB3204I",
        "csv_match_name": "CARBIDE",
        "mock_fallback": {"stack_lbs": 85000, "fugitive_lbs": 10000},
        "schedule": "continuous"
    }
}    # ── To add a new facility, paste a new block above matching this format ──

TARGET_ZIP = "42029"
MAP_CENTER = (37.0317, -88.3542)
HYSPLIT_ENGINE_PATH = "/Users/nawrig04/hysplit/exec/hycs_std"
GRIB_CONVERTER_PATH = "/Users/nawrig04/hysplit/exec/api2arl_v6"
# ==============================================================================

import os
import sys
import glob
import json
import math
import shutil
import time
import datetime
import subprocess
import argparse
import csv
from typing import Dict, List, Any

class CalvertCityPlumeEngine:
    """
    Orchestration class for the Calvert City HYSPLIT dispersion modeling and visualization pipeline.
    """
    
    def __init__(self, workspace_dir: str, output_html_name: str = "index.html"):
        """
        Initialize the dispersion engine configuration.
        
        Args:
            workspace_dir: Absolute path to the simulation workspace directory.
            output_html_name: Filename for the generated interactive HTML visualization.
        """
        self.original_workspace_dir = os.path.abspath(workspace_dir)
        self.workspace_dir = self.original_workspace_dir
        
        # Check if workspace_dir has spaces. HYSPLIT and api2arl require space-free paths.
        if " " in self.workspace_dir:
            home_dir = os.path.expanduser("~")
            symlink_path = os.path.join(home_dir, "plume_workspace_link")
            
            # Remove existing link or file if one exists
            if os.path.exists(symlink_path) or os.path.islink(symlink_path):
                try:
                    if os.path.islink(symlink_path):
                        os.unlink(symlink_path)
                    elif os.path.isdir(symlink_path):
                        shutil.rmtree(symlink_path)
                    else:
                        os.remove(symlink_path)
                except Exception as e:
                    print(f"Warning: Could not remove existing link {symlink_path}: {e}")
            
            try:
                os.symlink(self.original_workspace_dir, symlink_path)
                print(f"Created space-free symlink: {symlink_path} -> {self.original_workspace_dir}")
                self.workspace_dir = symlink_path
            except Exception as e:
                print(f"Error creating symlink {symlink_path}: {e}. Proceeding with original path (may fail).")
                
        # Resolve executables from global configuration paths
        self.hycs_std_path = os.path.abspath(HYSPLIT_ENGINE_PATH)
        self.hysplit_exec_dir = os.path.dirname(self.hycs_std_path)
        self.api2arl_path = os.path.abspath(GRIB_CONVERTER_PATH)
        self.par2asc_path = os.path.join(self.hysplit_exec_dir, "par2asc")
        self.output_html_name = output_html_name
        
        # Parse simulation date from START_DATE
        self.set_active_date(START_DATE)
        
        # ecCodes definitions path — required by api2arl_v6 to decode GRIB2 files.
        self.eccodes_defs_path = os.path.join(
            os.path.dirname(self.hysplit_exec_dir), "share", "eccodes", "definitions"
        )
        if not os.path.isdir(self.eccodes_defs_path):
            print(f"WARNING: ecCodes definitions not found at {self.eccodes_defs_path}")
        
        # Core industrial facilities configuration with dynamic geolocation harvesting
        import pandas as pd
        df_coords = None
        if os.path.exists(LOCAL_TRI_CSV_PATH):
            try:
                df_coords = pd.read_csv(LOCAL_TRI_CSV_PATH)
                print(f"Loaded CSV using pandas for coordinate harvesting: {LOCAL_TRI_CSV_PATH}")
            except Exception as e:
                print(f"Error loading CSV with pandas: {e}")

        self.facilities = []
        for idx, (name, details) in enumerate(FACILITIES.items()):
            lat = details["coords"][0]
            lon = details["coords"][1]
            
            # Dynamic coordinate harvesting
            if df_coords is not None and "facility name" in df_coords.columns:
                csv_match = details.get("csv_match_name", "").upper()
                if csv_match:
                    matched_rows = df_coords[df_coords["facility name"].str.upper().str.startswith(csv_match, na=False)]
                    if matched_rows.empty:
                        matched_rows = df_coords[df_coords["facility name"].str.upper().str.contains(csv_match, na=False)]
                    
                    if not matched_rows.empty:
                        row_lat = matched_rows.iloc[0].get("latitude")
                        row_lon = matched_rows.iloc[0].get("longitude")
                        try:
                            # parse absolute values
                            parsed_lat = abs(float(row_lat))
                            parsed_lon = -abs(float(row_lon))  # Longitude in USA is negative
                            if not math.isnan(parsed_lat) and not math.isnan(parsed_lon):
                                lat = parsed_lat
                                lon = parsed_lon
                                print(f"Dynamically harvested coordinates for {name}: ({lat}, {lon})")
                        except Exception as e:
                            print(f"Error parsing coordinates for {name}: {e}")

            self.facilities.append({
                "id": idx,
                "name": name,
                "lat": lat,
                "lon": lon,
                "height": float(RELEASE_HEIGHT_METERS),
                "color": details["color"],
                "tri_id": details["tri_id"],
                "schedule": details.get("schedule", "continuous")
            })
            
        # Grid variables and directories
        # WEATHER_CACHE_DIR supports user home expanding
        self.grib_dir = os.path.expanduser(WEATHER_CACHE_DIR)
        
        # Initialize file system structures
        os.makedirs(self.workspace_dir, exist_ok=True)
        os.makedirs(self.grib_dir, exist_ok=True)
        
        # Parse TRI CSV release data once at initialization
        self.tri_csv_path = LOCAL_TRI_CSV_PATH
        self.tri_data = self.parse_tri_csv()
        
        # Precompute maximum emissions across all facilities for relative scaling
        all_totals = []
        for fac in self.facilities:
            tri_data = self.get_facility_releases(fac["name"])
            releases = tri_data.get("releases", [])
            total_lbs = sum(chem.get("total_lbs", 0.0) for chem in releases)
            all_totals.append(total_lbs)
        self.max_facility_lbs = max(all_totals) if all_totals else 1.0
        if self.max_facility_lbs == 0.0:
            self.max_facility_lbs = 1.0

    def set_active_date(self, date_str: str):
        """
        Set the active simulation date and update all dependent variables and paths.
        """
        self.date_str = date_str
        self.date_obj = datetime.datetime.strptime(self.date_str, "%Y-%m-%d")
        self.met_file_path = os.path.join(self.workspace_dir, f"MET_{self.date_obj.strftime('%Y%m%d')}.ARL")
        
    def parse_tri_csv(self) -> Dict[str, list]:
        """
        Parse the TRI Explorer release CSV file.
        Ingests the local TRI file, harvesting facility locations and emissions.
        """
        if not os.path.exists(self.tri_csv_path):
            print(f"Warning: TRI CSV file not found at {self.tri_csv_path}. Will use mock fallback data.")
            return {}
        
        result = {}
        try:
            with open(self.tri_csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    fac_name = row.get("facility name", "").strip().upper()
                    if not fac_name:
                        continue
                    
                    chem_name = row.get("chemical", "").strip().upper()
                    if not chem_name:
                        continue
                        
                    # Extract fugitive and stack air releases in pounds
                    fugitive_lbs = self._parse_tri_amount(row.get("5.1 - fugitive air", "0"))
                    stack_lbs = self._parse_tri_amount(row.get("5.2 - stack air", "0"))
                    total_lbs = fugitive_lbs + stack_lbs
                    
                    # Calculate grams/hour values
                    conv_factor = 453.59237 / 8760.0
                    fugitive_g_hr = fugitive_lbs * conv_factor
                    stack_g_hr = stack_lbs * conv_factor
                    
                    # Determine default active state status
                    default_active = chem_name in DEFAULT_ACTIVE_CHEMICALS
                    
                    if fac_name not in result:
                        result[fac_name] = []
                        
                    # Consolidate duplicate chemical entries if they exist
                    existing = [c for c in result[fac_name] if c["chemical"] == chem_name]
                    if existing:
                        existing[0]["stack_lbs"] = round(existing[0]["stack_lbs"] + stack_lbs, 2)
                        existing[0]["fugitive_lbs"] = round(existing[0]["fugitive_lbs"] + fugitive_lbs, 2)
                        existing[0]["total_lbs"] = round(existing[0]["total_lbs"] + total_lbs, 2)
                        existing[0]["stack_g_hr"] = round(existing[0]["stack_g_hr"] + stack_g_hr, 4)
                        existing[0]["fugitive_g_hr"] = round(existing[0]["fugitive_g_hr"] + fugitive_g_hr, 4)
                    else:
                        result[fac_name].append({
                            "chemical": chem_name,
                            "stack_lbs": round(stack_lbs, 2),
                            "fugitive_lbs": round(fugitive_lbs, 2),
                            "total_lbs": round(total_lbs, 2),
                            "stack_g_hr": round(stack_g_hr, 4),
                            "fugitive_g_hr": round(fugitive_g_hr, 4),
                            "defaultActive": default_active
                        })
        except Exception as e:
            print(f"Error parsing flat TRI CSV: {e}")
            return {}
            
        print(f"Parsed TRI CSV: {len(result)} facilities loaded from {os.path.basename(self.tri_csv_path)}")
        for fac_key in result:
            print(f"  {fac_key}: {len(result[fac_key])} chemicals")
        return result
    
    @staticmethod
    def _parse_tri_amount(raw_value: str) -> float:
        """Parse a TRI numeric field, handling commas, leading whitespace, and '.' as zero."""
        if not raw_value or raw_value.strip() in (".", "**", "NA", ""):
            return 0.0
        try:
            return float(raw_value.strip().replace(",", ""))
        except (ValueError, TypeError):
            return 0.0
    
    def get_facility_releases(self, facility_name: str) -> Dict[str, Any]:
        """
        Look up a facility's chemical release data from the parsed TRI CSV.
        Matches using the csv_match_name field from the FACILITIES config dict.
        Falls back to mock_fallback data if no CSV match is found.
        
        Matching priority: exact match > startswith > contains, preferring shortest key.
        """
        fac_config = FACILITIES.get(facility_name, {})
        csv_match = fac_config.get("csv_match_name", "")
        
        if csv_match and self.tri_data:
            csv_match_upper = csv_match.upper()
            
            # Try exact match first
            if csv_match_upper in self.tri_data:
                releases = self.tri_data[csv_match_upper]
                sorted_releases = sorted(releases, key=lambda x: x["total_lbs"], reverse=True)
                print(f"CSV match for {facility_name}: {len(sorted_releases)} chemicals (exact match '{csv_match}')")
                return {"fac_name": facility_name, "releases": sorted_releases, "source": "csv"}
            
            # Try startswith, prefer shortest key (most specific)
            candidates = [(k, v) for k, v in self.tri_data.items() 
                          if k.startswith(csv_match_upper) or csv_match_upper in k]
            if candidates:
                # Sort by key length so the most specific (shortest) match wins
                candidates.sort(key=lambda x: len(x[0]))
                best_key, releases = candidates[0]
                sorted_releases = sorted(releases, key=lambda x: x["total_lbs"], reverse=True)
                print(f"CSV match for {facility_name}: {len(sorted_releases)} chemicals (matched '{csv_match}' -> '{best_key}')")
                return {"fac_name": facility_name, "releases": sorted_releases, "source": "csv"}
        
        print(f"No CSV match for {facility_name} (csv_match_name='{csv_match}'). Using mock fallback.")
        return self._get_mock_tri_data(facility_name)
    
    def _get_mock_tri_data(self, facility_name: str) -> Dict[str, Any]:
        """
        Produce a mock emissions record from the facility's embedded mock_fallback config.
        """
        fac_config = FACILITIES.get(facility_name, {})
        mock_data = fac_config.get("mock_fallback", {"stack_lbs": 10000, "fugitive_lbs": 5000})
        stack_lbs = mock_data.get("stack_lbs", 0)
        fugitive_lbs = mock_data.get("fugitive_lbs", 0)
        total_lbs = stack_lbs + fugitive_lbs
        
        conv_factor = 453.59237 / 8760.0
        stack_g_hr = stack_lbs * conv_factor
        fugitive_g_hr = fugitive_lbs * conv_factor
        
        return {
            "fac_name": facility_name.upper(),
            "releases": [
                {
                    "chemical": "SIMULATED POINT-SOURCE SPECIES",
                    "stack_lbs": float(stack_lbs),
                    "fugitive_lbs": float(fugitive_lbs),
                    "total_lbs": float(total_lbs),
                    "stack_g_hr": round(stack_g_hr, 4),
                    "fugitive_g_hr": round(fugitive_g_hr, 4),
                    "defaultActive": True
                }
            ],
            "source": "mock"
        }

    def download_weather_data(self) -> List[str]:
        """
        Retrieve 24 hourly NOAA HRRR GRIB2 files using the Herbie library.
        Bound strictly to self.date_obj and global cache directory structure.
        
        Returns:
            List of absolute paths to downloaded GRIB2 files.
        """
        print(f"Starting NOAA HRRR weather data download via Herbie for {self.date_str}...")
        from herbie import Herbie
        
        grib_files = []
        for hour in range(24):
            dt_hour = self.date_obj.replace(hour=hour)
            date_time_str = dt_hour.strftime("%Y-%m-%d %H:%M")
            print(f"Downloading HRRR grid for simulation hour {hour:02d}:00 ({date_time_str})...")
            try:
                # Retrieve HRRR pressure level grid (fxx=0 represents analysis hour)
                h = Herbie(
                    dt_hour,
                    model="hrrr",
                    product="prs",
                    fxx=0,
                    save_dir=self.grib_dir
                )
                file_path = h.download()
                if file_path and os.path.exists(file_path):
                    print(f"File cached at: {file_path}")
                    grib_files.append(str(file_path))
                else:
                    print(f"Warning: Download returned empty or path does not exist for hour {hour}.")
            except Exception as e:
                print(f"Error downloading weather grid for hour {hour}: {e}")
                
        if not grib_files:
            raise RuntimeError("Weather download yielded zero files. Simulation aborted.")
            
        print(f"Successfully retrieved {len(grib_files)} weather grid files.")
        return grib_files

    def convert_grib_to_arl(self, grib_files: List[str]):
        """
        Convert weather grids to HYSPLIT ARL format using api2arl_v6.
        Concatenates hourly conversions into a single daily ARL meteorology file.
        
        Args:
            grib_files: List of file paths to raw GRIB2 files.
        """
        print("Converting GRIB2 files to HYSPLIT ARL format using api2arl_v6...")
        if not os.path.exists(self.api2arl_path):
            raise FileNotFoundError(f"HYSPLIT api2arl_v6 executable not found at {self.api2arl_path}")
            
        if os.path.exists(self.met_file_path):
            os.remove(self.met_file_path)
            
        # Sort files chronologically to maintain ARL record consistency
        for idx, grib_file in enumerate(sorted(grib_files)):
            grib_dir = os.path.dirname(grib_file)
            grib_filename = os.path.basename(grib_file)
            
            # Temporary output file inside the same directory as the GRIB file (keeps paths short)
            local_temp_arl = os.path.join(grib_dir, "DATA.ARL")
            local_cfg_path = os.path.join(grib_dir, "arldata.cfg")
            
            # Remove any intermediate DATA.ARL or arldata.cfg in the GRIB dir
            if os.path.exists(local_temp_arl):
                os.remove(local_temp_arl)
            if os.path.exists(local_cfg_path):
                os.remove(local_cfg_path)
                
            print(f"Processing grid file {idx+1}/{len(grib_files)}: {grib_filename}")
            
            # Execute api2arl_v6 inside the GRIB directory using relative arguments
            cmd = [
                self.api2arl_path,
                f"-i{grib_filename}",
                "-oDATA.ARL",
                "-z1"  # Initialize file structure
            ]
            
            # Build environment with ecCodes definitions path for the GRIB decoder
            run_env = os.environ.copy()
            run_env["ECCODES_DEFINITION_PATH"] = self.eccodes_defs_path
            
            try:
                result = subprocess.run(
                    cmd,
                    cwd=grib_dir,
                    env=run_env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=180
                )
                
                if result.returncode != 0:
                    print(f"Error converting {grib_filename}: code {result.returncode}")
                    print(f"Stderr: {result.stderr}")
                    continue
                    
                # Append the newly converted time slice to the primary daily ARL file
                if os.path.exists(local_temp_arl):
                    with open(self.met_file_path, "ab") as dest_file, open(local_temp_arl, "rb") as src_file:
                        shutil.copyfileobj(src_file, dest_file)
                    print(f"Appended hour {idx} records to daily meteorology grid.")
                    os.remove(local_temp_arl)
                else:
                    print(f"Warning: Expected output {local_temp_arl} not found after conversion.")
                
                if os.path.exists(local_cfg_path):
                    os.remove(local_cfg_path)
                    
            except subprocess.TimeoutExpired:
                print(f"Timeout occurred during conversion of {grib_filename}.")
            except Exception as e:
                print(f"Unexpected error converting {grib_filename}: {e}")
            
        if not os.path.exists(self.met_file_path) or os.path.getsize(self.met_file_path) == 0:
            raise RuntimeError("Daily ARL meteorology file is empty or was not created.")
            
        print(f"Successfully compiled compiled meteorology file: {self.met_file_path}")

    def write_control_file(self, run_dir: str, facility: Dict[str, Any]):
        """
        Generate a HYSPLIT CONTROL file configured for a single-source dispersion simulation.
        Ensures strict coupling to the emission multiplier, release heights, and physics grids.
        
        Args:
            run_dir: Directory where the CONTROL file should be written.
            facility: Dictionary containing facility release parameters.
        """
        control_path = os.path.join(run_dir, "CONTROL")
        
        # Dates formatted as double digit strings
        yy = self.date_obj.strftime("%y")
        mm = self.date_obj.strftime("%m")
        dd = self.date_obj.strftime("%d")
        
        # Dynamic calculation of grids based on WEATHER_BOX_RADIUS_KM (approx 111 km per degree)
        grid_span = float(WEATHER_BOX_RADIUS_KM) / 111.0
        grid_span_str = f"{grid_span:.3f} {grid_span:.3f}"
        
        lines = [
            f"{yy} {mm} {dd} 01",                             # Start time (YY MM DD HH) - 01 UTC (t00z met unavailable)
            "1",                                              # Number of starting locations
            f"{facility['lat']:.4f} {facility['lon']:.4f} {facility['height']:.1f}",  # Lat, Lon, Height (m AGL)
            "23",                                             # Simulation duration (hours) - 01 through 23 UTC
            "0",                                              # Vertical motion method (0 = use met data vertical velocity)
            "10000.0",                                        # Top of simulation model (m AGL)
            "1",                                              # Number of input meteorology files
            os.path.dirname(self.met_file_path) + "/",       # Directory of meteorology grid (with trailing slash)
            os.path.basename(self.met_file_path),             # Filename of meteorology grid
            "1",                                              # Number of pollutant species
            "POL",                                            # Pollutant identifier tag
            f"{float(EMISSION_MULTIPLIER):.3f}",              # Emission rate bound to global multiplier (units/hour)
            "23.0",                                           # Emission duration (hours)
            f"{yy} {mm} {dd} 01 00",                          # Emission release start (YY MM DD HH MM)
            # --- Concentration grid definition ---
            "1",                                              # Number of concentration grids
            f"{MAP_CENTER[0]:.4f} {MAP_CENTER[1]:.4f}",       # Grid center from global configuration
            "0.02 0.02",                                      # High resolution grid spacing (degrees lat, lon)
            grid_span_str,                                    # Dynamic grid span derived from WEATHER_BOX_RADIUS_KM
            run_dir + "/",                                    # Output directory (with trailing slash)
            "cdump",                                          # Output filename prefix
            "1",                                              # Number of vertical concentration levels
            "100",                                            # Height of level (m AGL)
            f"{yy} {mm} {dd} 00 00",                          # Sampling start time (YY MM DD HH MM)
            f"{yy} {mm} {dd} 00 00",                          # Sampling stop time (YY MM DD HH MM) - 00=use run end
            "01 00 00",                                       # Averaging period (HH MM SS) - hourly snapshots
            # --- Deposition definition (per pollutant species) ---
            "1",                                              # Number of depositing species
            "0.0 0.0 0.0",                                    # Dry deposition: vel(m/s), mol_wt(g), A-ratio
            "0.0 0.0 0.0 0.0 0.0",                            # Wet removal: Henry, in-cloud, below-cloud, type, decay
            "0.0 0.0 0.0",                                    # Resuspension: factor, min_size, max_size
            "0.0",                                            # Radioactive decay half-life (0=none)
            "0.0",                                            # Pollutant resuspension factor (0=none)
        ]
        
        with open(control_path, "w") as f:
            f.write("\n".join(lines) + "\n")
        print(f"CONTROL file written to: {control_path}")

    def write_setup_file(self, run_dir: str, facility: Dict[str, Any]):
        """
        Generate the HYSPLIT SETUP.cfg file to configure particle dumps.
        Scales the number of computational particles (numpar) proportionally
        to the facility's total emissions relative to the maximum emitter,
        enforcing a minimum count of 10 particles for dispersion visualization.
        
        Args:
            run_dir: Directory where SETUP.cfg should be written.
            facility: Dictionary containing facility release parameters.
        """
        setup_path = os.path.join(run_dir, "SETUP.cfg")
        
        # Get total emissions for this facility
        tri_data = self.get_facility_releases(facility["name"])
        releases = tri_data.get("releases", [])
        total_lbs = sum(chem.get("lbs_year", 0.0) for chem in releases)
        
        # Scale HYSPLIT particles based on PARTICLES_PER_UNIT_EMISSION configuration
        base_numpar = int(PARTICLES_PER_UNIT_EMISSION * 10)
        ratio = total_lbs / self.max_facility_lbs
        numpar_value = int(base_numpar * ratio)
        
        # Enforce floor of 10 particles so even the smallest source produces a visible plume path
        if numpar_value < 10:
            numpar_value = 10
            
        # Make numpar negative to force constant hourly emission rate in HYSPLIT point-source mode
        numpar_value = -numpar_value
        
        # Max particle age converted to hours for HYSPLIT config (khmax)
        khmax_hours = max(1, int(MAX_PARTICLE_AGE_MINUTES / 60))
        
        content = (
            "&SETUP\n"
            "  initd = 0,\n"                            # No particle initialization file at start
            f"  khmax = {khmax_hours},\n"                # Max lifetime of particles (hours) derived from config
            "  ndump = 1,\n"                            # Dump particle positions every 1 hour
            "  ncycl = 1,\n"                            # Particle release cycle interval (hours)
            f"  numpar = {numpar_value},\n"              # Particles released per cycle mapped from config
            "  maxpar = 30000,\n"                       # Max total active particles in memory
            "  poutf = 'PARDUMP',\n"                    # Particle dump output file name
            "/\n"
        )
        with open(setup_path, "w") as f:
            f.write(content)
        print(f"SETUP.cfg written to: {setup_path} (numpar={numpar_value})")

    def convert_and_parse_pardumps(self, run_dir: str, facility_idx: int) -> Dict[int, List[Dict[str, Any]]]:
        """
        Convert HYSPLIT binary PARDUMP files to GIS-compatible CSV files, then parse coordinates.
        The single PARDUMP binary contains all hourly particle snapshots. par2asc extracts them
        into a PAR_GIS.txt with a 'time' column that we use to group particles by hour.
        
        Args:
            run_dir: Path to directory containing output files.
            facility_idx: Numeric facility index for labeling particle source.
            
        Returns:
            Dict mapping hour index to lists of particle dictionaries.
        """
        print(f"Extracting particle positions from PARDUMP binaries in: {run_dir}...")
        if not os.path.exists(self.par2asc_path):
            raise FileNotFoundError(f"HYSPLIT par2asc executable not found at {self.par2asc_path}")
        
        # Find the PARDUMP file (single file containing all hourly snapshots)
        pardump_path = os.path.join(run_dir, "PARDUMP")
        if not os.path.exists(pardump_path):
            # Check for numbered variants
            candidates = sorted(glob.glob(os.path.join(run_dir, "PARDUMP.*")))
            if candidates:
                pardump_path = candidates[0]
            else:
                print(f"Warning: No PARDUMP files found in {run_dir}.")
                return {}
        
        # Clear pre-existing outputs from past executions
        gis_output = os.path.join(run_dir, "PAR_GIS.txt")
        if os.path.exists(gis_output):
            os.remove(gis_output)
            
        cmd = [
            self.par2asc_path,
            f"-i{pardump_path}",
            "-oPAR_ASC.txt",
            "-a1"  # Generates 1-line-per-particle PAR_GIS.txt file
        ]
        
        try:
            result = subprocess.run(
                cmd,
                cwd=run_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                print(f"Warning: par2asc failed: {result.returncode}")
                print(f"Stderr: {result.stderr}")
                return {}
                
            if os.path.exists(gis_output):
                hourly_particles = self.parse_gis_file_by_hour(gis_output, facility_idx)
                total = sum(len(v) for v in hourly_particles.values())
                print(f"Parsed {total} total particles across {len(hourly_particles)} hourly snapshots")
                return hourly_particles
            else:
                print(f"Warning: PAR_GIS.txt was not written by par2asc.")
                return {}
        except Exception as e:
            print(f"Error converting PARDUMP file: {e}")
            return {}

    def parse_gis_file_by_hour(self, gis_filepath: str, facility_idx: int) -> Dict[int, List[Dict[str, Any]]]:
        """
        Parse GIS text file containing one-line particle data, grouping by dump hour.
        Filters out particles that drift beyond WEATHER_BOX_RADIUS_KM from MAP_CENTER.
        
        Args:
            gis_filepath: File path to converted PAR_GIS.txt file.
            facility_idx: Numeric facility index for classification.
            
        Returns:
            Dict mapping hour index (1-23) to lists of particle dictionaries.
        """
        hourly_data = {}
        with open(gis_filepath, "r") as f:
            header_line = f.readline().strip()
            if not header_line:
                return {}
                
            # Parse header indices dynamically
            headers = [h.strip().lower() for h in header_line.split(",")]
            header_map = {name: idx for idx, name in enumerate(headers)}
            
            # The 'time' column is always index 0 in PAR_GIS.txt
            time_idx = header_map.get("time", 0)
            lat_idx = header_map.get("latitude") or header_map.get("lat")
            lon_idx = header_map.get("longitude") or header_map.get("lon")
            height_idx = header_map.get("height") or header_map.get("zlvl")
            age_idx = header_map.get("page") or header_map.get("age")
            nsort_idx = header_map.get("nsort") or header_map.get("id")
            
            if lat_idx is None or lon_idx is None:
                print(f"Error parsing headers in {gis_filepath}. Required fields missing.")
                return {}
                
            for line in f:
                line = line.strip()
                if not line:
                    continue
                cols = [c.strip() for c in line.split(",")]
                if len(cols) < len(headers):
                    continue
                    
                try:
                    # Extract hour from time column (format: "M/DD/YY HH:MM" or "M/ D/YY  H: M")
                    time_str = cols[time_idx].strip()
                    time_parts = time_str.split()
                    hour = 1  # default
                    for part in time_parts:
                        if ":" in part:
                            hour = int(part.replace(":", ""))
                            break
                    
                    lat = float(cols[lat_idx])
                    lon = float(cols[lon_idx])
                    
                    # Apply physics limits: Filter out particles exceeding WEATHER_BOX_RADIUS_KM from MAP_CENTER
                    if not self._is_within_radius(lat, lon):
                        continue
                        
                    height = float(cols[height_idx]) if height_idx is not None else 0.0
                    age = int(float(cols[age_idx])) if age_idx is not None else 0
                    nsort = int(cols[nsort_idx]) if nsort_idx is not None else 0
                    
                    particle = {
                        "id": nsort,
                        "lat": round(lat, 5),
                        "lon": round(lon, 5),
                        "height": round(height, 1),
                        "age": age,
                        "facility": facility_idx
                    }
                    
                    if hour not in hourly_data:
                        hourly_data[hour] = []
                    hourly_data[hour].append(particle)
                    
                except Exception:
                    continue
                    
        return hourly_data

    def _is_within_radius(self, lat: float, lon: float) -> bool:
        """
        Calculate if coordinate falls within WEATHER_BOX_RADIUS_KM from MAP_CENTER using Haversine formulas.
        """
        lat1, lon1 = MAP_CENTER
        lat2, lon2 = lat, lon
        
        # Radius of Earth in kilometers
        R = 6371.0
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        
        return distance <= float(WEATHER_BOX_RADIUS_KM)

    def run_dispersion_model(self) -> Dict[str, Dict[int, List[Dict[str, Any]]]]:
        """
        Run HYSPLIT simulation loops independently for each facility.
        
        Returns:
            Dict nested by facility name, then hour index, containing lists of particles.
        """
        print("Executing dispersion model simulations...")
        if not os.path.exists(self.hycs_std_path):
            raise FileNotFoundError(f"HYSPLIT hycs_std executable not found at {self.hycs_std_path}")
        
        # HYSPLIT expects boundary files (ASCDATA.CFG, LANDUSE.ASC, etc.) at ../bdyfiles/
        # relative to each run directory. Create a symlink in the workspace to the HYSPLIT bdyfiles.
        hysplit_bdyfiles = os.path.join(os.path.dirname(self.hysplit_exec_dir), "bdyfiles")
        workspace_bdyfiles = os.path.join(self.workspace_dir, "bdyfiles")
        if os.path.isdir(hysplit_bdyfiles):
            if os.path.exists(workspace_bdyfiles) or os.path.islink(workspace_bdyfiles):
                try:
                    if os.path.islink(workspace_bdyfiles):
                        os.unlink(workspace_bdyfiles)
                    elif os.path.isdir(workspace_bdyfiles):
                        pass
                    else:
                        os.remove(workspace_bdyfiles)
                except Exception as e:
                    print(f"Warning: Could not remove existing link {workspace_bdyfiles}: {e}")
            
            if not os.path.exists(workspace_bdyfiles) and not os.path.islink(workspace_bdyfiles):
                os.symlink(hysplit_bdyfiles, workspace_bdyfiles)
                print(f"Linked boundary files: {workspace_bdyfiles} -> {hysplit_bdyfiles}")
            
        all_facility_particles = {}
        
        for idx, facility in enumerate(self.facilities):
            name = facility["name"]
            print(f"\n========================================\nSource Group: {name}")
            
            # Setup dedicated run directory to prevent file locking issues
            run_dir_name = f"run_{name.lower().replace(' ', '_')}"
            run_dir = os.path.join(self.workspace_dir, run_dir_name)
            os.makedirs(run_dir, exist_ok=True)
            
            self.write_control_file(run_dir, facility)
            self.write_setup_file(run_dir, facility)
            
            print(f"Launching HYSPLIT hycs_std in workspace: {run_dir}...")
            try:
                result = subprocess.run(
                    [self.hycs_std_path],
                    cwd=run_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=300
                )
                
                if result.returncode != 0:
                    print(f"Error: HYSPLIT execution failed for {name} (exit code: {result.returncode})")
                    print(f"Stderr: {result.stderr}")
                    continue
                    
                print(f"HYSPLIT run successful. Log output written to HYSPLIT MESSAGE files.")
                
                # Convert and read the binary dumps
                parsed_particles = self.convert_and_parse_pardumps(run_dir, idx)
                all_facility_particles[name] = parsed_particles
                
            except subprocess.TimeoutExpired:
                print(f"Timeout occurred executing HYSPLIT for {name}.")
            except Exception as e:
                print(f"Unexpected execution failure for {name}: {e}")
                
        return all_facility_particles

    def process_ambient_monitors(self) -> Dict[str, Any]:
        """
        Process the EPA monitoring CSV files in chunks.
        Extract units of measure dynamically and filter for target state and counties on target date.
        """
        import pandas as pd
        import numpy as np

        regional_monitor_data = {}

        for pollutant, info in EPA_MONITOR_CONFIG.items():
            csv_path = info["path"]
            if not os.path.exists(csv_path):
                print(f"Warning: CSV file for {pollutant} not found at {csv_path}. Skipping.")
                regional_monitor_data[pollutant] = {
                    "unit": "N/A",
                    "good": info["good"],
                    "mod": info["mod"],
                    "unhealthy": info["unhealthy"],
                    "stations": {}
                }
                continue

            unit = None
            stations_data = {}  # station_id -> {county, lat, lon, parameter_name, hourly_values: [[] for _ in range(24)]}

            print(f"Processing EPA monitor data for {pollutant} from {os.path.basename(csv_path)}...")
            try:
                # Optimized line-by-line reading with pre-filtering
                with open(csv_path, "r", encoding="utf-8") as f:
                    header_line = f.readline()
                    if not header_line:
                        continue
                    
                    # Parse header to find column indices
                    reader = csv.reader([header_line])
                    headers = next(reader)
                    
                    try:
                        idx_state_name = headers.index('State Name')
                        idx_county_name = headers.index('County Name')
                        idx_date_local = headers.index('Date Local')
                        idx_units = headers.index('Units of Measure')
                        idx_state_code = headers.index('State Code')
                        idx_county_code = headers.index('County Code')
                        idx_site_num = headers.index('Site Num')
                        idx_lat = headers.index('Latitude')
                        idx_lon = headers.index('Longitude')
                        idx_param_name = headers.index('Parameter Name')
                        idx_time_local = headers.index('Time Local')
                        idx_sample_meas = headers.index('Sample Measurement')
                    except ValueError as ve:
                        print(f"Warning: Missing required columns in {csv_path}: {ve}. Skipping.")
                        continue
                    
                    target_counties_set = set(TARGET_COUNTIES)
                    
                    # Fast search loop to identify matching lines as raw strings
                    matching_lines = []
                    for line in f:
                        if TARGET_STATE in line and self.date_str in line:
                            matching_lines.append(line)
                            
                if matching_lines:
                    reader = csv.reader(matching_lines)
                    for row in reader:
                        if len(row) <= max(idx_state_name, idx_county_name, idx_date_local):
                            continue
                        if row[idx_state_name] != TARGET_STATE:
                            continue
                        if row[idx_county_name] not in target_counties_set:
                            continue
                        if row[idx_date_local] != self.date_str:
                            continue
                            
                        # Extract units dynamically from first matched row
                        if unit is None:
                            unit_val = row[idx_units].strip()
                            if unit_val:
                                unit = unit_val
                                
                        state_code = row[idx_state_code].strip().zfill(2)
                        county_code = row[idx_county_code].strip().zfill(3)
                        site_num = row[idx_site_num].strip().zfill(4)
                        station_id = f"{state_code}-{county_code}-{site_num}"
                        
                        lat = float(row[idx_lat])
                        lon = float(row[idx_lon])
                        county = row[idx_county_name].strip()
                        param_name = row[idx_param_name].strip()
                        
                        time_str = row[idx_time_local].strip()
                        try:
                            hour = int(time_str.split(':')[0])
                        except Exception:
                            continue
                            
                        if not (0 <= hour <= 23):
                            continue
                            
                        val_str = row[idx_sample_meas]
                        if not val_str or val_str.strip() == "":
                            val = None
                        else:
                            try:
                                val = float(val_str)
                            except ValueError:
                                val = None
                                
                        if station_id not in stations_data:
                            stations_data[station_id] = {
                                "county": county,
                                "lat": lat,
                                "lon": lon,
                                "parameter_name": param_name,
                                "hourly_values": [[] for _ in range(24)]
                            }
                            
                        if val is not None:
                            stations_data[station_id]["hourly_values"][hour].append(val)

                # After chunking, finalize station values (average multiple measurements for the same hour)
                formatted_stations = {}
                for sid, sinfo in stations_data.items():
                    hourly_data = [None] * 24
                    for h in range(24):
                        vals = sinfo["hourly_values"][h]
                        if vals:
                            hourly_data[h] = float(np.mean(vals))

                    formatted_stations[sid] = {
                        "county": sinfo["county"],
                        "lat": sinfo["lat"],
                        "lon": sinfo["lon"],
                        "parameter_name": sinfo["parameter_name"],
                        "hourly_data": hourly_data
                    }

                # Store compiled data
                regional_monitor_data[pollutant] = {
                    "unit": unit if unit is not None else "N/A",
                    "good": info["good"],
                    "mod": info["mod"],
                    "unhealthy": info["unhealthy"],
                    "stations": formatted_stations
                }

                # Print summary
                num_stations = len(formatted_stations)
                print(f"  Pollutant {pollutant}: unit='{unit}', found {num_stations} stations in target counties.")

            except Exception as e:
                print(f"Error processing CSV for {pollutant}: {e}")
                regional_monitor_data[pollutant] = {
                    "unit": "N/A",
                    "good": info["good"],
                    "mod": info["mod"],
                    "unhealthy": info["unhealthy"],
                    "stations": {}
                }

        # --- PARSE LOCAL CALVERT CITY DAILY VOC EXCEL DATA ---
        excel_path = os.path.join(self.original_workspace_dir, "CalvertDailyVOCS_DateEnding6.30.2025.xlsx")
        if os.path.exists(excel_path):
            print(f"Processing local Calvert City VOC data from {os.path.basename(excel_path)}...")
            try:
                # Read the excel file
                df_voc = pd.read_excel(excel_path)
                df_voc['Date Local'] = pd.to_datetime(df_voc['Date Local'])
                
                # Find all unique dates in the Excel file
                available_dates = df_voc['Date Local'].dropna().unique()
                
                if len(available_dates) > 0:
                    target_date = pd.to_datetime(self.date_str)
                    
                    # Find the next available sample date on or after the target date,
                    # since canisters accumulate air in the days leading up to the sample date.
                    future_dates = [d for d in available_dates if pd.to_datetime(d) >= target_date]
                    if future_dates:
                        closest_date = min(future_dates)
                    else:
                        closest_date = max(available_dates) # Fallback to the latest available past date
                        
                    closest_date_str = pd.to_datetime(closest_date).strftime('%Y-%m-%d')
                    days_diff = int(abs((pd.to_datetime(closest_date) - target_date).days))
                    
                    # Filter dataset for the closest date
                    df_date = df_voc[df_voc['Date Local'] == closest_date]
                    
                    if not df_date.empty:
                        # Make sure the "VOCs" parameter group exists and has proper units
                        if "VOCs" in regional_monitor_data:
                            if regional_monitor_data["VOCs"].get("unit") in (None, "N/A", "None", "None"):
                                regional_monitor_data["VOCs"]["unit"] = "ppbC"
                        else:
                            regional_monitor_data["VOCs"] = {
                                "unit": "ppbC",
                                "good": 50.0,
                                "mod": 150.0,
                                "unhealthy": 300.0,
                                "stations": {}
                            }
                        
                        # Group by station to sum all compounds and extract detailed lists
                        for (site_num, site_name), station_df in df_date.groupby(['Site Num', 'Local Site Name']):
                            lat = float(station_df.iloc[0].get('Latitude', 0.0))
                            lon = float(station_df.iloc[0].get('Longitude', 0.0))
                            county = station_df.iloc[0].get('County Name', 'Marshall')
                            
                            # Sum all non-null daily average values to calculate Total VOCs
                            mean_vals = station_df['Arithmetic Mean'].dropna()
                            total_sum = float(mean_vals.sum()) if not mean_vals.empty else None
                            
                            # Replicate daily measurement across all 24 hours
                            hourly_data = [total_sum] * 24 if total_sum is not None else [None] * 24
                            
                            # Gather sorted dictionary of individual chemical measurements
                            voc_details = {}
                            for _, row in station_df.iterrows():
                                p_name = row.get('Parameter Name')
                                m_val = row.get('Arithmetic Mean')
                                if not pd.isna(m_val) and p_name:
                                    voc_details[p_name] = float(m_val)
                            
                            # Sort chemical details descending by concentration
                            sorted_vocs = sorted(voc_details.items(), key=lambda x: x[1] if x[1] is not None else 0.0, reverse=True)
                            voc_details_dict = {k: v for k, v in sorted_vocs}
                            
                            station_id = f"CC_{int(site_num)} - {site_name}"
                            regional_monitor_data["VOCs"]["stations"][station_id] = {
                                "county": county,
                                "lat": lat,
                                "lon": lon,
                                "parameter_name": "Total VOCs",
                                "hourly_data": hourly_data,
                                "voc_details": voc_details_dict,
                                "sample_date": closest_date_str,
                                "is_interpolated": days_diff > 0,
                                "days_diff": days_diff
                            }
                        
                        print(f"  Successfully loaded {df_date['Parameter Name'].nunique()} local VOC compounds from sample date {closest_date_str} for target date {self.date_str} (diff: {days_diff}d).")
                    else:
                        print(f"  No local VOC data found in Excel for closest date {closest_date_str}.")
                else:
                    print("  No dates found in Excel.")
            except Exception as e:
                print(f"Error parsing Calvert VOC Excel file: {e}")

        return regional_monitor_data

    def compile_data_for_json(self, raw_particles: Dict[str, Dict[int, List[Dict[str, Any]]]]) -> Dict[str, Any]:
        """
        Compile facilities list and hourly simulation timelines into a JavaScript-friendly structure.
        
        Args:
            raw_particles: Output coordinates from dispersion runs.
            
        Returns:
            Dict containing formatted facility objects and simulation timelines.
        """
        print("\nCompiling trajectory coordinates and EPA data for web layout...")
        self.regional_monitor_data = self.process_ambient_monitors()

        
        # Compile facility variables (merging EPA API/fallback data)
        compiled_facilities = []
        for idx, fac in enumerate(self.facilities):
            tri_data = self.get_facility_releases(fac["name"])
            releases = tri_data.get("releases", [])
            total_lbs = sum(chem.get("total_lbs", 0.0) for chem in releases)
            compiled_facilities.append({
                "id": fac["id"],
                "name": fac["name"],
                "lat": fac["lat"],
                "lon": fac["lon"],
                "height": fac["height"],
                "color": fac["color"],
                "tri_id": fac["tri_id"],
                "tri_name": tri_data.get("fac_name", fac["name"]),
                "chemicals": releases,
                "total_lbs": total_lbs,
                "schedule": fac.get("schedule", "continuous")
            })
            
        # Build internal timeline (used only for wind vector extraction, not serialized)
        timeline = [[] for _ in range(25)]
        
        for fac in self.facilities:
            fac_name = fac["name"]
            fac_data = raw_particles.get(fac_name, {})
            
            for hour_idx, particles in fac_data.items():
                if 0 <= hour_idx <= 24:
                    timeline[hour_idx].extend(particles)
                    
        # Extract per-hour wind grids from particle displacements
        # Each grid is a 2D array of size GRID_SIZE x GRID_SIZE.
        GRID_SIZE = 10
        grid_span = float(WEATHER_BOX_RADIUS_KM) / 111.0
        lat_min = MAP_CENTER[0] - grid_span
        lat_max = MAP_CENTER[0] + grid_span
        lon_min = MAP_CENTER[1] - grid_span
        lon_max = MAP_CENTER[1] + grid_span
        
        lat_span = lat_max - lat_min
        lon_span = lon_max - lon_min
        
        wind_grid = [] # List of 24 grids, grid[hour][row][col] = {"dLat": ..., "dLon": ...}
        
        for hour_idx in range(24):
            curr = timeline[hour_idx]
            nxt = timeline[hour_idx + 1] if hour_idx + 1 <= 24 else []
            
            # Compute global median displacement for this hour as a fallback
            global_dlat = 0.0
            global_dlon = 0.0
            next_map = {}
            if curr and nxt:
                next_map = {(p["facility"], p["id"]): p for p in nxt}
                all_dlats = []
                all_dlons = []
                for p in curr:
                    key = (p["facility"], p["id"])
                    if key in next_map:
                        pn = next_map[key]
                        dl = pn["lat"] - p["lat"]
                        do_ = pn["lon"] - p["lon"]
                        if abs(dl) < 0.5 and abs(do_) < 0.5:
                            all_dlats.append(dl)
                            all_dlons.append(do_)
                if all_dlats:
                    all_dlats.sort()
                    all_dlons.sort()
                    global_dlat = all_dlats[len(all_dlats) // 2]
                    global_dlon = all_dlons[len(all_dlons) // 2]
            
            # Initialize empty grid with global median fallback
            hour_grid = [[{"dLat": round(global_dlat, 6), "dLon": round(global_dlon, 6)} for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
            
            # Group displacements by cell
            cell_displacements = {} # (r, c) -> {"dlats": [], "dlons": []}
            if curr and nxt:
                for p in curr:
                    key = (p["facility"], p["id"])
                    if key in next_map:
                        pn = next_map[key]
                        dl = pn["lat"] - p["lat"]
                        do_ = pn["lon"] - p["lon"]
                        if abs(dl) < 0.5 and abs(do_) < 0.5:
                            # Map coordinate to cell index
                            r = int(((p["lat"] - lat_min) / lat_span) * GRID_SIZE)
                            c = int(((p["lon"] - lon_min) / lon_span) * GRID_SIZE)
                            # Clamp indices to grid boundaries
                            r = max(0, min(GRID_SIZE - 1, r))
                            c = max(0, min(GRID_SIZE - 1, c))
                            
                            cell_key = (r, c)
                            if cell_key not in cell_displacements:
                                cell_displacements[cell_key] = {"dlats": [], "dlons": []}
                            cell_displacements[cell_key]["dlats"].append(dl)
                            cell_displacements[cell_key]["dlons"].append(do_)
            
            # Compute median for each populated cell
            for (r, c), data in cell_displacements.items():
                dlats = sorted(data["dlats"])
                dlons = sorted(data["dlons"])
                local_dlat = dlats[len(dlats) // 2]
                local_dlon = dlons[len(dlons) // 2]
                hour_grid[r][c] = {
                    "dLat": round(local_dlat, 6),
                    "dLon": round(local_dlon, 6)
                }
            
            # Run IDW interpolation for unpopulated cells
            smoothed_grid = [[{"dLat": hour_grid[r][c]["dLat"], "dLon": hour_grid[r][c]["dLon"]} for c in range(GRID_SIZE)] for r in range(GRID_SIZE)]
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    if (r, c) not in cell_displacements:
                        # Find distance-weighted average from cells with particles
                        weights_sum = 0.0
                        dlat_sum = 0.0
                        dlon_sum = 0.0
                        for (pr, pc), pdata in cell_displacements.items():
                            dist = math.sqrt((r - pr)**2 + (c - pc)**2)
                            if dist == 0:
                                continue
                            w = 1.0 / (dist**2)
                            weights_sum += w
                            
                            p_dlats = sorted(pdata["dlats"])
                            p_dlons = sorted(pdata["dlons"])
                            dlat_sum += p_dlats[len(p_dlats) // 2] * w
                            dlon_sum += p_dlons[len(p_dlons) // 2] * w
                        
                        if weights_sum > 0:
                            smoothed_grid[r][c] = {
                                "dLat": round(dlat_sum / weights_sum, 6),
                                "dLon": round(dlon_sum / weights_sum, 6)
                            }
            
            num_cells_filled = len(cell_displacements)
            print(f"  Hour {hour_idx:2d}→{hour_idx+1:2d}: global dLat={global_dlat:+.5f}° dLon={global_dlon:+.5f}°, {num_cells_filled}/{GRID_SIZE*GRID_SIZE} cells populated by particles.")
            wind_grid.append(smoothed_grid)
            
        grid_info = {
            "grid_size": GRID_SIZE,
            "lat_min": round(lat_min, 6),
            "lat_max": round(lat_max, 6),
            "lon_min": round(lon_min, 6),
            "lon_max": round(lon_max, 6)
        }
        
        return {
            "facilities": compiled_facilities,
            "wind_grid": wind_grid,
            "grid_info": grid_info
        }

    def generate_web_visualization(self, master_archive: Dict[str, Any]):
        """
        Write the standalone visualization index.html file with embedded data.
        Ensures strict variable injection matching configuration block values.
        
        Args:
            master_archive: Dictionary of daily plumes and monitors keyed by date string.
        """
        output_path = os.path.join(self.workspace_dir, self.output_html_name)
        print(f"Generating web visualization index.html at: {output_path}...")
        
        # Serialize the simulation data to embed directly in the script template
        archive_json_data = json.dumps(master_archive, indent=2)
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calvert City Industrial Dispersion Prototype</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;800&display=swap" rel="stylesheet">
    
    <!-- Leaflet.js Mapping Engine -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
    
    <style>
        :root {{
            --bg-dark: #0f0f12;
            --panel-bg: rgba(20, 20, 25, 0.72);
            --panel-border: rgba(255, 255, 255, 0.09);
            --text-main: #f9fafb;
            --text-muted: #9ca3af;
            --primary-accent: #3b82f6;
            --primary-accent-glow: rgba(59, 130, 246, 0.35);
            --font-family: 'Inter', system-ui, sans-serif;
            --header-font: 'Outfit', sans-serif;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body, html {{
            width: 100%;
            height: 100%;
            overflow: hidden;
            background-color: var(--bg-dark);
            font-family: var(--font-family);
            color: var(--text-main);
        }}

        #map-viewport {{
            position: relative;
            width: 100vw;
            height: 100vh;
            z-index: 1;
        }}

        #map {{
            width: 100%;
            height: 100%;
            background-color: var(--bg-dark);
        }}

        #particle-canvas {{
            position: absolute;
            pointer-events: none;
        }}

        /* Dark theme Leaflet Popups (removes white border and tip) */
        .leaflet-popup-content-wrapper {{
            background: #121214 !important;
            color: #f3f4f6 !important;
            padding: 0 !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6) !important;
        }}

        .leaflet-popup-content {{
            margin: 0 !important;
            padding: 0 !important;
        }}

        .leaflet-popup-tip {{
            background: #121214 !important;
            border-left: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-top: 1px solid rgba(255, 255, 255, 0.12) !important;
            box-shadow: none !important;
        }}

        .leaflet-popup-close-button {{
            color: #9ca3af !important;
            padding: 8px 8px 0 0 !important;
        }}

        .leaflet-popup-close-button:hover {{
            color: #fff !important;
            background: transparent !important;
        }}

        /* Glassmorphic Panel Design System */
        .glass-panel {{
            background: var(--panel-bg);
            border: 1px solid var(--panel-border);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 16px;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.65),
                        inset 0 1px 0 rgba(255, 255, 255, 0.05);
            color: var(--text-main);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        /* ── Collapsible Panel System ── */
        .panel-topbar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 4px;
        }}

        .panel-collapse-btn {{
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text-muted);
            border-radius: 6px;
            width: 28px;
            height: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 14px;
            line-height: 1;
            transition: all 0.2s ease;
            outline: none;
            flex-shrink: 0;
        }}

        .panel-collapse-btn:hover {{
            background: rgba(255, 255, 255, 0.14);
            border-color: rgba(255, 255, 255, 0.25);
            color: #fff;
            transform: scale(1.1);
        }}

        .panel-body {{
            overflow: hidden;
            transition: max-height 0.35s cubic-bezier(0.4, 0, 0.2, 1),
                        opacity 0.25s ease,
                        padding 0.3s ease;
            max-height: 2000px;
            opacity: 1;
        }}

        .panel-body.collapsed {{
            max-height: 0;
            opacity: 0;
            padding-top: 0;
            padding-bottom: 0;
        }}

        /* Floating restore pills — visible when parent panel is collapsed */
        .panel-restore-pill {{
            position: absolute;
            z-index: 1100;
            display: none;
            align-items: center;
            gap: 6px;
            padding: 8px 14px;
            border-radius: 20px;
            cursor: pointer;
            font-family: var(--font-family);
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            transition: all 0.25s ease;
        }}

        .panel-restore-pill.visible {{
            display: flex;
        }}

        .panel-restore-pill:hover {{
            transform: scale(1.06);
        }}

        #restore-header {{
            top: 24px;
            left: 24px;
            background: var(--panel-bg);
            border: 1px solid var(--panel-border);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            color: #a5b4fc;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
        }}

        #restore-header:hover {{
            background: rgba(30, 30, 38, 0.85);
            box-shadow: 0 8px 28px rgba(59, 130, 246, 0.15);
        }}

        #restore-legend {{
            top: 24px;
            right: 24px;
            background: var(--panel-bg);
            border: 1px solid var(--panel-border);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            color: #a5b4fc;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
        }}

        #restore-legend:hover {{
            background: rgba(30, 30, 38, 0.85);
            box-shadow: 0 8px 28px rgba(59, 130, 246, 0.15);
        }}

        /* Header Panel */
        .hud-header {{
            position: absolute;
            top: 24px;
            left: 24px;
            z-index: 1100;
            padding: 20px 24px;
            width: 380px;
        }}

        .hud-header.panel-hidden {{
            display: none;
        }}

        .hud-header h1 {{
            font-family: var(--header-font);
            font-size: 20px;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 6px;
            background: linear-gradient(135deg, #ffffff 30%, #a5b4fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .hud-header .subtitle {{
            font-size: 12px;
            color: var(--text-muted);
            line-height: 1.4;
        }}

        .hud-header .divider {{
            height: 1px;
            background: rgba(255, 255, 255, 0.08);
            margin: 12px 0;
        }}

        .hud-header .meta-row {{
            display: flex;
            justify-content: space-between;
            font-size: 11px;
        }}

        .hud-header .meta-val {{
            font-weight: 600;
            color: #a5b4fc;
        }}

        /* Bottom Controls HUD */
        .hud-controls {{
            position: absolute;
            bottom: 36px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 1100;
            width: 680px;
            padding: 20px 28px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        .controls-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
        }}

        .time-readout {{
            display: flex;
            align-items: baseline;
            gap: 8px;
            min-width: 140px;
        }}

        .time-val {{
            font-family: var(--header-font);
            font-size: 26px;
            font-weight: 600;
            color: #fff;
            font-variant-numeric: tabular-nums;
        }}

        .time-label {{
            font-size: 11px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .playback-actions {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .btn {{
            background: rgba(255, 255, 255, 0.07);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text-main);
            border-radius: 50%;
            width: 44px;
            height: 44px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s ease;
            outline: none;
        }}

        .btn:hover {{
            background: rgba(255, 255, 255, 0.15);
            border-color: rgba(255, 255, 255, 0.25);
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
            transform: scale(1.05);
        }}

        .btn:active {{
            transform: scale(0.95);
        }}

        .slider-container {{
            flex-grow: 1;
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .slider {{
            -webkit-appearance: none;
            width: 100%;
            height: 6px;
            border-radius: 3px;
            background: rgba(255, 255, 255, 0.12);
            outline: none;
            cursor: pointer;
            transition: background 0.15s ease;
        }}

        .slider::-webkit-slider-thumb {{
            -webkit-appearance: none;
            appearance: none;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #fff;
            cursor: pointer;
            box-shadow: 0 0 8px rgba(0,0,0,0.5);
            transition: transform 0.1s ease;
        }}

        .slider::-webkit-slider-thumb:hover {{
            transform: scale(1.25);
            background: #a5b4fc;
        }}

        /* Speed slider specifics */
        .speed-control {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 11px;
            color: var(--text-muted);
            min-width: 140px;
        }}

        .speed-control select {{
            background: rgba(20, 20, 25, 0.85);
            border: 1px solid var(--panel-border);
            color: var(--text-main);
            padding: 4px 8px;
            border-radius: 6px;
            outline: none;
            cursor: pointer;
            font-family: var(--font-family);
            font-size: 11px;
        }}

        /* Legend Panel */
        .hud-legend {{
            position: absolute;
            top: 24px;
            right: 24px;
            z-index: 1100;
            width: 360px;
            padding: 20px;
            max-height: calc(100vh - 120px);
            display: flex;
            flex-direction: column;
        }}

        .hud-legend.panel-hidden {{
            display: none;
        }}

        #legend-panel-body {{
            display: flex;
            flex-direction: column;
            min-height: 0;
            flex: 1;
        }}

        .legend-title {{
            font-family: var(--header-font);
            font-size: 15px;
            font-weight: 600;
            margin-bottom: 14px;
            letter-spacing: -0.01em;
            color: #fff;
        }}

        .facility-list {{
            display: flex;
            flex-direction: column;
            gap: 12px;
            overflow-y: auto;
            padding-right: 4px;
            flex: 1;
            min-height: 0;
        }}

        .facility-item {{
            border-radius: 10px;
            padding: 10px 12px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.03);
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .facility-item:hover {{
            background: rgba(255, 255, 255, 0.05);
            border-color: rgba(255, 255, 255, 0.08);
        }}

        .facility-item.disabled {{
            opacity: 0.35;
        }}

        .facility-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 6px;
        }}

        .facility-name-row {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .facility-badge {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            box-shadow: 0 0 8px currentColor;
        }}

        .facility-name {{
            font-weight: 600;
            font-size: 13px;
            color: #fff;
        }}

        .toggle-icon {{
            font-size: 10px;
            color: var(--text-muted);
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.05em;
        }}

        .chem-list {{
            display: flex;
            flex-direction: column;
            gap: 4px;
            padding-left: 18px;
            font-size: 11px;
            color: var(--text-muted);
            border-left: 1px solid rgba(255, 255, 255, 0.06);
            margin-top: 4px;
        }}

        .chem-item {{
            display: flex;
            justify-content: space-between;
        }}

        .chem-val {{
            font-weight: 500;
            color: var(--text-main);
        }}

        /* Tooltip style */
        .particle-tooltip {{
            position: absolute;
            z-index: 1200;
            background: rgba(12, 12, 16, 0.92);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 8px;
            padding: 10px 14px;
            color: var(--text-main);
            font-size: 11px;
            pointer-events: none;
            box-shadow: 0 8px 24px rgba(0,0,0,0.6);
            display: none;
            line-height: 1.5;
            backdrop-filter: blur(8px);
        }}

        .tooltip-header {{
            font-weight: 700;
            margin-bottom: 4px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 2px;
            font-family: var(--header-font);
        }}

        /* Map Attribution adjustments */
        .leaflet-control-attribution {{
            background: rgba(0,0,0,0.85) !important;
            color: var(--text-muted) !important;
            font-size: 9px !important;
        }}

        /* Custom Facility Marker DivIcon Overrides */
        .custom-facility-divicon {{
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }}

        /* Enable Text Selection inside Leaflet Popups */
        .leaflet-popup-content, .leaflet-popup-content * {{
            -webkit-user-select: text !important;
            -moz-user-select: text !important;
            -ms-user-select: text !important;
            user-select: text !important;
        }}

        #pollutant-select, #date-picker, #display-mode-select {{
            width: 100%;
            background: rgba(18, 18, 20, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 8px;
            color: #fff;
            font-family: 'Inter', sans-serif;
            font-size: 12px;
            padding: 8px 12px;
            outline: none;
            cursor: pointer;
            transition: all 0.2s ease;
            backdrop-filter: blur(4px);
        }}
        
        #pollutant-select:hover, #date-picker:hover, #display-mode-select:hover {{
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.2);
        }}
        
        #pollutant-select option, #display-mode-select option {{
            background: #121214;
            color: #fff;
        }}

        #date-picker::-webkit-calendar-picker-indicator {{
            filter: invert(1);
            cursor: pointer;
        }}

        /* ── Simulation Sandbox Panel ── */
        .sandbox-section {{
            margin-top: 14px;
        }}

        .sandbox-toggle-btn {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            background: rgba(59, 130, 246, 0.08);
            border: 1px solid rgba(59, 130, 246, 0.18);
            border-radius: 8px;
            padding: 8px 12px;
            cursor: pointer;
            color: #a5b4fc;
            font-family: var(--font-family);
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            transition: all 0.25s ease;
        }}

        .sandbox-toggle-btn:hover {{
            background: rgba(59, 130, 246, 0.15);
            border-color: rgba(59, 130, 246, 0.35);
            box-shadow: 0 0 12px rgba(59, 130, 246, 0.15);
        }}

        .sandbox-toggle-arrow {{
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            font-size: 10px;
        }}

        .sandbox-toggle-arrow.expanded {{
            transform: rotate(180deg);
        }}

        .sandbox-body {{
            display: none;
            flex-direction: column;
            gap: 10px;
            margin-top: 10px;
            padding: 12px;
            background: rgba(10, 10, 14, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 10px;
        }}

        .sandbox-body.open {{
            display: flex;
        }}

        .sandbox-group {{
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}

        .sandbox-label {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 10px;
            color: var(--text-muted);
            font-weight: 600;
            letter-spacing: 0.04em;
        }}

        .sandbox-val {{
            font-weight: 700;
            color: #a5b4fc;
            font-variant-numeric: tabular-nums;
            min-width: 56px;
            text-align: right;
        }}

        .sandbox-slider {{
            -webkit-appearance: none;
            width: 100%;
            height: 5px;
            border-radius: 3px;
            background: rgba(255, 255, 255, 0.1);
            outline: none;
            cursor: pointer;
            transition: background 0.15s ease;
        }}

        .sandbox-slider::-webkit-slider-thumb {{
            -webkit-appearance: none;
            appearance: none;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: linear-gradient(135deg, #818cf8, #6366f1);
            cursor: pointer;
            box-shadow: 0 0 6px rgba(99, 102, 241, 0.5);
            transition: transform 0.12s ease, box-shadow 0.12s ease;
        }}

        .sandbox-slider::-webkit-slider-thumb:hover {{
            transform: scale(1.3);
            box-shadow: 0 0 12px rgba(99, 102, 241, 0.7);
        }}

        .sandbox-slider::-moz-range-thumb {{
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: linear-gradient(135deg, #818cf8, #6366f1);
            cursor: pointer;
            border: none;
            box-shadow: 0 0 6px rgba(99, 102, 241, 0.5);
        }}

        .sandbox-divider {{
            height: 1px;
            background: rgba(255, 255, 255, 0.05);
            margin: 2px 0;
        }}
    </style>
</head>
<body>

    <div id="map-viewport">
        <!-- Leaflet Map Div -->
        <div id="map"></div>
        
        <!-- Overhead Particle Rendering Canvas -->
        <canvas id="particle-canvas"></canvas>
        
        <!-- Floating Restore Pills (visible when panels are collapsed) -->
        <div class="panel-restore-pill" id="restore-header">
            <span>☰</span><span>Controls</span>
        </div>
        <div class="panel-restore-pill" id="restore-legend">
            <span>☰</span><span>Sources</span>
        </div>

        <!-- HUD Header -->
        <div class="hud-header glass-panel" id="hud-header-panel">
            <div class="panel-topbar">
                <h1 style="margin-bottom:0">Calvert City Plume Analysis</h1>
                <button class="panel-collapse-btn" id="collapse-header" title="Minimize Panel">−</button>
            </div>
            <div class="panel-body" id="header-panel-body">
                <div class="subtitle" style="margin-top:4px">Multi-date batch chemical dispersion simulation using hourly NOAA HRRR boundary conditions.</div>
                <div class="divider"></div>
                <div class="meta-row">
                    <div style="display: flex; align-items: center; gap: 4px;">STATE: <span class="meta-val">KENTUCKY</span></div>
                    <div style="display: flex; align-items: center; gap: 4px;">WEATHER: <span class="meta-val">HRRR GRIB2</span></div>
                </div>
                <div class="divider"></div>
                <div style="margin-top: 12px;">
                    <label for="date-picker" style="font-size: 10px; color: var(--text-muted); font-weight: 600; display: block; margin-bottom: 6px; letter-spacing: 0.05em;">SIMULATION DATE</label>
                    <input type="date" id="date-picker">
                </div>
                <div style="margin-top: 12px;">
                    <label for="pollutant-select" style="font-size: 10px; color: var(--text-muted); font-weight: 600; display: block; margin-bottom: 6px; letter-spacing: 0.05em;">EPA AIR QUALITY PARAMETER</label>
                    <select id="pollutant-select">
                        <!-- Javascript populated -->
                    </select>
                </div>
                <div style="margin-top: 12px;">
                    <label for="display-mode-select" style="font-size: 10px; color: var(--text-muted); font-weight: 600; display: block; margin-bottom: 6px; letter-spacing: 0.05em;">PLUME DISPLAY MODE</label>
                    <select id="display-mode-select">
                        <option value="combined" selected>Combined Total Air</option>
                        <option value="stack">Stacks Only</option>
                        <option value="fugitive">Fugitive Only</option>
                    </select>
                </div>

                <!-- ══ Simulation Sandbox Control Panel ══ -->
                <div class="sandbox-section">
                    <button class="sandbox-toggle-btn" id="sandbox-toggle" type="button">
                        <span>⚙ Simulation Sandbox</span>
                        <span class="sandbox-toggle-arrow" id="sandbox-arrow">▼</span>
                    </button>
                    <div class="sandbox-body" id="sandbox-body">

                        <!-- Plume Density Multiplier -->
                        <div class="sandbox-group">
                            <div class="sandbox-label">
                                <span>PLUME DENSITY MULTIPLIER</span>
                                <span class="sandbox-val" id="densityVal">1.0×</span>
                            </div>
                            <input type="range" class="sandbox-slider" id="densitySlider"
                                   min="0.1" max="5.0" step="0.1" value="1.0">
                        </div>

                        <!-- Particle Lifespan -->
                        <div class="sandbox-group">
                            <div class="sandbox-label">
                                <span>PARTICLE LIFESPAN</span>
                                <span class="sandbox-val" id="lifespanVal">{MAX_PARTICLE_AGE_MINUTES} min</span>
                            </div>
                            <input type="range" class="sandbox-slider" id="lifespanSlider"
                                   min="30" max="240" step="10" value="{MAX_PARTICLE_AGE_MINUTES}">
                        </div>

                        <!-- Particle Size -->
                        <div class="sandbox-group">
                            <div class="sandbox-label">
                                <span>PARTICLE SIZE</span>
                                <span class="sandbox-val" id="sizeVal">{BASE_PARTICLE_RADIUS_PIXELS}px</span>
                            </div>
                            <input type="range" class="sandbox-slider" id="sizeSlider"
                                   min="1" max="10" step="0.5" value="{BASE_PARTICLE_RADIUS_PIXELS}">
                        </div>

                        <div class="sandbox-divider"></div>

                        <!-- Stack Particle Opacity -->
                        <div class="sandbox-group">
                            <div class="sandbox-label">
                                <span>STACK PARTICLE OPACITY</span>
                                <span class="sandbox-val" id="stackOpacityVal">0.70</span>
                            </div>
                            <input type="range" class="sandbox-slider" id="stackOpacitySlider"
                                   min="0.05" max="1.0" step="0.05" value="0.70">
                        </div>

                        <!-- Fugitive Particle Opacity -->
                        <div class="sandbox-group">
                            <div class="sandbox-label">
                                <span>FUGITIVE PARTICLE OPACITY</span>
                                <span class="sandbox-val" id="fugitiveOpacityVal">0.70</span>
                            </div>
                            <input type="range" class="sandbox-slider" id="fugitiveOpacitySlider"
                                   min="0.05" max="1.0" step="0.05" value="0.70">
                        </div>

                    </div>
                </div>
            </div>
        </div>

        <!-- Legend and Toggles -->
        <div class="hud-legend glass-panel" id="hud-legend-panel">
            <div class="panel-topbar">
                <div class="legend-title" style="margin-bottom:0">Industrial Point Sources</div>
                <button class="panel-collapse-btn" id="collapse-legend" title="Minimize Panel">−</button>
            </div>
            <div class="panel-body" id="legend-panel-body">
                <div class="facility-list" id="facility-legend">
                    <!-- Javascript populated -->
                </div>
            </div>
        </div>

        <!-- Controls HUD -->
        <div class="hud-controls glass-panel">
            <div class="controls-row">
                <div class="time-readout">
                    <span class="time-val" id="time-display">12:00</span>
                    <span class="time-label" id="ampm-display">AM</span>
                </div>
                
                <div class="slider-container">
                    <span style="font-size:10px; color:var(--text-muted)">00:00</span>
                    <input type="range" min="0.0" max="24.0" step="0.01" value="0.0" class="slider" id="time-slider">
                    <span style="font-size:10px; color:var(--text-muted)">24:00</span>
                </div>
            </div>
            
            <div class="controls-row" style="margin-top: 4px;">
                <div class="playback-actions">
                    <button class="btn" id="play-btn" title="Play/Pause">
                        <!-- Play Icon -->
                        <svg id="play-icon" width="14" height="16" viewBox="0 0 14 16" fill="none" style="display:none;">
                            <path d="M13 8L1 1V15L13 8Z" fill="white" stroke="white" stroke-width="2" stroke-linejoin="round"/>
                        </svg>
                        <!-- Pause Icon -->
                        <svg id="pause-icon" width="12" height="16" viewBox="0 0 12 16" fill="none">
                            <path d="M1 1V15M11 1V15" stroke="white" stroke-width="3" stroke-linecap="round"/>
                        </svg>
                    </button>
                    <button class="btn" id="restart-btn" title="Restart Simulation">
                        <!-- Restart SVG -->
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/>
                            <path d="M21 3v5h-5"/>
                        </svg>
                    </button>
                </div>
                
                <div class="speed-control">
                    <span>PLAYBACK SPEED:</span>
                    <select id="speed-select">
                        <option value="1">1 Hour/Min</option>
                        <option value="2" selected>5 Hours/Min</option>
                        <option value="3">10 Hours/Min</option>
                        <option value="4">30 Hours/Min</option>
                        <option value="5">60 Hours/Min</option>
                    </select>
                </div>
                
                <div style="font-size: 11px; color: var(--text-muted)">
                    ACTIVE PARTICLES: <span id="active-count" style="font-weight:600; color:#fff">0</span>
                </div>
            </div>
        </div>
        
        <!-- Interactive Tooltip Overlay -->
        <div class="particle-tooltip" id="tooltip">
            <div class="tooltip-header" id="tooltip-title">Facility</div>
            <div id="tooltip-body">Coords</div>
        </div>
    </div>

    <!-- Data Injection Block -->
    <script>
        const historicalSimulationArchive = {archive_json_data};
    </script>

    <!-- UI and Rendering Engine Script -->
    <script>
        // Active date and data states
        let activeDate = "{START_DATE}";
        let PLUME_DATA = historicalSimulationArchive[activeDate].plumes;
        let regionalMonitorData = historicalSimulationArchive[activeDate].monitors;

        // Leaflet Map Initialization
        const map = L.map('map', {{
            zoomControl: false,
            maxZoom: 16,
            minZoom: 11
        }}).setView([{MAP_CENTER[0]}, {MAP_CENTER[1]}], {MAP_ZOOM_LEVEL});
        
        // CartoDB Dark Matter tile layer
        L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 20
        }}).addTo(map);
        
        // Custom control layout placement
        L.control.zoom({{
            position: 'bottomright'
        }}).addTo(map);

        // Stop propagation of mousedown and touchstart inside Leaflet popups
        // to prevent Leaflet from intercepting drag events and disabling selection.
        document.addEventListener('mousedown', function(e) {{
            if (e.target.closest('.leaflet-popup')) {{
                e.stopPropagation();
            }}
        }}, true);
        document.addEventListener('touchstart', function(e) {{
            if (e.target.closest('.leaflet-popup')) {{
                e.stopPropagation();
            }}
        }}, true);

        // --- EPA MONITORING LAYERS ---
        const activeMonitorLayer = L.layerGroup().addTo(map);
        const monitorMarkers = [];

        // Populate monitor markers for all unique stations across all dates
        const uniqueStations = {{}};
        Object.keys(historicalSimulationArchive).forEach(dateStr => {{
            const dayMonitors = historicalSimulationArchive[dateStr].monitors;
            Object.keys(dayMonitors).forEach(pollutant => {{
                const pData = dayMonitors[pollutant];
                const stations = pData.stations || {{}};
                
                Object.keys(stations).forEach(stationId => {{
                    const station = stations[stationId];
                    const key = pollutant + "_" + stationId;
                    if (!uniqueStations[key]) {{
                        uniqueStations[key] = {{
                            pollutant: pollutant,
                            stationId: stationId,
                            lat: station.lat,
                            lon: station.lon,
                            unit: pData.unit
                        }};
                    }}
                }});
            }});
        }});

        // Build leaflet markers from the unique stations list
        Object.keys(uniqueStations).forEach(key => {{
            const info = uniqueStations[key];
            const marker = L.circleMarker([info.lat, info.lon], {{
                radius: 8,
                fillColor: '#808080',
                color: '#ffffff',
                weight: 2,
                opacity: 0.9,
                fillOpacity: 0.8
            }});

            marker.bindPopup('', {{
                className: 'custom-leaflet-popup'
            }});

            monitorMarkers.push({{
                marker: marker,
                pollutant: info.pollutant,
                stationId: info.stationId,
                unit: info.unit
            }});
        }});

        // Populate pollutant select dropdown
        const pollutantSelect = document.getElementById('pollutant-select');
        Object.keys(regionalMonitorData).forEach(pollutant => {{
            const opt = document.createElement('option');
            opt.value = pollutant;
            opt.textContent = pollutant;
            pollutantSelect.appendChild(opt);
        }});

        // Configure Date Picker
        const datePicker = document.getElementById('date-picker');
        datePicker.min = "{START_DATE}";
        datePicker.max = "{END_DATE}";
        datePicker.value = activeDate;

        function syncActiveMonitorLayer(selectedPollutant) {{
            activeMonitorLayer.clearLayers();
            monitorMarkers.forEach(m => {{
                if (m.pollutant === selectedPollutant) {{
                    m.marker.addTo(activeMonitorLayer);
                }}
            }});
        }}

        // Initialize with default pollutant
        const defaultPollutant = regionalMonitorData['VOCs'] ? 'VOCs' : (Object.keys(regionalMonitorData)[0] || 'PM2.5');
        pollutantSelect.value = defaultPollutant;
        syncActiveMonitorLayer(defaultPollutant);

        pollutantSelect.addEventListener('change', (e) => {{
            const selected = e.target.value;
            syncActiveMonitorLayer(selected);
            let currentHourInt = Math.floor(playbackTime);
            if (currentHourInt < 0) currentHourInt = 0;
            if (currentHourInt > 23) currentHourInt = 23;
            updateMonitorPopups(currentHourInt);
        }});

        // Date Picker Change Event Listener
        datePicker.addEventListener('change', (e) => {{
            const selectedDate = e.target.value;
            const activeDayData = historicalSimulationArchive[selectedDate];
            if (!activeDayData) return;

            // Pause playback
            isPlaying = false;
            document.getElementById('play-icon').style.display = 'block';
            document.getElementById('pause-icon').style.display = 'none';

            // Hot-swap data layers
            activeDate = selectedDate;
            PLUME_DATA = activeDayData.plumes;
            regionalMonitorData = activeDayData.monitors;

            // Reset simulation timeline
            playbackTime = 0.0;
            prevPlaybackTime = 0.0;
            particles = [];
            lastSpawnTime = -999;

            // Update UI components
            updateHUD();
            PLUME_DATA.facilities.forEach(fac => {{
                updateFacilityPopup(fac.id);
            }});
            drawParticles();
        }});

        function getMonitorColorAndStatus(val, thresholds) {{
            if (val === null || val === undefined) {{
                return {{ color: '#808080', status: 'No Data' }};
            }}
            if (val <= thresholds.good) {{
                return {{ color: '#10B981', status: 'Good' }};
            }} else if (val <= thresholds.mod) {{
                return {{ color: '#F59E0B', status: 'Moderate' }};
            }} else if (val <= thresholds.unhealthy) {{
                return {{ color: '#EF4444', status: 'Unhealthy' }};
            }} else {{
                return {{ color: '#8B5CF6', status: 'Very Unhealthy' }};
            }}
        }}

        function updateMonitorPopups(currentHourInt) {{
            const selected = document.getElementById('pollutant-select').value;
            monitorMarkers.forEach(m => {{
                if (m.pollutant !== selected) return;

                const thresholds = {{
                    good: regionalMonitorData[m.pollutant].good,
                    mod: regionalMonitorData[m.pollutant].mod,
                    unhealthy: regionalMonitorData[m.pollutant].unhealthy
                }};
                
                const station = regionalMonitorData[m.pollutant].stations[m.stationId];
                if (!station) {{
                    m.marker.setStyle({{
                        fillColor: '#808080'
                    }});
                    m.marker.setPopupContent('<div style="font-family:Inter,sans-serif;font-size:11px;color:#fff;padding:6px;">No data for this station on this day.</div>');
                    return;
                }}

                const val = station.hourly_data[currentHourInt];
                const {{ color, status }} = getMonitorColorAndStatus(val, thresholds);
                
                m.marker.setStyle({{
                    fillColor: color
                }});

                const valStr = (val !== null && val !== undefined) ? (val.toFixed(2) + ' ' + m.unit) : 'No Data';

                let sampleDateRow = '';
                let measuredVocHeader = 'Measured VOC Compounds (' + m.unit + '):';
                if (station.sample_date) {{
                    const statusText = station.is_interpolated ? ` (${{station.days_diff}}d nearest)` : ' (Actual)';
                    const colorStyle = station.is_interpolated ? 'color: #F59E0B;' : 'color: #10B981;';
                    sampleDateRow = 
                        '<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">' +
                            '<td style="padding: 4px 0; color: #9ca3af;">Sample Date:</td>' +
                            '<td style="padding: 4px 0; font-weight: 600; text-align: right; ' + colorStyle + '">' + station.sample_date + statusText + '</td>' +
                        '</tr>';
                    
                    if (station.is_interpolated) {{
                        measuredVocHeader = 'Measured VOC Compounds (' + m.unit + ' - Sampled ' + station.sample_date + '):';
                    }}
                }}

                const popupContent = 
                    '<div style="font-family: Inter, sans-serif; font-size: 12px; color: #f3f4f6; width: 260px; background: #121214; padding: 10px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);">' +
                        '<strong style="color: #a5b4fc; font-size: 14px; font-family: Outfit, sans-serif;">EPA Ambient Monitor</strong>' +
                        '<div style="height: 1px; background: rgba(255,255,255,0.08); margin: 8px 0;"></div>' +
                        '<table style="width: 100%; border-collapse: collapse; font-size: 11px; color: #d1d5db;">' +
                            '<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">' +
                                '<td style="padding: 4px 0; color: #9ca3af;">Station ID:</td>' +
                                '<td style="padding: 4px 0; font-weight: 600; text-align: right; color: #fff;">' + m.stationId + '</td>' +
                            '</tr>' +
                            '<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">' +
                                '<td style="padding: 4px 0; color: #9ca3af;">County:</td>' +
                                '<td style="padding: 4px 0; font-weight: 600; text-align: right; color: #fff;">' + station.county + '</td>' +
                            '</tr>' +
                            '<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">' +
                                '<td style="padding: 4px 0; color: #9ca3af;">Coordinates:</td>' +
                                '<td style="padding: 4px 0; font-weight: 600; text-align: right; color: #fff;">' + station.lat.toFixed(4) + ', ' + station.lon.toFixed(4) + '</td>' +
                            '</tr>' +
                            '<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">' +
                                '<td style="padding: 4px 0; color: #9ca3af;">Parameter:</td>' +
                                '<td style="padding: 4px 0; font-weight: 600; text-align: right; color: #fff; max-width: 150px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="' + station.parameter_name + '">' + station.parameter_name + '</td>' +
                            '</tr>' +
                            sampleDateRow +
                            '<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">' +
                                '<td style="padding: 4px 0; color: #9ca3af;">Active Hour:</td>' +
                                '<td style="padding: 4px 0; font-weight: 600; text-align: right; color: #fff;">' + String(currentHourInt).padStart(2, '0') + ':00</td>' +
                            '</tr>' +
                            '<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">' +
                                '<td style="padding: 4px 0; color: #9ca3af;">Value:</td>' +
                                '<td style="padding: 4px 0; font-weight: 600; text-align: right; color: #fff;">' + valStr + '</td>' +
                            '</tr>' +
                            '<tr' + (station.voc_details ? ' style="border-bottom: 1px solid rgba(255,255,255,0.05);"' : '') + '>' +
                                '<td style="padding: 4px 0; color: #9ca3af;">Classification:</td>' +
                                '<td style="padding: 4px 0; font-weight: 700; text-align: right; color: ' + color + ';">' + status + '</td>' +
                            '</tr>' +
                        '</table>' +
                        (station.voc_details ? 
                            ('<div style="margin-top: 8px; border-top: 1px dashed rgba(255,255,255,0.15); padding-top: 8px;">' +
                                '<strong style="color: #a5b4fc; font-size: 11px; display: block; margin-bottom: 6px;">' + measuredVocHeader + '</strong>' +
                                '<div style="max-height: 120px; overflow-y: auto; font-size: 10px; padding-right: 4px;">' +
                                Object.keys(station.voc_details).map(compound => {{
                                    const cVal = station.voc_details[compound];
                                    const cValStr = cVal !== null ? cVal.toFixed(3) : 'N/A';
                                    return '<div style="display: flex; justify-content: space-between; margin-bottom: 3px; border-bottom: 1px solid rgba(255,255,255,0.02); padding-bottom: 1px;">' +
                                               '<span style="color: #9ca3af; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 170px;" title="' + compound + '">' + compound + ':</span>' +
                                               '<span style="font-weight: 600; color: #fff;">' + cValStr + '</span>' +
                                           '</div>';
                                }}).join('') +
                                '</div>' +
                            '</div>') : '') +
                    '</div>';

                m.marker.setPopupContent(popupContent);

                if (m.marker.isPopupOpen()) {{
                    m.marker.getPopup().setContent(popupContent);
                }}
            }});
        }}

        // State variables
        let isPlaying = true;
        let playbackTime = 0.0; // simulation hour index (0.0 to 24.0)
        let activeFacilities = new Array(PLUME_DATA.facilities.length).fill(true); // boolean array for toggles
        let activeChemicals = {{}}; // nested object for chemical checkbox toggles
        
        // Canvas Setup
        const canvas = document.getElementById('particle-canvas');
        const ctx = canvas.getContext('2d');
        
        // Move canvas inside leaflet's overlay pane so it sits behind popups (which are in popupPane)
        map.getPanes().overlayPane.appendChild(canvas);
        
        function resizeCanvas() {{
            const size = map.getSize();
            canvas.width = size.x;
            canvas.height = size.y;
            
            const topLeft = map.containerPointToLayerPoint([0, 0]);
            canvas.style.position = 'absolute';
            canvas.style.left = topLeft.x + 'px';
            canvas.style.top = topLeft.y + 'px';
        }}
        resizeCanvas();
        
        // Helper formatting functions
        function formatSimulationTime(decHours) {{
            const totalMinutes = Math.floor(decHours * 60);
            const hours24 = Math.floor(totalMinutes / 60);
            const minutes = totalMinutes % 60;
            
            const hours12 = hours24 % 12 === 0 ? 12 : hours24 % 12;
            const ampm = hours24 >= 12 ? 'PM' : 'AM';
            
            const timeStr = `${{String(hours12).padStart(2, '0')}}:${{String(minutes).padStart(2, '0')}}`;
            return {{ time: timeStr, ampm: ampm }};
        }}
        
        function hexToRgbA(hex, opacity) {{
            if (!hex || hex.indexOf('#') !== 0) return 'rgba(255,255,255,' + opacity + ')';
            let c = hex.substring(1);
            if (c.length === 3) {{
                c = c.split('').map(x => x + x).join('');
            }}
            if (c.length === 6) {{
                const r = parseInt(c.substring(0, 2), 16);
                const g = parseInt(c.substring(2, 4), 16);
                const b = parseInt(c.substring(4, 6), 16);
                return 'rgba(' + r + ',' + g + ',' + b + ',' + opacity + ')';
            }}
            return 'rgba(255,255,255,' + opacity + ')';
        }}

        // Draw static facilities markers and setup facilityMarkers global dictionary
        const facilityMarkers = {{}};

        function updateFacilityPopup(facId) {{
            const fac = PLUME_DATA.facilities.find(f => f.id === facId);
            const marker = facilityMarkers[facId];
            if (!fac || !marker) return;
            
            let active_stack_total = 0;
            let active_fugitive_total = 0;
            let active_total = 0;
            
            let chemHtml = '';
            fac.chemicals.forEach(c => {{
                const isActive = activeChemicals[facId][c.chemical];
                if (isActive) {{
                    active_stack_total += c.stack_lbs || 0;
                    active_fugitive_total += c.fugitive_lbs || 0;
                    active_total += c.total_lbs || 0;
                    
                    chemHtml += `<div style="display:flex; justify-content:space-between; gap:10px; margin-top:2px;">
                        <span style="color:#9ca3af">${{c.chemical}}:</span>
                        <span style="font-weight:600; color:#fff">${{c.total_lbs.toLocaleString()}} lbs/yr</span>
                    </div>`;
                }} else {{
                    chemHtml += `<div style="display:flex; justify-content:space-between; gap:10px; margin-top:2px; opacity:0.4;">
                        <span style="color:#9ca3af; text-decoration: line-through;">${{c.chemical}}:</span>
                        <span style="font-weight:600; color:#9ca3af">0.0 lbs</span>
                    </div>`;
                }}
            }});
            
            const totalText = active_total === 0 ? '0.0 lbs' : active_total.toLocaleString(undefined, {{maximumFractionDigits: 1}}) + ' lbs/yr';
            const stackText = active_stack_total === 0 ? '0.0 lbs' : active_stack_total.toLocaleString(undefined, {{maximumFractionDigits: 1}}) + ' lbs/yr';
            const fugitiveText = active_fugitive_total === 0 ? '0.0 lbs' : active_fugitive_total.toLocaleString(undefined, {{maximumFractionDigits: 1}}) + ' lbs/yr';
            
            const popupContent = `
                <div style="font-family:'Inter',sans-serif; font-size:12px; color:#f3f4f6; width:240px; background:#121214; padding:6px; border-radius:8px;">
                    <strong style="color:${{fac.color}}; font-size:13px;">${{fac.name}}</strong><br/>
                    <span style="font-size:11px; color:#9b9b9b;">TRI ID: ${{fac.tri_id}}</span>
                    <div style="height:1px; background:#2e2e2e; margin:6px 0;"></div>
                    <div style="font-weight:600; color:#a5b4fc; margin-bottom:4px;">Active Source Strength:</div>
                    <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:2px;">
                        <span style="color:#9ca3af">Active Stack:</span>
                        <span style="font-weight:600; color:#fff">${{stackText}}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:4px;">
                        <span style="color:#9ca3af">Active Fugitive:</span>
                        <span style="font-weight:600; color:#fff">${{fugitiveText}}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; font-size:11px; font-weight:700; border-top:1px dashed #2e2e2e; padding-top:4px; margin-bottom:6px;">
                        <span style="color:#a5b4fc">Active Combined:</span>
                        <span style="color:#a5b4fc">${{totalText}}</span>
                    </div>
                    <div style="height:1px; background:#2e2e2e; margin:6px 0;"></div>
                    <span style="font-weight:500; font-size:11px; color:#a5b4fc;">Annual Chemical Releases:</span>
                    ${{chemHtml}}
                </div>
            `;
            
            marker.bindPopup(popupContent, {{
                className: 'custom-leaflet-popup'
            }});
            
            if (marker.isPopupOpen()) {{
                marker.getPopup().setContent(popupContent);
            }}
        }}

        PLUME_DATA.facilities.forEach(fac => {{
            const squareIcon = L.divIcon({{
                className: 'custom-facility-divicon',
                html: `<div style="background-color: ${{fac.color}}; border: 1.5px solid #ffffff; width: 10px; height: 10px; box-shadow: 0 0 4px rgba(0,0,0,0.5);"></div>`,
                iconSize: [13, 13],
                iconAnchor: [6.5, 6.5]
            }});
            const marker = L.marker([fac.lat, fac.lon], {{
                icon: squareIcon
            }}).addTo(map);
            
            facilityMarkers[fac.id] = marker;
        }});

        // Legend construction with collapsible dropdowns and total lbs display
        const legendContainer = document.getElementById('facility-legend');
        PLUME_DATA.facilities.forEach(fac => {{
            // Initialize active chemical states for this facility based on defaultActive
            activeChemicals[fac.id] = {{}};
            fac.chemicals.forEach(c => {{
                activeChemicals[fac.id][c.chemical] = c.defaultActive;
            }});

            const item = document.createElement('div');
            item.className = 'facility-item';
            item.dataset.id = fac.id;
            
            let chemHtml = '';
            fac.chemicals.forEach(c => {{
                const isChecked = c.defaultActive ? 'checked' : '';
                chemHtml += `
                    <div class="chem-item" style="margin-bottom: 4px; display: flex; align-items: center; justify-content: space-between; gap: 8px;">
                        <label style="display: flex; align-items: center; gap: 6px; cursor: pointer; font-size: 11px; color: #d1d5db; user-select: none; min-width: 0; flex: 1;">
                            <input type="checkbox" ${{isChecked}} class="chem-chk" data-fac="${{fac.id}}" data-chem="${{c.chemical}}" style="accent-color: ${{fac.color}}; cursor: pointer; flex-shrink: 0;" />
                            <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${{c.chemical}}</span>
                        </label>
                        <span class="chem-val" style="white-space: nowrap; margin-left: 10px; font-size: 11px; color: var(--text-muted);">${{c.total_lbs.toLocaleString()}} lbs/yr</span>
                    </div>`;
            }});
            
            const totalLbsFormatted = fac.total_lbs ? fac.total_lbs.toLocaleString(undefined, {{maximumFractionDigits: 1}}) : "0";
            
            item.innerHTML = `
                <div class="facility-header" style="display: flex; align-items: center; justify-content: space-between; gap: 8px;">
                    <div class="facility-left-section" style="display: flex; align-items: center; gap: 8px; flex: 1; min-width: 0;">
                        <span class="facility-badge" style="color:${{fac.color}}; background-color:${{fac.color}}; flex-shrink: 0;"></span>
                        <div class="facility-info" style="min-width: 0; display: flex; flex-direction: column;">
                            <span class="facility-name" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${{fac.name}}</span>
                            <span class="facility-total-lbs" id="total-lbs-${{fac.id}}" style="font-size: 11px; color: var(--text-muted); font-weight: 500; margin-top: 1px;">
                                ${{totalLbsFormatted}} lbs/yr
                            </span>
                        </div>
                    </div>
                    <div class="facility-actions" style="display: flex; align-items: center; gap: 8px; flex-shrink: 0;">
                        <span class="toggle-icon" id="toggle-lbl-${{fac.id}}" style="padding: 4px 6px; border-radius: 4px; font-size: 9px; cursor: pointer; transition: all 0.2s; color: #10B981; background: rgba(16, 185, 129, 0.1); font-weight: 700; letter-spacing: 0.05em;">VISIBLE</span>
                        <span class="dropdown-arrow" id="arrow-${{fac.id}}" style="font-size: 11px; transition: transform 0.2s; padding: 4px; cursor: pointer; color: var(--text-muted);">▼</span>
                    </div>
                </div>
                <div class="chem-list" id="chem-list-${{fac.id}}" style="display: none; flex-direction: column; margin-top: 10px; border-top: 1px solid rgba(255, 255, 255, 0.05); padding-top: 8px;">
                    ${{chemHtml}}
                </div>
            `;
            
            const toggleBtn = item.querySelector(`#toggle-lbl-${{fac.id}}`);
            const chemList = item.querySelector(`#chem-list-${{fac.id}}`);
            const arrow = item.querySelector(`#arrow-${{fac.id}}`);
            
            // Particle visibility toggle
            toggleBtn.addEventListener('click', (e) => {{
                e.stopPropagation(); // Prevent dropdown expansion
                activeFacilities[fac.id] = !activeFacilities[fac.id];
                if (activeFacilities[fac.id]) {{
                    item.classList.remove('disabled');
                    toggleBtn.textContent = 'VISIBLE';
                    toggleBtn.style.color = '#10B981';
                    toggleBtn.style.background = 'rgba(16, 185, 129, 0.1)';
                }} else {{
                    item.classList.add('disabled');
                    toggleBtn.textContent = 'HIDDEN';
                    toggleBtn.style.color = 'var(--text-muted)';
                    toggleBtn.style.background = 'rgba(255, 255, 255, 0.05)';
                }}
                drawParticles();
            }});
            
            // Chemical checkbox toggles
            item.querySelectorAll('.chem-chk').forEach(chk => {{
                chk.addEventListener('change', (e) => {{
                    const facId = parseInt(chk.dataset.fac);
                    const chemName = chk.dataset.chem;
                    activeChemicals[facId][chemName] = chk.checked;
                    
                    // Filter out existing particles of this chemical from map immediately
                    if (!chk.checked) {{
                        particles = particles.filter(p => p.fac !== facId || p.chem !== chemName);
                    }}
                    
                    // Recalculate totals
                    const facObj = PLUME_DATA.facilities.find(f => f.id === facId);
                    let active_total = 0;
                    facObj.chemicals.forEach(c => {{
                        if (activeChemicals[facId][c.chemical]) {{
                            active_total += c.total_lbs || 0;
                        }}
                    }});
                    
                    // Update sidebar total
                    const totalLbsLabel = document.getElementById('total-lbs-' + facId);
                    if (totalLbsLabel) {{
                        totalLbsLabel.textContent = active_total === 0 ? '0.0 lbs' : active_total.toLocaleString(undefined, {{maximumFractionDigits: 1}}) + ' lbs/yr';
                    }}
                    
                    // Update Leaflet popup content
                    updateFacilityPopup(facId);
                    
                    drawParticles();
                }});
                chk.addEventListener('click', (e) => {{
                    e.stopPropagation(); // Prevent dropdown collapse/expand
                }});
            }});
            
            // Chemical dropdown toggle
            item.addEventListener('click', () => {{
                const isExpanded = chemList.style.display !== 'none';
                if (isExpanded) {{
                    chemList.style.display = 'none';
                    arrow.style.transform = 'rotate(0deg)';
                }} else {{
                    chemList.style.display = 'flex';
                    arrow.style.transform = 'rotate(180deg)';
                }}
            }});
            
            legendContainer.appendChild(item);
            
            // Initialize popups and sidebar labels
            updateFacilityPopup(fac.id);
            
            let initial_active_total = 0;
            fac.chemicals.forEach(c => {{
                if (activeChemicals[fac.id][c.chemical]) {{
                    initial_active_total += c.total_lbs || 0;
                }}
            }});
            const totalLbsLabel = document.getElementById('total-lbs-' + fac.id);
            if (totalLbsLabel) {{
                totalLbsLabel.textContent = initial_active_total === 0 ? '0.0 lbs' : initial_active_total.toLocaleString(undefined, {{maximumFractionDigits: 1}}) + ' lbs/yr';
            }}
        }});

        // Plume Display Mode select event listener
        document.getElementById('display-mode-select').addEventListener('change', () => {{
            const displayMode = document.getElementById('display-mode-select').value;
            if (displayMode === 'stack') {{
                particles = particles.filter(p => p.type === 'stack');
            }} else if (displayMode === 'fugitive') {{
                particles = particles.filter(p => p.type === 'fugitive');
            }}
            drawParticles();
        }});

        // ================================================================
        // CLIENT-SIDE CONTINUOUS PARTICLE SYSTEM
        // ================================================================
        
        // Sandbox slider live-read helpers (replace hardcoded constants)
        function getSandboxLifespan() {{
            const el = document.getElementById('lifespanSlider');
            return el ? parseFloat(el.value) : {MAX_PARTICLE_AGE_MINUTES};
        }}
        function getSandboxSize() {{
            const el = document.getElementById('sizeSlider');
            return el ? parseFloat(el.value) : {BASE_PARTICLE_RADIUS_PIXELS};
        }}
        function getSandboxDensity() {{
            const el = document.getElementById('densitySlider');
            return el ? parseFloat(el.value) : 1.0;
        }}
        function getSandboxStackOpacity() {{
            const el = document.getElementById('stackOpacitySlider');
            return el ? parseFloat(el.value) : 0.70;
        }}
        function getSandboxFugitiveOpacity() {{
            const el = document.getElementById('fugitiveOpacitySlider');
            return el ? parseFloat(el.value) : 0.70;
        }}

        const MAX_ACTIVE = 4000;                // Global particle cap
        const SPAWN_INTERVAL = 1.0 / 30.0;     // Spawn every 2 sim-minutes
        const BASE_SPAWN_COUNT = 5;             // Particles per spawn for biggest emitter
        const TURB_BASE = 0.004;                // Base turbulent diffusion (deg/hr)
        const TURB_GROWTH = 0.006;              // Extra diffusion per hour of age
        
        // Find max emissions for proportional spawning
        const maxFacLbs = Math.max(...PLUME_DATA.facilities.map(f => f.total_lbs || 1), 1);
        
        let particles = [];
        let lastSpawnTime = -999;
        let prevPlaybackTime = playbackTime;

        // ── Sandbox UI wiring ──
        (function initSandbox() {{
            const toggle = document.getElementById('sandbox-toggle');
            const body = document.getElementById('sandbox-body');
            const arrow = document.getElementById('sandbox-arrow');
            toggle.addEventListener('click', () => {{
                const open = body.classList.toggle('open');
                arrow.classList.toggle('expanded', open);
            }});

            // Wire each slider to its value display
            const wirings = [
                {{ slider: 'densitySlider',         display: 'densityVal',         fmt: v => v.toFixed(1) + '×' }},
                {{ slider: 'lifespanSlider',        display: 'lifespanVal',        fmt: v => v.toFixed(0) + ' min' }},
                {{ slider: 'sizeSlider',            display: 'sizeVal',            fmt: v => v.toFixed(1) + 'px' }},
                {{ slider: 'stackOpacitySlider',    display: 'stackOpacityVal',    fmt: v => v.toFixed(2) }},
                {{ slider: 'fugitiveOpacitySlider', display: 'fugitiveOpacityVal', fmt: v => v.toFixed(2) }}
            ];
            wirings.forEach(({{ slider, display, fmt }}) => {{
                const sl = document.getElementById(slider);
                const dp = document.getElementById(display);
                if (sl && dp) {{
                    sl.addEventListener('input', () => {{ dp.textContent = fmt(parseFloat(sl.value)); }});
                }}
            }});
        }})();

        // ── Collapsible Panel Toggle System ──
        (function initPanelToggles() {{
            // Left Controls panel
            const headerPanel = document.getElementById('hud-header-panel');
            const headerBody = document.getElementById('header-panel-body');
            const collapseHeader = document.getElementById('collapse-header');
            const restoreHeader = document.getElementById('restore-header');

            collapseHeader.addEventListener('click', () => {{
                headerPanel.classList.add('panel-hidden');
                restoreHeader.classList.add('visible');
            }});
            restoreHeader.addEventListener('click', () => {{
                headerPanel.classList.remove('panel-hidden');
                restoreHeader.classList.remove('visible');
            }});

            // Right Legend/Sources panel
            const legendPanel = document.getElementById('hud-legend-panel');
            const legendBody = document.getElementById('legend-panel-body');
            const collapseLegend = document.getElementById('collapse-legend');
            const restoreLegend = document.getElementById('restore-legend');

            collapseLegend.addEventListener('click', () => {{
                legendPanel.classList.add('panel-hidden');
                restoreLegend.classList.add('visible');
            }});
            restoreLegend.addEventListener('click', () => {{
                legendPanel.classList.remove('panel-hidden');
                restoreLegend.classList.remove('visible');
            }});
        }})();
        
        // ── Wind vector interpolation ──
        const gridInfo = PLUME_DATA.grid_info;
        const GRID_SIZE = gridInfo.grid_size;
        const latMin = gridInfo.lat_min;
        const latMax = gridInfo.lat_max;
        const lonMin = gridInfo.lon_min;
        const lonMax = gridInfo.lon_max;
        const latSpan = latMax - latMin;
        const lonSpan = lonMax - lonMin;

        function interpolateGrid(grid, lat, lon) {{
            let clampedLat = Math.max(latMin, Math.min(latMax, lat));
            let clampedLon = Math.max(lonMin, Math.min(lonMax, lon));

            const x = ((clampedLon - lonMin) / lonSpan) * (GRID_SIZE - 1);
            const y = ((clampedLat - latMin) / latSpan) * (GRID_SIZE - 1);

            const x0 = Math.floor(x);
            const x1 = Math.min(GRID_SIZE - 1, x0 + 1);
            const y0 = Math.floor(y);
            const y1 = Math.min(GRID_SIZE - 1, y0 + 1);

            const tx = x - x0;
            const ty = y - y0;

            const v00 = grid[y0][x0];
            const v10 = grid[y0][x1];
            const v01 = grid[y1][x0];
            const v11 = grid[y1][x1];

            const dLat = (1 - ty) * ((1 - tx) * v00.dLat + tx * v10.dLat) +
                          ty  * ((1 - tx) * v01.dLat + tx * v11.dLat);
            const dLon = (1 - ty) * ((1 - tx) * v00.dLon + tx * v10.dLon) +
                          ty  * ((1 - tx) * v01.dLon + tx * v11.dLon);

            return {{ dLat, dLon }};
        }}

        function getWind(time, lat, lon) {{
            const wg = PLUME_DATA.wind_grid;
            if (!wg || wg.length === 0) return {{dLat: 0, dLon: 0}};
            
            const h = Math.max(0, Math.min(wg.length - 2, Math.floor(time)));
            const hn = Math.min(wg.length - 1, h + 1);
            const t = time - Math.floor(time);
            const s = t * t * (3 - 2 * t); // smoothstep
            
            const w1 = interpolateGrid(wg[h], lat, lon);
            const w2 = interpolateGrid(wg[hn], lat, lon);

            return {{
                dLat: w1.dLat + s * (w2.dLat - w1.dLat),
                dLon: w1.dLon + s * (w2.dLon - w1.dLon)
            }};
        }}
        
        // ── Spawn particles at all active facilities ──
        // Density slider multiplies the base spawn count in real-time.
        function spawnBatch() {{
            if (particles.length >= MAX_ACTIVE) return;
            
            const displayMode = document.getElementById('display-mode-select').value;
            const densityMult = getSandboxDensity();  // live density slider
            
            PLUME_DATA.facilities.forEach((fac, idx) => {{
                if (!activeFacilities[idx]) return;
                
                // Enforce operating hours schedule if configured
                if (fac.schedule && fac.schedule !== 'continuous') {{
                    const currentHour = playbackTime;
                    if (fac.schedule.type === 'shift') {{
                        if (currentHour < fac.schedule.start_hour || currentHour > fac.schedule.end_hour) {{
                            return;
                        }}
                    }}
                }}
                
                fac.chemicals.forEach(c => {{
                    if (!activeChemicals[idx] || !activeChemicals[idx][c.chemical]) return;
                    
                    // Stack Spawning
                    if (displayMode === 'combined' || displayMode === 'stack') {{
                        const stackLbs = c.stack_lbs || 0;
                        if (stackLbs > 0) {{
                            const ratio = stackLbs / maxFacLbs;
                            const countFloat = ratio * BASE_SPAWN_COUNT * 1.5 * densityMult;
                            let count = Math.floor(countFloat);
                            if (Math.random() < (countFloat - count)) count += 1;
                            
                            for (let i = 0; i < count; i++) {{
                                particles.push({{
                                    lat: fac.lat + (Math.random() - 0.5) * 0.0008,
                                    lon: fac.lon + (Math.random() - 0.5) * 0.0008,
                                    ht: fac.height || 15.0,
                                    birth: playbackTime,
                                    fac: idx,
                                    chem: c.chemical,
                                    col: fac.color,
                                    type: 'stack',
                                    tLat: (Math.random() - 0.5) * 2,
                                    tLon: (Math.random() - 0.5) * 2
                                }});
                            }}
                        }}
                    }}
                    
                    // Fugitive Spawning
                    if (displayMode === 'combined' || displayMode === 'fugitive') {{
                        const fugitiveLbs = c.fugitive_lbs || 0;
                        if (fugitiveLbs > 0) {{
                            const ratio = fugitiveLbs / maxFacLbs;
                            const countFloat = ratio * BASE_SPAWN_COUNT * 1.5 * densityMult;
                            let count = Math.floor(countFloat);
                            if (Math.random() < (countFloat - count)) count += 1;
                            
                            for (let i = 0; i < count; i++) {{
                                particles.push({{
                                    lat: fac.lat + (Math.random() - 0.5) * 0.0012,
                                    lon: fac.lon + (Math.random() - 0.5) * 0.0012,
                                    ht: 2.0, // lower fugitive release height
                                    birth: playbackTime,
                                    fac: idx,
                                    chem: c.chemical,
                                    col: fac.color,
                                    type: 'fugitive',
                                    tLat: (Math.random() - 0.5) * 3,
                                    tLon: (Math.random() - 0.5) * 3
                                }});
                            }}
                        }}
                    }}
                }});
            }});
        }}
        
        // ── Advect all particles forward by dtHours ──
        // Lifespan slider is read live so lowering lifespan instantly prunes old particles.
        function advect(dtHours) {{
            const displayMode = document.getElementById('display-mode-select').value;
            const liveLifespan = getSandboxLifespan();  // dynamic lifespan from slider
            particles = particles.filter(p => {{
                const age = (playbackTime - p.birth) * 60;
                const matchesMode = (displayMode === 'combined') || (displayMode === p.type);
                return age >= 0 && age < liveLifespan && activeFacilities[p.fac] && activeChemicals[p.fac][p.chem] && matchesMode;
            }});
            
            for (let i = 0; i < particles.length; i++) {{
                const p = particles[i];
                const ageH = playbackTime - p.birth; // age in hours
                const baseTurb = p.type === 'fugitive' ? TURB_BASE * 1.5 : TURB_BASE;
                const turbGrowth = p.type === 'fugitive' ? TURB_GROWTH * 1.5 : TURB_GROWTH;
                const turb = baseTurb + turbGrowth * ageH;
                const wind = getWind(playbackTime, p.lat, p.lon);
                
                p.lat += (wind.dLat + p.tLat * turb + (Math.random() - 0.5) * turb * 0.4) * dtHours;
                p.lon += (wind.dLon + p.tLon * turb + (Math.random() - 0.5) * turb * 0.4) * dtHours;
                if (p.type === 'fugitive') {{
                    p.ht = Math.max(0, Math.min(10, p.ht + (Math.random() - 0.5) * 1 * dtHours));
                }} else {{
                    p.ht = Math.max(0, p.ht + (Math.random() - 0.5) * 3 * dtHours);
                }}
            }}
        }}
        
        // ── Deterministic jitter to de-cluster co-located dots ──
        function jHash(a, b) {{
            const s = a * 2654435761 + b * 340573321;
            return ((s >>> 0) % 1000) / 1000.0;
        }}

        // ── Draw all active particles ──
        // Size, lifespan, and per-type opacity sliders are read every frame.
        function drawParticles() {{
            resizeCanvas();
            const topLeft = map.containerPointToLayerPoint([0, 0]);
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            document.getElementById('active-count').textContent = particles.length;
            
            const bounds = map.getBounds();
            const liveLifespan = getSandboxLifespan();
            const liveSize = getSandboxSize();
            const stackOpacity = getSandboxStackOpacity();
            const fugitiveOpacity = getSandboxFugitiveOpacity();
            
            for (let i = 0; i < particles.length; i++) {{
                const p = particles[i];
                const ageMin = (playbackTime - p.birth) * 60;
                if (ageMin < 0 || ageMin >= liveLifespan) continue;
                
                const ll = L.latLng(p.lat, p.lon);
                if (!bounds.contains(ll)) continue;
                
                const pt = map.latLngToLayerPoint(ll);
                const ageFade = Math.max(0, 1 - (ageMin / liveLifespan));
                if (ageFade <= 0.01) continue;

                // Per-type opacity ceiling from sandbox sliders
                const typeOpacityCap = (p.type === 'fugitive') ? fugitiveOpacity : stackOpacity;
                const opacity = ageFade * typeOpacityCap;
                
                const baseR = liveSize;  // dynamic from size slider
                const hBonus = Math.min(1.2, p.ht / 250.0);
                const radius = Math.min(liveSize * 2.5, (baseR + hBonus) * {EMISSION_MULTIPLIER});
                
                const jx = (jHash(i, p.fac) - 0.5) * 2.5;
                const jy = (jHash(i + 7919, p.fac) - 0.5) * 2.5;
                const px = pt.x - topLeft.x + jx;
                const py = pt.y - topLeft.y + jy;
                
                ctx.beginPath();
                ctx.arc(px, py, radius, 0, 6.2832);
                ctx.fillStyle = hexToRgbA(p.col, opacity);
                ctx.fill();
                
                ctx.beginPath();
                ctx.arc(px, py, radius * 2, 0, 6.2832);
                ctx.fillStyle = hexToRgbA(p.col, opacity * 0.17);
                ctx.fill();
            }}
        }}

        // Playback speed mapping
        function getSpeedMultiplier() {{
            const selectVal = parseInt(document.getElementById('speed-select').value);
            switch(selectVal) {{
                case 1: return 1.0 / 60.0;
                case 2: return 5.0 / 60.0;
                case 3: return 10.0 / 60.0;
                case 4: return 30.0 / 60.0;
                case 5: return 60.0 / 60.0;
                default: return 5.0 / 60.0;
            }}
        }}

        // HUD State update
        const timeSlider = document.getElementById('time-slider');
        const timeValDisplay = document.getElementById('time-display');
        const ampmDisplay = document.getElementById('ampm-display');
        
        function updateHUD() {{
            timeSlider.value = playbackTime.toFixed(2);
            const {{ time, ampm }} = formatSimulationTime(playbackTime);
            timeValDisplay.textContent = time;
            ampmDisplay.textContent = ampm;

            let currentHourInt = Math.floor(playbackTime);
            if (currentHourInt < 0) currentHourInt = 0;
            if (currentHourInt > 23) currentHourInt = 23;
            updateMonitorPopups(currentHourInt);
        }}

        // Slider scrub
        timeSlider.addEventListener('input', (e) => {{
            const newTime = parseFloat(e.target.value);
            if (Math.abs(newTime - playbackTime) > 0.3) {{
                particles = [];
                lastSpawnTime = -999;
            }}
            playbackTime = newTime;
            prevPlaybackTime = playbackTime;
            updateHUD();
            drawParticles();
        }});

        // Tooltip hover
        const tooltip = document.getElementById('tooltip');
        const tooltipTitle = document.getElementById('tooltip-title');
        const tooltipBody = document.getElementById('tooltip-body');
        
        map.on('mousemove', (e) => {{
            const mp = e.containerPoint;
            let hit = null;
            
            for (let i = 0; i < particles.length; i++) {{
                const p = particles[i];
                const pt = map.latLngToContainerPoint(L.latLng(p.lat, p.lon));
                if (Math.hypot(pt.x - mp.x, pt.y - mp.y) < 8) {{
                    hit = p;
                    break;
                }}
            }}
            
            if (hit) {{
                const fac = PLUME_DATA.facilities[hit.fac];
                tooltipTitle.textContent = fac.name;
                tooltipTitle.style.color = fac.color;
                const ageMin = ((playbackTime - hit.birth) * 60).toFixed(0);
                tooltipBody.innerHTML = `
                    Chemical: <strong>` + hit.chem + `</strong><br/>
                    Type: <strong>` + hit.type.toUpperCase() + `</strong><br/>
                    Lat/Lon: <strong>` + hit.lat.toFixed(4) + `, ` + hit.lon.toFixed(4) + `</strong><br/>
                    Height: <strong>` + hit.ht.toFixed(0) + ` m AGL</strong><br/>
                    Age: <strong>` + ageMin + ` min</strong>
                `;
                tooltip.style.left = (mp.x + 15) + "px";
                tooltip.style.top = (mp.y + 15) + "px";
                tooltip.style.display = 'block';
            }} else {{
                tooltip.style.display = 'none';
            }}
        }});
        
        map.on('mouseout', () => {{
            tooltip.style.display = 'none';
        }});

        // Play/Pause
        const playBtn = document.getElementById('play-btn');
        const playIcon = document.getElementById('play-icon');
        const pauseIcon = document.getElementById('pause-icon');
        
        playBtn.addEventListener('click', () => {{
            isPlaying = !isPlaying;
            if (isPlaying) {{
                playIcon.style.display = 'none';
                pauseIcon.style.display = 'block';
            }} else {{
                playIcon.style.display = 'block';
                pauseIcon.style.display = 'none';
            }}
        }});

        document.getElementById('restart-btn').addEventListener('click', () => {{
            playbackTime = 0.0;
            prevPlaybackTime = 0.0;
            particles = [];
            lastSpawnTime = -999;
            updateHUD();
            drawParticles();
        }});

        // Map redraws
        map.on('move', drawParticles);
        map.on('zoom', drawParticles);
        map.on('resize', () => {{
            resizeCanvas();
            drawParticles();
        }});

        // Main animation loop
        let lastTimestamp = null;
        
        function tick(timestamp) {{
            if (!lastTimestamp) lastTimestamp = timestamp;
            const deltaSec = (timestamp - lastTimestamp) / 1000;
            lastTimestamp = timestamp;
            
            if (isPlaying) {{
                const hourRate = getSpeedMultiplier();
                const dtHours = deltaSec * hourRate;
                playbackTime += dtHours;
                
                if (playbackTime > 24.0) {{
                    playbackTime = 0.0;
                    particles = [];
                    lastSpawnTime = -999;
                }}
                
                if (playbackTime - lastSpawnTime >= SPAWN_INTERVAL) {{
                    spawnBatch();
                    lastSpawnTime = playbackTime;
                }}
                
                advect(dtHours);
                prevPlaybackTime = playbackTime;
                
                updateHUD();
            }}
            
            drawParticles();
            requestAnimationFrame(tick);
        }}
        
        // Boot
        requestAnimationFrame(tick);
    </script>
</body>
</html>
"""
        
        with open(output_path, "w") as f:
            f.write(html_content)
        print(f"Interactive Leaflet visualization written successfully to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calvert City Plume Dispersion Simulation Pipeline")
    parser.add_argument(
        "--workspace",
        default=os.path.dirname(os.path.abspath(__file__)),
        help="Workspace directory containing calculations and web assets"
    )
    parser.add_argument(
        "--skip-weather",
        action="store_true",
        help="Skip weather downloading and conversion if MET file is already created"
    )
    parser.add_argument(
        "--regen-html",
        action="store_true",
        help="Skip ALL simulation steps and only regenerate the HTML visualization "
             "using data already embedded in the existing index.html"
    )

    args = parser.parse_args()

    # Run the full pipeline orchestration
    try:
        pipeline = CalvertCityPlumeEngine(
            workspace_dir=args.workspace
        )

        # Step 1: Programmatically generate the list of dates between START_DATE and END_DATE
        start_dt = datetime.datetime.strptime(START_DATE, "%Y-%m-%d")
        end_dt = datetime.datetime.strptime(END_DATE, "%Y-%m-%d")
        delta = datetime.timedelta(days=1)

        date_list = []
        curr_dt = start_dt
        while curr_dt <= end_dt:
            date_list.append(curr_dt.strftime("%Y-%m-%d"))
            curr_dt += delta

        # ── Fast-path detection: check for existing simulation outputs ──
        existing_html_path = os.path.join(pipeline.workspace_dir, pipeline.output_html_name)
        has_existing_html = os.path.exists(existing_html_path) and os.path.getsize(existing_html_path) > 1000

        # Count existing run directories (one per facility = simulation already ran)
        existing_run_dirs = [
            d for d in os.listdir(pipeline.workspace_dir)
            if d.startswith("run_") and os.path.isdir(os.path.join(pipeline.workspace_dir, d))
        ]

        skip_simulation = False

        if args.regen_html:
            # Explicit CLI flag: skip everything, just rebuild HTML
            skip_simulation = True
            print("\n--regen-html flag detected. Skipping all simulation steps.")

        elif has_existing_html and len(existing_run_dirs) > 0:
            # Interactive prompt: existing data found
            print("\n" + "=" * 64)
            print("  EXISTING SIMULATION DATA DETECTED")
            print("=" * 64)
            print(f"  HTML visualization : {existing_html_path}")
            print(f"  Run directories    : {len(existing_run_dirs)} facility folders found")
            print(f"  Simulation dates   : {START_DATE} to {END_DATE} ({len(date_list)} day(s))")
            print()
            print("  The full simulation pipeline (weather download, HYSPLIT,")
            print("  EPA monitor processing) can take a very long time.")
            print()
            print("  If you're only making UI/HUD changes, you can skip the")
            print("  simulation and just regenerate the HTML from existing data.")
            print("=" * 64)
            print()

            while True:
                answer = input("  Re-run full simulation? [y/N]: ").strip().lower()
                if answer in ("", "n", "no"):
                    skip_simulation = True
                    print("\n  → Skipping simulation. Regenerating HTML only.\n")
                    break
                elif answer in ("y", "yes"):
                    skip_simulation = False
                    print("\n  → Running full simulation pipeline.\n")
                    break
                else:
                    print("  Please enter 'y' or 'n'.")

        if skip_simulation:
            # ── Extract embedded JSON archive from existing index.html ──
            master_archive = None

            if has_existing_html:
                print("Extracting simulation data from existing index.html...")
                try:
                    import re as _re
                    with open(existing_html_path, "r", encoding="utf-8") as f:
                        html_text = f.read()

                    # The JSON blob is embedded as:
                    #   const historicalSimulationArchive = { ... };
                    pattern = r'const\s+historicalSimulationArchive\s*=\s*'
                    match = _re.search(pattern, html_text)
                    if match:
                        json_start = match.end()
                        # Find the matching closing brace by counting braces
                        depth = 0
                        json_end = json_start
                        for i in range(json_start, len(html_text)):
                            if html_text[i] == '{':
                                depth += 1
                            elif html_text[i] == '}':
                                depth -= 1
                                if depth == 0:
                                    json_end = i + 1
                                    break
                        json_str = html_text[json_start:json_end]
                        master_archive = json.loads(json_str)
                        num_dates = len(master_archive)
                        print(f"Successfully extracted archive with {num_dates} date(s) of simulation data.")
                        
                        # Rebuild and inject updated facilities metadata (e.g. schedules, coords, colors)
                        for date_key in master_archive:
                            if "plumes" in master_archive[date_key]:
                                plumes = master_archive[date_key]["plumes"]
                                updated_facilities = []
                                for fac in pipeline.facilities:
                                    tri_data = pipeline.get_facility_releases(fac["name"])
                                    releases = tri_data.get("releases", [])
                                    total_lbs = sum(chem.get("total_lbs", 0.0) for chem in releases)
                                    updated_facilities.append({
                                        "id": fac["id"],
                                        "name": fac["name"],
                                        "lat": fac["lat"],
                                        "lon": fac["lon"],
                                        "height": fac["height"],
                                        "color": fac["color"],
                                        "tri_id": fac["tri_id"],
                                        "tri_name": tri_data.get("fac_name", fac["name"]),
                                        "chemicals": releases,
                                        "total_lbs": total_lbs,
                                        "schedule": fac.get("schedule", "continuous")
                                    })
                                plumes["facilities"] = updated_facilities
                            
                            # Also re-parse and update monitors data so we don't have to rerun HYSPLIT simulation
                            print(f"Updating monitors data for date: {date_key}")
                            pipeline.set_active_date(date_key)
                            master_archive[date_key]["monitors"] = pipeline.process_ambient_monitors()
                    else:
                        print("Warning: Could not locate embedded JSON in existing HTML.")
                except Exception as e:
                    print(f"Warning: Failed to extract data from existing HTML: {e}")

            if master_archive is None:
                print("ERROR: No existing simulation data could be recovered.")
                print("Please re-run without --regen-html to generate fresh data.")
                sys.exit(1)

            # Regenerate HTML with the extracted archive
            pipeline.generate_web_visualization(master_archive)

        else:
            # ── Full pipeline execution ──
            master_archive = {}

            for d_str in date_list:
                print(f"\n========================================================")
                print(f" PROCESSING SIMULATION FOR DATE: {d_str}")
                print(f"========================================================\n")
                pipeline.set_active_date(d_str)

                # Step 1: NOAA HRRR retrieval (skip download and conversion if daily ARL file exists)
                grib_files = []
                # Check if meteorology file exists and is complete (each hour is ~554MB, 24 hours is ~13.3GB)
                # We enforce a minimum size of 10GB to ensure it is not a partial/incomplete compilation.
                if os.path.exists(pipeline.met_file_path) and os.path.getsize(pipeline.met_file_path) >= 10 * 1024 * 1024 * 1024:
                    print(f"Existing complete ARL meteorology file found ({os.path.getsize(pipeline.met_file_path):,} bytes) for {d_str}. Skipping weather download and conversion.")
                else:
                    if args.skip_weather:
                        # Look for cached GRIB files matching this date
                        date_folder_str = pipeline.date_obj.strftime("%Y%m%d")
                        grib_pattern = os.path.join(pipeline.grib_dir, "hrrr", date_folder_str, "**", "*.grib2")
                        grib_files = sorted(glob.glob(grib_pattern, recursive=True))
                        if not grib_files:
                            grib_files = sorted(glob.glob(os.path.join(pipeline.grib_dir, f"*{date_folder_str}*.grib2")))

                        if grib_files:
                            print(f"Skipping weather download. Found {len(grib_files)} existing GRIB files for {d_str} in cache.")
                        else:
                            print(f"No existing GRIB files or ARL found for {d_str}. Running download...")
                            grib_files = pipeline.download_weather_data()
                    else:
                        grib_files = pipeline.download_weather_data()

                    pipeline.convert_grib_to_arl(grib_files)

                # Step 2: HYSPLIT simulation
                raw_output = pipeline.run_dispersion_model()

                # Step 3: Compile coordinates and EPA data
                compiled_json = pipeline.compile_data_for_json(raw_output)

                # Step 4: Add to master archive
                master_archive[d_str] = {
                    "plumes": compiled_json,
                    "monitors": pipeline.regional_monitor_data
                }

            # Step 5: Visual assets compilation
            pipeline.generate_web_visualization(master_archive)

        print("\nPipeline execution completed successfully!")
        print(f"You can view the simulation by opening: file://{os.path.join(pipeline.workspace_dir, pipeline.output_html_name)}")

    except Exception as err:
        print(f"\nPipeline failure: {err}", file=sys.stderr)
        sys.exit(1)


