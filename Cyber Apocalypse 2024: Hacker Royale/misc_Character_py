import socket

def connect_to_server(ip, port):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((ip, port))
        return server
    except socket.error as e:
        print(f"Failed to connect to {ip}:{port}, error: {e}")
        return None

def get_flag_character_by_character(server):
    if not server:
        print("Server connection not established.")
        return ""

    secret = ''
    index = 0
    while True:
        try:
            # Send the index to the server
            server.sendall(f"{index}\n".encode())

            # Receive the response from the server
            response = server.recv(1024).decode()  # Adjust buffer size if necessary
            
            # Check if response is empty or null
            if not response:
                print("No response received from the server.")
                break
            
            # Extract the character from the response
            char = response.strip()  # Extract the character received
            
            if not char:
                break  # Stop if no character is returned or response is only whitespace
            
            print(f"Received: {char}")  # For debugging
            
            secret += char
            index += 1
        except socket.error as e:
            print(f"Failed to communicate with the server, error: {e}")
            break

    return secret

ip_address = 'HOST'
port = PORT 

# Attempt to connect to the server
server = connect_to_server(ip_address, port)

if server:
    # Initial connection and prompt handling
    try:
        prompt = server.recv(1024).decode()  # Adjust buffer size if necessary
        print(prompt)  # Display the initial prompt from the server
    except socket.error as e:
        print(f"Failed to receive initial prompt, error: {e}")
    
    # Retrieve the secret
    secret = get_flag_character_by_character(server)
    print("\nComplete secret:", secret)

    # Clean up and close the connection
    server.close()
else:
    print("Unable to proceed without a server connection.")
