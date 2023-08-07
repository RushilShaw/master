import sys
import json
import gps_starter
import gps_stopper
import load_simulation_commands
import gps_location_and_datetime_setter


def main():
    command_to_script = {
        "motion": load_simulation_commands,
        "fixed": gps_location_and_datetime_setter,
        "start": gps_starter,
        "stop": gps_stopper
    }

    try:
        command_line_json_arguments = sys.argv[1]
        configuration_variables = json.loads(command_line_json_arguments)
        command = configuration_variables["command"]
        script = command_to_script[command]
        return_code = script.main(**configuration_variables)
        print(return_code)

    except:
        print("PY_FATAL_EXCEPTION")
        # raise


if __name__ == '__main__':
    main()
