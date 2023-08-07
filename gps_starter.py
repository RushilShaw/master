import sys
import time
import GpsUtils
import gps_location_and_datetime_setter


def main(**kwargs):
    gps = GpsUtils.ClawGPSSimulator()
    new_datetime = kwargs.get("NEW_DATETIME_ISO_8601")
    datetime_commands = gps_location_and_datetime_setter.generate_datetime_commands(new_datetime)

    gps.stream_list_of_commands(datetime_commands)

    gps.send_command("SIM:COM START")

    for _ in range(10):
        current_state = gps.send_command("SIM:STATE?")
        if current_state == b"RUNNING\r\n":
            return "PY_SUCCESS"
        time.sleep(1)

    return "PY_FATAL_EXCEPTION"


if __name__ == '__main__':
    main(NEW_DATETIME_ISO_8601=sys.argv[1] if len(sys.argv) == 2 else None)
