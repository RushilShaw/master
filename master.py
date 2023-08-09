import sys
import json
import gps_starter
import gps_stopper
import gps_location_setter
import load_simulation_commands


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
        command_line_json_arguments = sys.argv[1]
        configuration_variables = json.loads(command_line_json_arguments)
        command = configuration_variables["command"]
        script = command_to_script[command]
        return_code = script.main(**configuration_variables)

        output["response"] = return_code
        output["description"] = "" if return_code == "PY_SUCCESS" else "unexpected response exception"

    except Exception as error:
        output["response"] = "PY_FATAL_EXCEPTION"
        output["description"] = f"{error.__class__.__name__} : {error.with_traceback(None)}"

    finally:
        print(json.dumps(output))


if __name__ == '__main__':
    main()
