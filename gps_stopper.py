import GpsUtils


def main(**kwargs):
    gps = GpsUtils.ClawGPSSimulator()

    current_state = gps.send_command("SIM:COM STATE?")
    if current_state == "STOPPED":
        return "PY_SUCCESS"

    gps.send_command("SIM:COM STOP")

    if current_state == "STOPPING":
        current_state = gps.send_command("SIM:COM STATE?")

    if current_state == "STOPPED":
        return "PY_SUCCESS"
    else:
        return "PY_FATAL_EXCEPTION"


if __name__ == '__main__':
    main()
