from shipsafe_sdk import ShipSafe

shipsafe = ShipSafe(
    "YOUR_API_KEY",
    ID_OF_YOUR_PROJECT,
)

result = shipsafe.is_flag_enabled("YOUR_FLAG")

assert result is False
print("Test passed")