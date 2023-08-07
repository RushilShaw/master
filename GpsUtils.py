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
            port_name = self.detect_device_port()
        self.PORT = serial.Serial(port=port_name, baudrate=self.BAUD)

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
