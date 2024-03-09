import socket
import time
import re

def main():
    host = '94.237.61.203'
    port = 34323

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        # Receive the welcome message and additional info
        welcome_message = receive_until_prompt(s, "Are you ready? (y/n)")
        print(welcome_message)

        # Start the game
        s.sendall(b'Y\n')
        time.sleep(1)  # Short delay to allow the server to respond

        # Now, handle the game responses
        handle_game(s)

def handle_game(s):
    while True:
        # Receive scenario from the server
        scenario = receive_until_prompt(s, "What do you do?", wait_for_more_data=True)
        print(scenario)

        actions_needed = re.findall(r'GORGE|PHREAK|FIRE', scenario)
        if actions_needed:
            action_response = '-'.join(map(response_to_action, actions_needed))
            print("Sending:", action_response)
            s.sendall((action_response + '\n').encode())
        else:
            # If no more actions needed, listen for any final messages (like the flag)
            listen_for_final_message(s)
            break

def listen_for_final_message(s):
    print("Listening for any final message...")
    while True:
        data = s.recv(1024).decode()
        if not data:
            break
        print(data)

def receive_until_prompt(s, prompt, wait_for_more_data=False):
    total_data = []
    while True:
        data = s.recv(1024).decode()
        total_data.append(data)
        if prompt in data or (wait_for_more_data and not data):
            break
    return ''.join(total_data)

def response_to_action(action):
    return {
        "GORGE": "STOP",
        "PHREAK": "DROP",
        "FIRE": "ROLL"
    }[action]

if __name__ == "__main__":
    main()
