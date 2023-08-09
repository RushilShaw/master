import serial
import time
import pathlib
import serial.tools.list_ports


class ClawGPSSimulator:
    GPS_DEVICE_NAME = "Silicon Labs CP210x USB to UART Bridge"
    BAUD = 115200
    PORT: serial.Serial
    PORT_INITIALIZATION_DELAY_SECONDS = 0.5

    def __init__(self, port_name=None):
        if port_name is None:
            detected_port_name = self.detect_device_port()
            if detected_port_name is None:
                raise Exception(f"GPS is not connected to this PC or is not named {self.GPS_DEVICE_NAME}")
            port_name = detected_port_name

        self.PORT = serial.Serial(port=port_name, baudrate=self.BAUD)

        if not self.PORT.is_open:
            not_open_error = serial.serialutil.PortNotOpenError()
            not_open_error.args = (*not_open_error.args, "Did you forget to close SIMCOM?")
            raise not_open_error

    def detect_device_port(self):
        for port in serial.tools.list_ports.comports():
            if port.description.startswith(self.GPS_DEVICE_NAME):
                return port.name

    def stream_file(self, commands_filepath: pathlib.Path):
        with (
            open(commands_filepath, 'r') as file,
            self.PORT as ser
        ):
            time.sleep(self.PORT_INITIALIZATION_DELAY_SECONDS)
            ser.flushInput()
            for line in file.readlines():
                encoded_command = f"{line.strip()}\r".encode()
                ser.write(encoded_command)
                ser.read_until(b"scpi > ")

    def stream_list_of_commands(self, commands: list[str]):
        with self.PORT as ser:
            time.sleep(self.PORT_INITIALIZATION_DELAY_SECONDS)
            ser.flushInput()
            for command in commands:
                encoded_command = f"{command.strip()}\r".encode()
                ser.write(encoded_command)
                ser.read_until(b"scpi > ")

    def send_command(self, command: str) -> bytes:
        with self.PORT as ser:
            time.sleep(self.PORT_INITIALIZATION_DELAY_SECONDS)
            ser.flushInput()
            encoded_command = f"{command.strip()}\r".encode()
            ser.write(encoded_command)
            response = ser.read_until(b"scpi > ")
        return response[len(encoded_command)+1:-7]
