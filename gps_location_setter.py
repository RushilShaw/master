import GpsUtils


def generate_location_commands(longitude_degrees: float, latitude_degrees: float, altitude_meters: float) -> list[str]:
    """
    generate_location_commands func: creates a list of the commands needed to set the new location on the CLAW GPS
    """
    gps_commands = [
        "SIM:POS:MODE FIXED",
        f"SIMulation:POSition:LLH {longitude_degrees},{latitude_degrees},{altitude_meters}",
    ]
    return gps_commands


def main(**kwargs):
    gps = GpsUtils.ClawGPSSimulator()

    location_commands = generate_location_commands(
        kwargs["LONGITUDE_DEGREES"],
        kwargs["LATITUDE_DEGREES"],
        kwargs["ALTITUDE_METERS"]
    )

    commands = [
        "SIM:COM STOP"
    ]
    commands.extend(location_commands)
    commands.append("SIM:POS:MODE FIXED")

    gps.stream_list_of_commands(commands)

    return "PY_SUCCESS"


if __name__ == '__main__':
    main()
