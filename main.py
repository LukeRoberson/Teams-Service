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
    - sdk.Config: For managing configuration settings.
"""


# Standard library imports
from flask import Flask
from flask_session import Session
import logging
import os

# Custom imports
from api import teams_api
from teams_token import TeamsToken
from sdk import Config


CONFIG_URL = "http://core:5100/api/config"


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
    app.config['TOKEN_MANAGER'] = token_manager
    Session(app)

    # Register blueprints
    app.register_blueprint(teams_api)

    return app


# Config and logging setup
global_config = {}
with Config(CONFIG_URL) as config:
    global_config = config.read()

logging_setup(global_config)

# Setup the Teams token manager
token_manager = TeamsToken()
token_manager.get_token()

# Create the Flask application
app = create_app(
    token_manager=token_manager,
)
