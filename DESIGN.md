# ShipSafe Design Document

## Overview

ShipSafe is a feature flag management system built with Flask and SQLite. It allows developers to create projects, create feature flags inside those projects, enable or disable flags, and check their status through an API or Python SDK.

The main purpose of ShipSafe is to allow a feature's availability to be controlled remotely without changing the application's code.

## Architecture

ShipSafe consists of three main parts:

1. **Flask web application** — Handles authentication, projects, feature flags, and the web interface.
2. **SQLite database** — Stores users, projects, and feature flags.
3. **Python SDK and API** — Allows another Python application to check whether a feature flag is enabled.

The frontend uses HTML/CSS and JavaScript. JavaScript is used for actions such as copying an API key, confirming flag deletion, and toggling flags without reloading the page.

## Database Design

The database contains three main tables:

- `users` stores user accounts and hashed passwords.
- `projects` stores projects belonging to users and their API keys.
- `flags` stores feature flags belonging to projects.

Projects have a unique name per user, and flags have a unique name per project. Foreign keys are used to connect projects to users and flags to projects.

## Authentication and Security

Users register with a username and password. Passwords are hashed using Werkzeug before being stored in the database.

Flask sessions are used to keep track of the logged-in user. Routes that require authentication check the current session before allowing access.

Project and flag operations also verify ownership. A user can only access projects that belong to their account.

Each project receives a randomly generated API key using Python's `secrets` module. The API key is required when accessing the feature flag API.

## Feature Flags

A feature flag contains a name, an enabled status, and the project it belongs to.

Flags can be:

- Created
- Enabled
- Disabled
- Deleted

The enabled value is stored as an integer in SQLite, where `1` represents enabled and `0` represents disabled.

## API

The API provides an endpoint for checking a feature flag:

`/api/projects/<project_id>/flags/<flag_name>`

The client sends the project's API key using the `X-API-Key` request header.

The API verifies:

1. That an API key was provided.
2. That the project exists.
3. That the API key belongs to the project.
4. That the requested flag exists.

If everything is valid, the API returns the flag's enabled status as JSON.

## Python SDK

The Python SDK provides a simpler way for Python applications to communicate with the ShipSafe API.

A developer creates a `ShipSafe` object with an API key and project ID and then calls:

`is_flag_enabled("flag_name")`

The SDK sends a GET request to the ShipSafe API and returns a Python boolean:

- `True` if the flag is enabled.
- `False` if the flag is disabled.

API errors are converted into Python `ValueError` exceptions.

## Main Design Decisions

### Flask

Flask was chosen because it provides the routing, request handling, sessions, and templating needed for the project while keeping the application relatively simple.

### SQLite

SQLite was chosen because ShipSafe is a small application and does not require a separate database server. It also makes the project easy to run and test locally.

### API Keys

Each project has its own API key so that an application can authenticate with ShipSafe without using a user's login credentials.

### Server-Side Ownership Checks

Ownership is checked on the server rather than relying on the frontend. This prevents users from accessing another user's projects simply by changing a project ID in a URL.

### Python SDK

The SDK provides a convenient interface for Python applications while keeping the underlying API request details hidden from the developer using the SDK.

## Testing

The Python SDK is tested using `test_sdk.py`. The test creates a `ShipSafe` client and checks that a disabled feature flag returns `False`.

The application was also manually tested through the web interface, including registration, login, project creation, feature flag creation, enabling and disabling flags, deletion, API authentication, and user/project access restrictions.