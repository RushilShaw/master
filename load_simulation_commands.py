import GpsUtils
import pathlib
import sys


def main(**kwargs):
    # get configuration path_to_file variable
    path_to_file = kwargs.get("path_to_file")
    command_file = pathlib.Path(path_to_file)
    if not command_file.is_file():
        raise FileNotFoundError("path_to_file variable is invalid")

    # list all functions that will be sent to GPS
    initialization_commands = [
        "SIM:COM STOP",
        "SIM:POS:MOTION:ZEROIZE"
    ]
    final_commands = [
        "SIM:POS:MOTION:READ 1",
        "SIM:POS:MODE MOTION",
    ]

    # initialize GPS instance
    gps = GpsUtils.ClawGPSSimulator()

    # send commands to GPS
    gps.stream_list_of_commands(initialization_commands)
    gps.stream_file(command_file)
    gps.stream_list_of_commands(final_commands)

    return "PY_SUCCESS"


if __name__ == '__main__':
    main(path_to_file=sys.argv[1])
