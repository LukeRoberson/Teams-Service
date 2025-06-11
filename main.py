"""
Module: main.py

Module for managing interactions with Microsoft Teams.
This service handles:
    - Sending messages to Teams chats
    - Getting chat IDs

Module Tasks:
    1. Fetch global configuration from the web interface.
    2. Set up logging based on the global configuration.
    3. Create a Flask application instance and register API endpoints.

Usage:
    This is a Flask application that should run behind a WSGI server inside
        a Docker container.
    Build the Docker image and run it with the provided Dockerfile.

Functions:
    - fetch_global_config:
        Fetches the global configuration from the web interface.
    - logging_setup:
        Sets up the root logger for the web service.
    - create_app:
        Creates the Flask application instance and sets up the configuration.

Blueprints:
    - teams_api: Handles API endpoints for Teams interactions.

Dependencies:
    - Flask: For creating the web application.
    - Flask-Session: For session management.
    - requests: For making HTTP requests to the web interface.
    - logging: For logging messages to the terminal.
    - os: For environment variable access.

Custom Dependencies:
    - api.teams_api: Contains API endpoints for Teams interactions.
    - teams_token: For managing Teams tokens.
"""


# Standard library imports
from flask import Flask
from flask_session import Session
import requests
import logging
import os

# Custom imports
from api import teams_api
from teams_token import TeamsToken


CONFIG_URL = "http://core:5100/api/config"


def fetch_global_config(
    url: str = CONFIG_URL,
) -> dict:
    """
    Fetch the global configuration from the core service.

    Args:
        url (str): The URL to fetch the global configuration from.

    Returns:
        dict: The global configuration loaded from the core service.

    Raises:
        RuntimeError: If the global configuration cannot be loaded.
    """

    global_config = None
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        global_config = response.json()

    except Exception as e:
        logging.critical(
            "Failed to fetch global config from core service."
            f" Error: {e}"
        )

    if global_config is None:
        raise RuntimeError("Could not load global config from core service")

    return global_config['config']


def logging_setup(
    config: dict,
) -> None:
    """
    Set up the root logger for the web service.

    Args:
        config (dict): The global configuration dictionary

    Returns:
        None
    """

    # Get the logging level from the configuration (eg, "INFO")
    log_level_str = config['web']['logging-level'].upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    # Set up the logging configuration
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logging.info("Logging setup complete with level: %s", log_level)


def create_app(
    config: dict,
    token_manager: TeamsToken,
) -> Flask:
    """
    Create the Flask application instance and set up the configuration.
    Registers the necessary blueprints for the web service.

    Args:
        config (dict): The global configuration dictionary.
        token_manager (TeamsToken): The Teams token manager instance.

    Returns:
        Flask: The Flask application instance.
    """

    # Create the Flask application
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('api_master_pw')
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = '/app/flask_session'
    app.config['GLOBAL_CONFIG'] = config
    app.config['TOKEN_MANAGER'] = token_manager
    Session(app)

    # Register blueprints
    app.register_blueprint(teams_api)

    return app


# Config and logging setup
global_config = fetch_global_config(CONFIG_URL)
logging_setup(global_config)

# Setup the Teams token manager
token_manager = TeamsToken()
token_manager.get_token()

# Create the Flask application
app = create_app(
    config=global_config,
    token_manager=token_manager,
)
