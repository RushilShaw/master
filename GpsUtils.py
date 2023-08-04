import serial
import time
import pathlib
import serial.tools.list_ports


class ClawGPSSimulator:
    GPS_DEVICE_NAME = "Silicon Labs CP210x USB to UART Bridge"
    BAUD = 115200
    PORT: serial.Serial
    PORT_INITIALIZATION_DELAY_SECONDS = 1.0

    def __init__(self, port_name=None):
        if port_name is None:
            port_name = self.detect_device_port()
        self.PORT = serial.Serial(port=port_name, baudrate=self.BAUD)

    def detect_device_port(self):
        for port in serial.tools.list_ports.comports():
            if port.description.startswith(self.GPS_DEVICE_NAME):
                return port.name

    def stream_file(self, command_filepath: pathlib.Path):
        with (
            open(command_filepath, 'r') as file,
            self.PORT as ser
        ):
            time.sleep(self.PORT_INITIALIZATION_DELAY_SECONDS)
            ser.flushInput()
            for line in file.readlines():
                encoded_command = f"{line.strip()}\r".encode()
                ser.write(encoded_command)
                full_response = b""
                while not full_response.endswith(b"scpi > "):
                    bytes_to_read = ser.inWaiting()
                    response = ser.read(bytes_to_read)
                    full_response += response
                    time.sleep(0.01)
                if full_response.endswith(b"Command Error\r\nscpi > "):
                    raise ValueError(f"{line.strip()} -> caused an SCPI Error")

    def stream_list_of_commands(self, commands: list[str]):
        with self.PORT as ser:
            time.sleep(self.PORT_INITIALIZATION_DELAY_SECONDS)
            for command in commands:
                encoded_command = f"{command}\r".encode()
                ser.write(encoded_command)
                full_response = b""
                while not full_response.endswith(b"scpi > "):
                    bytes_to_read = ser.inWaiting()
                    response = ser.read(bytes_to_read)
                    full_response += response
                    time.sleep(0.01)
                if full_response.endswith(b"Command Error\r\nscpi > "):
                    raise ValueError(f"{command} -> caused an SCPI Error")

    def send_command(self, command: str) -> bytes:
        with self.PORT as ser:
            time.sleep(self.PORT_INITIALIZATION_DELAY_SECONDS)
            ser.flushInput()
            encoded_command = f"{command}\r".encode()
            ser.write(encoded_command)
            full_response = b""
            while not full_response.endswith(b"scpi > "):
                bytes_to_read = ser.inWaiting()
                response = ser.read(bytes_to_read)
                full_response += response
                time.sleep(0.01)
        return full_response[len(encoded_command)+1:-9]
