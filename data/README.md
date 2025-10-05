# Data Directory

This directory contains GeoJSON files required for geographic visualizations in GridCoPilot.

## Files

### NERC_regions_subregions.json
- **Purpose**: Contains NERC (North American Electric Reliability Corporation) regions and subregions boundaries
- **Source**: NERC geographic data
- **Usage**: Used for mapping NERC regions in visualizations
- **Size**: ~60MB

### geojson-counties-fips.json
- **Purpose**: Contains US county boundaries with FIPS codes
- **Source**: US Census Bureau geographic data
- **Usage**: Used for county-level mapping and FIPS code lookups
- **Size**: ~3MB

## Docker Integration

These files are automatically included in Docker builds and will be available at `/app/data/` inside the container.

The visualization code (`utils/visualization_county_v1.py`) has been updated to use relative paths that work both locally and in Docker containers:

```python
# Paths work in both local development and Docker
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
GEOJSON_PATH = os.path.join(DATA_DIR, "NERC_regions_subregions.json")
COUNTIES_GEOJSON_PATH = os.path.join(DATA_DIR, "geojson-counties-fips.json")
```

## File Structure
```
data/
├── README.md                     # This file
├── NERC_regions_subregions.json  # NERC regions data
└── geojson-counties-fips.json    # County boundaries data
```

## Notes

- These files are cached by Streamlit using `@st.cache_data` decorator for performance
- The files are automatically simplified during loading to reduce memory usage
- If files are missing, the application will display appropriate error messages
- File paths are now Docker-compatible (no hardcoded local paths)