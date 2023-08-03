import sys, os
import json
import GpsUtils
import stream_file
import gps_location_and_datetime_setter


def main():
    command_line_arguments = sys.argv[1:]
    command_line_arguments_combined = "".join(command_line_arguments)
    configuration_variables = json.loads(command_line_arguments_combined)

    if configuration_variables.get("command") is None:
        sys.exit(os.EX_CONFIG)

    command = configuration_variables["command"]

    if command == "motion":
        stream_file.main(**configuration_variables)

    elif command == "fixed":
        gps_location_and_datetime_setter.main(**configuration_variables)

    elif command == "start":
        gps = GpsUtils.ClawGPSSimulator()
        gps.send_command("SIM:COM START")

    elif command == "stop":
        gps = GpsUtils.ClawGPSSimulator()
        gps.send_command("SIM:COM STOP")


if __name__ == '__main__':
    main()
