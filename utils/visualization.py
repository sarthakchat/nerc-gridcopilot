# type: ignore
# pyright: reportMissingTypeStubs=false
import json
import re
import pandas as pd
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
import streamlit as st
from shapely.geometry import shape, mapping
import os
from typing import Dict, List, Tuple, Optional, Any
from .response_formatter import robust_json_parse

# Check if GeoJSON file exists
GEOJSON_PATH = "/Users/chat200/Downloads/NERC_regions_subregions 2.json"
GEOJSON_AVAILABLE = os.path.exists(GEOJSON_PATH)

@st.cache_data
def load_nerc_geojson(path: str) -> Dict[str, Any]:
    """Load and cache GeoJSON file."""
    with open(path, 'r') as f:
        gj = json.load(f)
    # Simplify each feature geometry to reduce complexity
    for feature in gj.get("features", []):
        geom_data = feature.get("geometry")
        if not geom_data:
            continue
        try:
            geom = shape(geom_data)
            simplified = geom.simplify(0.01, preserve_topology=True)
            feature["geometry"] = mapping(simplified)
        except Exception:
            continue
    return gj

# Hardcoded mapping of string ID to SUBNAME for reliable labeling
STRING_ID_TO_SUBNAME = {
    "1": "AZ-NM-SNV",
    "2": "CA-MX US",
    "3": "ERCOT",
    "4": "FRCC",
    "5": "NEW ENGLAND",
    "6": "NWPP",
    "7": "RMPA",
    "8": "SPP",
    "9": "DELTA",
    "10": "SOUTHEASTERN",
    "11": "CENTRAL",
    "12": "VACAR",
    "15": "NEW YORK",
    "17": "RFC",
    "18": "MRO US",
    "20": "GATEWAY"
}



def parse_temperature_json(response: str) -> Tuple[bool, Optional[pd.DataFrame], Optional[str]]:
    """Parse structured JSON response and detect event type."""
    try:
        cleaned = response.strip()
        json_start = cleaned.find('{')
        if json_start == -1:
            return False, None, None
        json_end = cleaned.rfind('}') + 1
        json_str = cleaned[json_start:json_end]
        # Parse JSON using robust parser
        data = robust_json_parse(json_str)
        if not (isinstance(data, dict) and 'data' in data and isinstance(data['data'], list)):
            return False, None, None
        events = data['data']
        # Map abbreviated LLM output keys to standard keys for visualization
        if events and isinstance(events[0], dict) and 'DS' in events[0]:
            key_map = {
                'DS': 'start_date',
                'DE': 'end_date',
                'T': 'temperature',
                'SC': 'spatial_coverage',
                'ID': 'NERC_ID',
                'Type': 'event_type'
            }
            for evt in events:
                for old_key, new_key in key_map.items():
                    if old_key in evt:
                        evt[new_key] = evt.pop(old_key)
        if not events:
            return False, None, None
        # Check for required fields
        required_fields = ['start_date', 'temperature', 'NERC_ID']
        if not all(field in events[0] for field in required_fields):
            return False, None, None
        # Convert to DataFrame
        df = pd.DataFrame(events)
        df['start_date'] = pd.to_datetime(df['start_date'])
        # Determine event type
        event_type = 'mixed'
        if 'event_type' in df.columns and df['event_type'].nunique() == 1:
            event_type = str(df['event_type'].iloc[0])
        return True, df, event_type
    except Exception:
        return False, None, None


@st.cache_data
def get_subname_centroids(nerc_geojson: Dict[str, Any]) -> pd.DataFrame:
    """Generate centroids for NERC regions to display SUBNAME labels."""
    labels = []
    for feature in nerc_geojson.get("features", []):
        geom_data = feature.get("geometry")
        if not geom_data:
            continue
        try:
            shp = shape(geom_data)
            cen = shp.centroid
        except Exception:
            continue
        
        # Get string ID from properties instead of feature id
        properties = feature.get("properties", {})
        string_id = properties.get("ID")
        if string_id is None:
            continue
            
        subname = STRING_ID_TO_SUBNAME.get(str(string_id))
        if subname:
            # Use the actual string ID from properties for consistency
            labels.append({"lat": cen.y, "lon": cen.x, "SUBNAME": subname, "NERC_ID": str(string_id)})
    return pd.DataFrame(labels)


def create_animated_choropleth_from_data(df: pd.DataFrame, event_type: str = 'heat'):
    """Create an animated choropleth map from temperature event data."""
    
    try:
        # Load GeoJSON
        if not GEOJSON_AVAILABLE:
            st.error("GeoJSON file not found. Cannot create choropleth map.")
            return None
        nerc_geojson = load_nerc_geojson(GEOJSON_PATH)

        # Prepare data for animation
        df_anim = df.copy()
        df_anim['year_month'] = df_anim['start_date'].dt.to_period('M').astype(str)
        
        # Aggregate by time period and region
        agg_data = df_anim.groupby(['year_month', 'NERC_ID']).agg({
            'temperature': ['count', 'mean', 'max', 'min']
        }).round(2)
        
        agg_data.columns = ['event_count', 'avg_temp', 'max_temp', 'min_temp']
        agg_data = agg_data.reset_index()
        # Ensure the IDs match GeoJSON featureid key types (strings)
        agg_data['OBJECTID'] = agg_data['NERC_ID'].astype(str)
        
        # Choose visualization settings based on event type (heat = red, cold = blue)
        if event_type == 'heat':
            # Use yellow-orange-red scale for heat events
            color_scale = "YlOrRd"
            temp_column = "max_temp"
            title_suffix = "Heat Wave"
        elif event_type == 'cold':
            # Use blue scale for cold snap events (normal direction, not reversed)
            color_scale = "Blues_r"
            temp_column = "min_temp"
            title_suffix = "Cold Snap"
        else:
            color_scale = "RdBu_r"
            temp_column = "avg_temp"
            title_suffix = "Temperature"
        
        # Determine global color range to prevent scale changes across frames
        vmin = agg_data[temp_column].min()
        vmax = agg_data[temp_column].max()
        
        # For cold events, ensure we have a reasonable color range
        if event_type == 'cold':
            # Make sure we have a good spread for the blue color scale
            # If the range is too narrow, expand it slightly
            temp_range = vmax - vmin
            if temp_range < 5:  # If temperature range is less than 5 degrees
                vmin = vmin - 2
                vmax = vmax + 2
        # General guard against degenerate color range
        try:
            if pd.isna(vmin) or pd.isna(vmax):
                vmin, vmax = 0.0, 1.0
            elif vmin == vmax:
                eps = 0.1 if vmax == 0 else abs(vmax) * 0.01
                vmin -= eps
                vmax += eps
        except Exception:
            pass

        # Base figure without embedding geojson in each trace
        fig = go.Figure()
        # Base map with static outlines and shared coloraxis for temperature
        fig.update_layout(
            mapbox_style='carto-positron',
            mapbox=dict(
                zoom=3.2,
                center={'lat': 39.5, 'lon': -98},
                layers=[dict(
                    sourcetype='geojson',
                    source=nerc_geojson,
                    type='line',
                    color='black',
                    line=dict(width=2)
                )]
            ),
            coloraxis=dict(
                colorscale=color_scale,
                cmin=vmin,
                cmax=vmax,
                colorbar=dict(
                    title=f'Temperature (°F)<br>{title_suffix}',
                    titleside='right'
                ),
                showscale=True
            ),
            margin={'r': 10, 't': 80, 'l': 10, 'b': 10},
            height=700
        )

        # Prepare static label trace (region names)
        label_df = get_subname_centroids(nerc_geojson)
        label_trace = go.Scattermapbox(
            lat=label_df['lat'], lon=label_df['lon'], mode='text',
            text=label_df['SUBNAME'], textfont=dict(size=12, color='black'),
            showlegend=False, hoverinfo='none'
        )
        # Add initial choropleth for first period using shared coloraxis
        periods = sorted(agg_data['year_month'].unique())
        first_period = periods[0]
        df_first = agg_data[agg_data['year_month'] == first_period]
        init_chor = go.Choroplethmapbox(
            geojson=nerc_geojson, featureidkey='properties.ID',
            locations=df_first['OBJECTID'].astype(str), z=df_first[temp_column],
            coloraxis='coloraxis', marker_opacity=0.8, marker_line_width=1,
            marker_line_color='white',
            hovertemplate='<b>NERC Region: %{location}</b><br>' +
                         f'{temp_column.replace("_", " ").title()}: %{{z:.1f}}°F<br>' +
                         '<extra></extra>',
            name=f'{title_suffix} - {first_period}'
        )
        fig.add_traces([init_chor, label_trace])

        # Build frames manually without geojson
        frames = []
        for period in sorted(agg_data['year_month'].unique()):
            df_slice = agg_data[agg_data['year_month'] == period]
            chor = go.Choroplethmapbox(
                geojson=nerc_geojson, featureidkey='properties.ID',
                locations=df_slice['OBJECTID'].astype(str), z=df_slice[temp_column],
                coloraxis='coloraxis', marker_opacity=0.8, marker_line_width=1,
                marker_line_color='white',
                hovertemplate='<b>NERC Region: %{location}</b><br>' +
                             f'{temp_column.replace("_", " ").title()}: %{{z:.1f}}°F<br>' +
                             '<extra></extra>',
                name=f'{title_suffix} - {period}'
            )
            # only update choropleth; labels remain static
            frames.append(go.Frame(data=[chor], name=period))

        fig.frames = frames
        # add playback controls
        fig.update_layout(
            updatemenus=[dict(
                type='buttons', showactive=False,
                y=0, x=1.05, xanchor='right', yanchor='top',
                pad=dict(t=0, r=10),
                buttons=[dict(label='Play', method='animate',
                              args=[None, {'frame': {'duration':500, 'redraw':True}, 'fromcurrent':True}])]
            )],
            sliders=[dict(
                active=0, pad={'t':50},
                steps=[dict(label=fr.name, method='animate', args=[[fr.name], {'frame':{'duration':0}, 'mode':'immediate'}]) for fr in frames]
            )]
        )

        # Final layout title
        fig.update_layout(title={'text': f"{title_suffix} Events - NERC Regions", 'x':0.5, 'xanchor':'center'})

        return fig
        
    except Exception:
        st.error("Error creating animated choropleth.")
        return None


def execute_viz_code(code: Optional[str], response: Optional[str] = None):
    """Execute visualization code or generate automatic visualization from response."""
    # Only handle temperature event visualization
    if response:
        is_temp_data, df, event_type = parse_temperature_json(response)
        
        if is_temp_data and df is not None:
            st.info("*Temperatures shown in NERC region represent maximum recorded during the heat wave event or minimum recorded during the cold snap event.*")
            return create_animated_choropleth_from_data(df, event_type or 'mixed')
    
    # No visualization possible
    st.info("No visualization data detected. Please provide temperature event data.")
    return None
