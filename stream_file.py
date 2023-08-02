import GpsUtils
import pathlib
import sys


def main(**kwargs):
    # get configuration variables
    path_to_file = kwargs.get("path_to_file")
    if path_to_file is None:
        path_to_file = sys.argv[1]

    # list all functions that will be sent to GPS
    initialization_commands = [
        "SIM:COM STOP",
        "SIM:POS:MOTION:ZEROIZE"
    ]
    command_file = pathlib.Path(path_to_file)
    final_commands = [
        "SIM:POS:MOTION:READ 1",
        "SIM:POS:MODE MOTION",
        "SIM:COM START"
    ]

    # initialize GPS instance
    gps = GpsUtils.ClawGPSSimulator()

    # send commands to GPS
    gps.stream_list_of_commands(initialization_commands)
    gps.stream_file(command_file)
    gps.stream_list_of_commands(final_commands)


if __name__ == '__main__':
    main()
