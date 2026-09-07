# ShipSafe

ShipSafe is a feature flag management system that allows developers to create projects, manage feature flags, and check feature flag status through an API or Python SDK.

## Installation

Install the ShipSafe Python SDK with:

```bash
pip install shipsafe-sdk
```

## Usage

```python
from shipsafe_sdk import ShipSafe

shipsafe = ShipSafe("YOUR_API_KEY", YOUR_PROJECT_ID)

enabled = shipsafe.is_flag_enabled("new_checkout")

print(enabled)
```

The SDK returns `True` if the feature flag is enabled and `False` if it is disabled.

## API

ShipSafe also provides an API for checking whether a feature flag is enabled.

Send a GET request to:

`/api/projects/<project_id>/flags/<flag_name>`

Include your API key in the `X-API-Key` header.

### Example Response

```json
{
    "enabled": 1
}
```

An enabled flag returns `1`, while a disabled flag returns `0`.

## Getting Started

1. Register for a ShipSafe account.
2. Create a project.
3. Create feature flags inside the project.
4. Copy the project's API key.
5. Use the API key and project ID with the ShipSafe SDK.

### Example

```python
from shipsafe_sdk import ShipSafe

shipsafe = ShipSafe("YOUR_API_KEY", 1)

if shipsafe.is_flag_enabled("new_checkout"):
    print("New checkout is enabled!")
else:
    print("New checkout is disabled.")
```

## Technologies

- Python
- Flask
- SQLite
- JavaScript
- HTML/CSS
- Python SDK

## How It Works

ShipSafe provides a dashboard where developers can create projects and feature flags. Each project has an API key that can be used to check feature flag status through the ShipSafe API or Python SDK.

## Demo

[Watch the ShipSafe demo](https://youtu.be/PKwlmm_qhew)

ShipSafe — Anas — CS50 Final Project — 2026