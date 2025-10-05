#!/usr/bin/env python3
# type: ignore  # suppress type-checker errors for dynamic JSON processing
import json
import re
import html
from typing import Optional, Dict, Any, List
def robust_json_parse(json_str: str) -> Optional[Dict[str, Any]]:
    """Inline robust JSON parsing to handle malformed JSON."""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        pass
    try:
        cleaned = re.sub(r'//.*?(?=\n|$)', '', json_str, flags=re.MULTILINE)
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    try:
        fixed = re.sub(r',\s*([}\]])', r'\1', json_str)
        return json.loads(fixed)
    except json.JSONDecodeError:
        pass
    try:
        # Truncate to last complete brace
        brace_count = 0
        last_valid = 0
        for i, ch in enumerate(json_str):
            if ch == '{':
                brace_count += 1
            elif ch == '}':
                brace_count -= 1
            if brace_count == 0:
                last_valid = i
        truncated = json_str[:last_valid+1]
        return json.loads(truncated)
    except Exception:
        pass
    
    # Strategy 6: Truncate to last complete object
    try:
        # Find the last complete closing brace
        last_brace = json_str.rfind('}')
        if last_brace != -1:
            # Check if this could be a valid JSON structure
            truncated = json_str[:last_brace + 1]
            
            # Remove any trailing comma and whitespace after the last }
            truncated = re.sub(r',\s*$', '', truncated)
            
            # Count opening and closing elements to see what we need to add
            open_braces = truncated.count('{')
            close_braces = truncated.count('}')
            open_brackets = truncated.count('[')
            close_brackets = truncated.count(']')
            
            # Add missing closures if needed
            if open_brackets > close_brackets:
                truncated += ']' * (open_brackets - close_brackets)
            if open_braces > close_braces:
                truncated += '}' * (open_braces - close_braces)
                
            return json.loads(truncated)
    except (json.JSONDecodeError, ValueError):
        pass
    
    return None

def extract_json_from_response(response: str) -> Optional[Dict[str, Any]]:
    """Extract JSON data from LLM response for visualization purposes."""
    try:
        cleaned = response.strip()
        # Prefer fenced code blocks (```json ... ```), case-insensitive on language tag
        fence_regex = re.compile(r"```\s*(json)?\s*\n(.*?)```", re.IGNORECASE | re.DOTALL)
        m = fence_regex.search(cleaned)
        if m:
            json_str = m.group(2).strip()
            parsed = robust_json_parse(json_str)
            if parsed is not None:
                return parsed

        # Fallback: find first '{' and attempt robust parsing of the remainder
        brace_idx = cleaned.find('{')
        if brace_idx != -1:
            json_str = cleaned[brace_idx:]
            return robust_json_parse(json_str)
        return None
    except (json.JSONDecodeError, KeyError, TypeError):
        return None

def format_json_response_as_table(response: str) -> str:
    """Convert JSON response to an HTML table with stable columns and units."""
    try:
        data = extract_json_from_response(response)
        if not (isinstance(data, dict) and 'data' in data and isinstance(data['data'], list)):
            return response

        events_raw = data['data']
        if not events_raw or not isinstance(events_raw[0], dict):
            return "No events found."

        # Build a display mapping (source_key -> display_name)
        # Support both abbreviated (DS, DE, T, SC, ID, Type) and verbose keys
        display_map_candidates = [
            {
                'DS': 'Start Date',
                'DE': 'End Date',
                'T': 'Temperature (°F)',
                'SC': 'Spatial Coverage (%)',
                'ID': 'NERC ID',
                'Type': 'Event Type',
            },
            {
                'start_date': 'Start Date',
                'end_date': 'End Date',
                'temperature': 'Temperature (°F)',
                'spatial_coverage': 'Spatial Coverage (%)',
                'NERC_ID': 'NERC ID',
                'event_type': 'Event Type',
            },
        ]

        # Determine which candidate mapping applies based on first row
        first_keys = set(events_raw[0].keys())
        display_map: Dict[str, str] = {}
        for cand in display_map_candidates:
            overlap = first_keys.intersection(cand.keys())
            if overlap:
                display_map.update(cand)
        # For any remaining keys, generate a title-cased display
        for k in first_keys:
            if k not in display_map:
                display_map[k] = k.replace('_', ' ').title()

        # Construct preferred column order using display names
        preferred_order: List[str] = [
            'Start Date',
            'End Date',
            'Event Type',
            'NERC ID',
            'Temperature (°F)',
            'Spatial Coverage (%)',
        ]

        # Build list of all display columns across all rows
        all_source_keys = set()
        for e in events_raw:
            if isinstance(e, dict):
                all_source_keys.update(e.keys())
        all_display_cols = {display_map.get(k, k.replace('_', ' ').title()) for k in all_source_keys}

        # Final ordered columns: preferred first (if present), then the rest sorted
        columns: List[str] = [c for c in preferred_order if c in all_display_cols]
        remaining = sorted(all_display_cols - set(columns))
        columns.extend(remaining)

        # Build reverse map from display_name -> list of possible source keys
        reverse_map: Dict[str, List[str]] = {}
        for src, disp in display_map.items():
            reverse_map.setdefault(disp, []).append(src)

        # Render as HTML table
        out: List[str] = []
        out.append('<div style="max-height:400px; overflow:auto;">')
        out.append('<table border="1" style="border-collapse:collapse; width:100%;">')
        # Header
        out.append('<thead><tr>' + ''.join(f'<th style=\"padding:8px; text-align:left;\">{html.escape(h)}</th>' for h in columns) + '</tr></thead>')
        out.append('<tbody>')

        # Helper for fetching a value using display -> potential source keys
        def get_value_for_display(event: Dict[str, Any], display_col: str) -> Any:
            # Try mapped keys first
            for src in reverse_map.get(display_col, []):
                if src in event:
                    return event[src]
            # Otherwise try a heuristic fallback by normalizing
            norm = display_col.lower().replace(' ', '_').replace('(degree_f)', 'temperature').replace('(%)', '').strip()
            return event.get(norm, "")

        # Data rows
        for event in events_raw:
            if not isinstance(event, dict):
                continue
            cells: List[str] = []
            for col in columns:
                val = get_value_for_display(event, col)
                # Format values for special columns
                if isinstance(val, float):
                    if col == 'Temperature (°F)':
                        cell_text = f"{val:.1f}"
                    elif col == 'Spatial Coverage (%)':
                        # Keep numeric magnitude as provided; just format consistently
                        cell_text = f"{val:.1f}"
                    else:
                        cell_text = f"{val:.1f}"
                else:
                    cell_text = str(val) if val is not None else ''
                cells.append(f'<td style=\"padding:8px;\">{html.escape(cell_text)}</td>')
            out.append('<tr>' + ''.join(cells) + '</tr>')

        out.append('</tbody>')
        out.append('</table>')
        out.append('</div>')
        return ''.join(out)

    except (json.JSONDecodeError, KeyError, TypeError):
        return response

def enhance_response_presentation(response: str) -> str:
    """Format response with JSON table conversion or basic markdown."""
    # Try to convert JSON to table
    json_table = format_json_response_as_table(response)
    if json_table != response:
        # Check if response contains technical insights section
        insights_idx = response.find('### Technical Insights:')
        if insights_idx != -1:
            insights_text = response[insights_idx:].strip()
            # Add methodology note after technical insights
            methodology_note = "\n\n*Heat wave and cold snap events identified using Definition 6: Heat wave events are detected based on daily maximum temperature with two temperature thresholds (T1 ~ 97.5th percentile and T2 ~ 81st percentile). All days in the event must have temperature > T2, with at least 3 consecutive days > T1, and the average temperature across all event days > T1.*"
            
            # Check if insights_text already has Supporting Visualization section
            if "### Supporting Visualization" in insights_text:
                # Replace any existing empty Supporting Visualization section with our complete one
                import re
                # Remove any trailing empty Supporting Visualization sections
                insights_text = re.sub(r'\n*### Supporting Visualization\s*$', '', insights_text)
                return f"## Analysis Results\n\n{json_table}\n\n" + insights_text + methodology_note
            else:
                return f"## Analysis Results\n\n{json_table}\n\n" + insights_text + methodology_note
        # No insights found, return only table
        return f"## Analysis Results\n\n{json_table}"
    
    # Return as-is if already formatted, otherwise add basic heading
    if "**" in response or "##" in response:
        return response
    else:
        return f"## Analysis\n{response}"
