# ⚡ GridCoPilot

⚡ AI-powered analysis and visualization for long-term grid planning

## Overview

GridCoPilot is a GenAI powered tool that streamlines compliance analysis and visualization for extreme weather events. It processes heatwave and coldsnap datasets to provide textual and visual insights for transmission planning requirements.

## 🔐 Alpha Release - Access Control

**This is an alpha release with access control.** Users need a 6-character alphanumeric validation code to access the application.

- 📖 **Users**: See [ALPHA_ACCESS_GUIDE.md](ALPHA_ACCESS_GUIDE.md) for instructions on accessing the application
- 🔧 **Administrators**: See [ACCESS_CODES.md](ACCESS_CODES.md) for managing validation codes

### Default Test Codes
For initial testing, these codes are available:
- `ALPHA1`, `BETA01`, `TEST99`, `DEMO01`

**Important:** Replace default codes with secure codes before production deployment.

## Features

- Natural language querying of power system planning data
- **🎬 Animated choropleth maps for temperature events** (NEW)
- Automated data visualization with smart detection
- Interactive chat interface
- Insight generation from complex datasets

### 🌡️ Enhanced Temperature Event Visualization
GridCoPilot now automatically detects heat wave and cold snap events in JSON responses and creates stunning animated choropleth maps that show:
- Time-based progression of events
- Geographic distribution across NERC regions  
- Interactive controls and detailed hover information
- Smart color coding (warm colors for heat, cool colors for cold)

## Installation

1. Clone this repository
2. Create and activate a virtual environment `python -m venv venv` and `source venv/bin/activate` 
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and configure your environment variables
5. Activate environment variables `source ./activate_env.sh`
6. Run the application: `streamlit run app.py`

## Usage

Ask questions in natural language about extreme weather events in NERC regions, such as:

- "Worst historical heat waves in my service territory of PJM?"
- "Spatial extent of worst heat waves in my service territory of MRO US?"
- "What's the twenty worst heatwave event in ERCOT?"
- "Worst five historical cold snaps in my Pacific Northwest?"
- "What are all coldsnap events after 2000 in RFC and neighbouring regions of MRO US, GATEWAY, NEWYORK, CENTRAL?"
- "What are all coldsnap events after year 2010?"

### 🌡️ Temperature Event Queries (Auto-generates animated choropleth maps):
- "Show me the worst heat wave events in PJM"
- "What are the most severe cold snaps in ERCOT after 2010?"

## Development

This project follows a modular architecture with separation of concerns:
- `models/`: LLM and agent setup
- `utils/`: Database connection, visualization, and response formatting
- `ui/`: Streamlit UI components and styling
- `prompts/`: System and visualization prompts

## Project Structure

```plaintext
gridcopilot/
├── .env.example                # Environment variable template
├── .gitignore                  # Git ignore file
├── README.md                   # Project documentation
├── requirements.txt            # Dependencies
├── activate_env.sh             # Script to load environment variables
│
├── config/
│   └── config.py               # Configuration settings
│
├── data/
│   ├── geojson-counties-fips.json    # County geographic data
│   ├── NERC_regions_subregions.json  # NERC region data
│   └── README.md                     # Data documentation
│
├── assets/
│   ├── pnnl.png                # PNNL logo
│   └── opengraph-image.png     # Sponsor logo
│
├── models/
│   └── llm_service.py          # LLM and agent setup
│
├── prompts/
│   └── base_prompt.txt         # Main system prompt
│
├── utils/
│   ├── database.py             # Database connection utilities
│   ├── response_formatter.py   # Response enhancement utilities
│   └── visualization.py        # Visualization utilities
│
├── ui/
│   ├── components.py           # UI components
│   ├── styles.py               # CSS styling
│   └── auth.py                 # Authentication & landing page
│
├── ACCESS_CODES.md             # Admin guide for managing codes
├── ALPHA_ACCESS_GUIDE.md       # User guide for alpha access
└── app.py                      # Main streamlit app
```

## License

MIT License

## Acknowledgements

Developed at Pacific Northwest National Laboratory (PNNL).