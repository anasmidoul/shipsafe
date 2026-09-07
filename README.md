# ShipSafe

ShipSafe is a feature flag management system that allows developers to create projects, manage feature flags, and check feature flag status through an API or Python SDK.

Feature flags allow developers to control whether a feature is enabled without having to change the application code each time. With ShipSafe, a developer can create a project, create feature flags, and enable or disable them from the ShipSafe dashboard. Applications can then check the current status of a flag through the API or the Python SDK.

## Installation

ShipSafe is built with Python, Flask, SQLite, JavaScript, HTML, and CSS.

To run ShipSafe locally, first make sure Python 3 is installed. Initialize the database by running:

python3 database.py

Then start the Flask application:

python3 app.py

The application will then be available at:

http://127.0.0.1:5000

The Python SDK can be installed with:

pip install shipsafe-sdk

## Getting Started

1. Register for a ShipSafe account.
2. Create a project.
3. Create feature flags inside the project.
4. Copy the project's API key.
5. Use the API key and project ID with the ShipSafe SDK or API.

## Usage

The Python SDK provides a simple way for an application to check whether a feature flag is enabled:

from shipsafe_sdk import ShipSafe

shipsafe = ShipSafe("YOUR_API_KEY", YOUR_PROJECT_ID)

enabled = shipsafe.is_flag_enabled("new_checkout")

print(enabled)

The SDK returns True if the feature flag is enabled and False if it is disabled.

For example:

from shipsafe_sdk import ShipSafe

shipsafe = ShipSafe("YOUR_API_KEY", 1)

if shipsafe.is_flag_enabled("new_checkout"):
    print("New checkout is enabled!")
else:
    print("New checkout is disabled.")

## API

ShipSafe also provides an API for checking whether a feature flag is enabled.

Send a GET request to:

/api/projects/<project_id>/flags/<flag_name>

The request must include the project's API key in the X-API-Key header.

For example, a successful response is:

{
    "enabled": 1
}

An enabled flag returns 1, while a disabled flag returns 0.

The API checks that the provided API key belongs to the requested project before returning the flag status.

## How It Works

ShipSafe consists of a Flask web application, a SQLite database, a JavaScript frontend, a REST API, and a Python SDK.

A user first creates an account and logs in. Users can then create projects. Each project has its own randomly generated API key. Feature flags belong to projects and can be enabled or disabled through the dashboard.

When an application uses the API or Python SDK to check a feature flag, ShipSafe verifies the project's API key and looks up the flag in the SQLite database. The current enabled status is then returned to the application.

This allows a developer to change the state of a feature without changing the application's source code or redeploying it.

## Files

### app.py

Contains the main Flask application. It handles user registration and login, project creation, feature flag creation, enabling and disabling flags, deleting flags, and serving the API endpoint. It also contains the authentication and authorization checks that prevent users from accessing other users' projects.

### database.py

Creates the SQLite database tables used by ShipSafe. It creates tables for users, projects, and feature flags, including the relationships and uniqueness constraints between them.

### shipsafe_sdk/sdk.py

Contains the Python SDK. The ShipSafe class allows another Python application to check a feature flag through the ShipSafe API using a project ID and API key.

### shipsafe_sdk/__init__.py

Exposes the ShipSafe class so it can be imported directly with:

from shipsafe_sdk import ShipSafe

### templates/

Contains the HTML templates used by the Flask application, including the login, registration, project list, project detail, and home pages.

### static/script.js

Contains the JavaScript used by the frontend. It handles actions such as copying an API key, confirming flag deletion, and enabling or disabling feature flags without requiring a full page reload.

### static/style.css

Contains the CSS used to style the ShipSafe interface.

### test_sdk.py

A simple test program used to verify that the Python SDK can successfully communicate with the ShipSafe API and correctly return the feature flag status.

### pyproject.toml

Contains the Python package configuration for the ShipSafe SDK.

### DESIGN.md

Contains the technical design documentation for ShipSafe, including its architecture, database design, authentication and security decisions, API, SDK, and testing approach.

## Design Decisions

I chose Flask because it provides the tools needed to build the web application and API while keeping the project relatively simple and understandable.

I chose SQLite as the database because ShipSafe is a small application and SQLite provides a straightforward way to store users, projects, and feature flags without requiring a separate database server.

I used API keys to authenticate requests from applications using the ShipSafe API. Each project has its own API key, which keeps projects separated and allows an application to access the feature flags belonging to that project.

I also added ownership checks to the application so that users can only access and modify their own projects and feature flags. Database constraints are used in addition to application checks to prevent duplicate project and feature flag names.

The Python SDK was added to make the API easier to use from Python applications. Instead of requiring a developer to manually construct HTTP requests, the SDK provides the is_flag_enabled method as a simple interface.

## Technologies

- Python
- Flask
- SQLite
- JavaScript
- HTML/CSS
- Python SDK

## Demo

[Watch the ShipSafe demo](https://youtu.be/c66Rpc2iatA)

ShipSafe — Anas — CS50 Final Project — 2026