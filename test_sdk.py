from shipsafe_sdk import ShipSafe

shipsafe = ShipSafe(
    "B8ZMPuB0s1UWuRepq-EIzTwQOC8Mbt0LsB8GsXyhs1s",
    4
)

result = shipsafe.is_flag_enabled("new_checkout")

print(result)