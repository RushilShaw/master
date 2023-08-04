import sys
import GpsUtils
import gps_location_and_datetime_setter


def main(**kwargs):
    gps = GpsUtils.ClawGPSSimulator()
    datetime_commands = gps_location_and_datetime_setter.generate_datetime_commands(kwargs.get("NEW_DATETIME_ISO_8601"))

    gps.stream_list_of_commands(datetime_commands)

    current_state = gps.send_command("SIM:COM STATE?")
    if current_state == "RUNNING":
        return "PY_SUCCESS"

    gps.send_command("SIM:COM START")

    if current_state == "STARTING":
        current_state = gps.send_command("SIM:COM STATE?")

    if current_state == "RUNNING":
        return "PY_SUCCESS"
    else:
        return "PY_FATAL_EXCEPTION"


if __name__ == '__main__':
    main(NEW_DATETIME_ISO_8601=sys.argv[1])
