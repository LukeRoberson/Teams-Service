"""
Main module for the MS Teams service.
"""

from flask import Flask
from flask_session import Session
import requests
import logging
import os

from api import teams_api
from teams_token import TeamsToken


# Get global config
global_config = None
try:
    response = requests.get("http://web-interface:5100/api/config", timeout=3)
    response.raise_for_status()  # Raise an error for bad responses
    global_config = response.json()

except Exception as e:
    logging.critical(
        "Failed to fetch global config from web interface."
        f" Error: {e}"
    )

if global_config is None:
    raise RuntimeError("Could not load global config from web interface")

# Set up logging
log_level_str = global_config['config']['web']['logging-level'].upper()
log_level = getattr(logging, log_level_str, logging.INFO)
logging.basicConfig(level=log_level)
logging.info("Logging level set to: %s", log_level_str)

# Setup the Teams token manager
token_manager = TeamsToken()
token_manager.get_token()

# Create the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('api_master_pw')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['GLOBAL_CONFIG'] = global_config['config']
app.config['TOKEN_MANAGER'] = token_manager
Session(app)

# Register the security API blueprint
app.register_blueprint(teams_api)
