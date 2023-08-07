import sys
import time
import GpsUtils
from datetime import datetime, timezone


def generate_datetime_commands(new_datetime_iso_8601: str) -> list[str]:
    """
    generate_datetime_commands func: creates a list of the commands needed to set the new datetime on the CLAW GPS
    """
    if new_datetime_iso_8601 is None:
        new_datetime = datetime.now(timezone.utc)
    else:
        new_datetime = datetime.fromisoformat(new_datetime_iso_8601)

    gps_commands = [
        "SIM:TIME:MODE ASSIGN",
        f"SIMulation:TIME:START:TIME {new_datetime.hour},{new_datetime.minute},{new_datetime.second}",
        f"SIMulation:TIME:START:DATE {new_datetime.year},{new_datetime.month},{new_datetime.day}"
    ]
    return gps_commands


def main(**kwargs):
    gps = GpsUtils.ClawGPSSimulator()
    new_datetime = kwargs.get("NEW_DATETIME_ISO_8601")
    datetime_commands = generate_datetime_commands(new_datetime)

    gps.send_command("SIM:COM STOP")

    gps.stream_list_of_commands(datetime_commands)

    gps.send_command("SIM:COM START")

    for _ in range(10):
        current_state = gps.send_command("SIM:STATE?")
        if current_state == b"RUNNING\r\n":
            return "PY_SUCCESS"
        time.sleep(0.5)

    return "PY_FATAL_EXCEPTION"


if __name__ == '__main__':
    main(NEW_DATETIME_ISO_8601=sys.argv[1] if len(sys.argv) == 2 else None)
