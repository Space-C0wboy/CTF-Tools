import socket
import json

def send_command(command_data):
    """
    Sends a command to the server and receives a response.

    :param command_data: A dictionary containing the command data.
    :return: The server's response as a JSON object.
    """
    host = '83.136.249.237'  # Update with actual server's hostname or IP address
    port = 52404             # Update with actual port used by the server
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
        except socket.error as err:
            print(f"Connection error: {err}")
            return None

        s.sendall(json.dumps(command_data).encode('utf-8'))
        
        data = b''
        try:
            while True:
                part = s.recv(1024)
                if not part:
                    break
                data += part
                if data.endswith(b']'):
                    break
        except socket.error as err:
            print(f"Receiving error: {err}")
            return None

        try:
            response = json.loads(data.decode('utf-8'))
        except json.JSONDecodeError as err:
            print(f"JSON decode error: {err}")
            return None

    return response

def read_flash_memory(address, length):
    """
    Reads data from the flash memory chip starting at the specified address and converts it to a flag.

    :param address: The starting address (24 bits) as an integer.
    :param length: The number of bytes to read.
    """
    address_bytes = address.to_bytes(3, byteorder='big')
    command = [0x03] + list(address_bytes)
    
    command_data = {
        "tool": "pyftdi",
        "cs_pin": 0,
        "url": 'ftdi://ftdi:2232h/1',
        "data_out": [hex(x) for x in command],
        "readlen": length
    }
    
    response = send_command(command_data)
    if response:
        # Convert the list of integer values to characters and concatenate them to form a string
        flag = ''.join(chr(byte) for byte in response if byte != 255)  # Exclude the 0xFF padding bytes
        print(f"Flag: {flag}")
    else:
        print("Failed to read data or decode the flag.")

# Example: Read 256 bytes of data starting from address 0x000000 to try and retrieve the flag
read_flash_memory(0x000000, 256)
