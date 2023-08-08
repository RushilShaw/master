import GpsUtils
import sys


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
        kwargs["Longitude"],
        kwargs["Latitude"],
        kwargs["Altitude_meters"]
    )

    gps.send_command("SIM:COM STOP")
    gps.stream_list_of_commands(location_commands)

    return "PY_SUCCESS"


if __name__ == '__main__':
    main(Longitude=float(sys.argv[1]), Latitude=float(sys.argv[2]), Altitude_meters=float(sys.argv[3]))
