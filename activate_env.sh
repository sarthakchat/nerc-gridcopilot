#!/bin/bash

# Load .env file variables
export $(grep -v '^#' .env | xargs)

# Print confirmation
echo "Environment variables from .env have been loaded!"
echo "DB_PATH: $DB_PATH"
echo "OPENAI_API_BASE: $OPENAI_API_BASE"
echo "OPENAI_MODEL: $OPENAI_MODEL"