import sys
import json
import GpsUtils
import gps_starter
import gps_stopper
import gps_location_setter
import load_simulation_commands


class InputError(Exception):
    pass


def main():
    command_to_script = {
        "motion": load_simulation_commands,
        "fixed": gps_location_setter,
        "start": gps_starter,
        "stop": gps_stopper
    }
    output = {
        "response": None,
        "description": None
    }

    try:
        if len(sys.argv) != 2:
            raise InputError("Must have one and only one command line argument")
        command_line_json_arguments = sys.argv[1]

        configuration_variables = json.loads(command_line_json_arguments)

        command = configuration_variables.get("command")
        if command is None:
            raise InputError(f"json string must *command* key")

        script = command_to_script.get(command)
        if script is None:
            raise InputError(f"Valid command keys are {''.join(command_to_script.keys())}")

        return_code = script.main(**configuration_variables)

        output["response"] = return_code
        output["description"] = "" if return_code == "PY_SUCCESS" else "unexpected response exception"

    except (json.JSONDecodeError, InputError) as error:
        incorrect_input_message = "Please reference documentation on instruction for the proper json input string."
        output["response"] = "PY_INCORRECT_INPUT"
        output["description"] = f"{error.__class__.__name__} : {error.with_traceback(None)}. {incorrect_input_message}"

    except (GpsUtils.GPSNotDetected, GpsUtils.GPSPortInUse) as error:
        output["response"] = "PY_GPS_DEVICE_NOT_CONNECTED"
        output["description"] = f"{error.__class__.__name__} : {error.with_traceback(None)}"

    except GpsUtils.CommandsFileNotFound as error:
        output["response"] = "PY_GPS_ROUTE_FILE_NOT_PRESENT"
        output["description"] = f"{error.__class__.__name__} : {error.with_traceback(None)}"

    except Exception as error:
        output["response"] = "PY_FATAL_EXCEPTION"
        output["description"] = f"{error.__class__.__name__} : {error.with_traceback(None)}"

    finally:
        print(json.dumps(output))


if __name__ == '__main__':
    main()
