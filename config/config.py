import os
import urllib.parse

# Database configuration - PostgreSQL on AWS RDS
DB_HOST = os.environ.get('DB_HOST', '')
DB_NAME = os.environ.get('DB_NAME', 'main')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')

# Encode the password to handle special characters in the connection string
encoded_password = urllib.parse.quote_plus(DB_PASSWORD)

# Create PostgreSQL connection string
DB_CONNECTION_STRING = f'postgresql+psycopg2://{DB_USER}:{encoded_password}@{DB_HOST}:5432/{DB_NAME}'



# Database configuration
# DB_PATH = os.environ.get('DB_PATH', '/path/to/default/database.db')
# DB_CONNECTION_STRING = f'sqlite:///{DB_PATH}'

# API configuration
OPENAI_API_BASE = os.environ.get('OPENAI_API_BASE', 'https://policyai-openai-westus.openai.azure.com/')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-4.1')

# Prompt paths
PROMPT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts')
BASE_PROMPT_PATH = os.path.join(PROMPT_DIR, 'base_prompt.txt')

# UI Constants
APP_TITLE = "GridCoPilot"
APP_ICON = "⚡"

# Access Control - Valid Alpha Release Codes
# Add 6-character alphanumeric codes here for users who should have access
VALID_ACCESS_CODES = [
    "ALPHA1",
    "BETA01",
    "TEST99",
    "DEMO01",
    # Add more codes as needed
]
