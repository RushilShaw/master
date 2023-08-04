import GpsUtils
from datetime import datetime, timezone


def generate_location_commands(longitude_degrees: float, latitude_degrees: float, altitude_meters: float) -> list[str]:
    """
    generate_location_commands func: creates a list of the commands needed to set the new location on the CLAW GPS
    """
    gps_commands = [
        "SIM:POS:MODE FIXED",
        f"SIMulation:POSition:LLH {longitude_degrees},{latitude_degrees},{altitude_meters}",
    ]
    return gps_commands


def generate_datetime_commands(new_datetime_iso_8601: str) -> list[str]:
    """
    generate_datetime_commands func: creates a list of the commands needed to set the new datetime on the CLAW GPS
    """
    if new_datetime_iso_8601 is None:
        new_datetime = datetime.now(timezone.utc)
    else:
        new_datetime = datetime.fromisoformat(new_datetime_iso_8601)

    gps_commands = [
        "SIM:TIME:MODE ASSIGN"
        f"SIMulation:TIME:START:TIME {new_datetime.hour},{new_datetime.minute},{new_datetime.second}",
        f"SIMulation:TIME:START:DATE {new_datetime.year},{new_datetime.month},{new_datetime.day}"
    ]
    return gps_commands


def main(**kwargs):
    gps = GpsUtils.ClawGPSSimulator()

    commands = generate_location_commands(
        kwargs["LONGITUDE_DEGREES"],
        kwargs["LATITUDE_DEGREES"],
        kwargs["ALTITUDE_METERS"]
    )
    if "DATETIME_ISO_8601" in kwargs:
        commands += generate_datetime_commands(kwargs["DATETIME_ISO_8601"])

    gps.stream_list_of_commands(commands)

    return "PY_SUCCESS"


if __name__ == '__main__':
    main()
