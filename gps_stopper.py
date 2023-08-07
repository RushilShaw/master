import time

import GpsUtils


def main(**kwargs):
    gps = GpsUtils.ClawGPSSimulator()

    gps.send_command("SIM:COM STOP")

    for _ in range(10):
        current_state = gps.send_command("SIM:STATE?")
        if current_state == b"STOPPED\r\n":
            return "PY_SUCCESS"
        time.sleep(1.0)

    return "PY_FATAL_EXCEPTION"


if __name__ == '__main__':
    main()
