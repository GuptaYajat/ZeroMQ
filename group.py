import zmq
import sys
import time
import threading

class Group:
    def __init__(self, group_id, port_number):       
        self.context = zmq.Context()
        self.group_id = group_id
        self.port_number = port_number
        self.server_port_number = "5510"

    def register_with_server(self):
        group_server_socket= self.context.socket(zmq.REQ)
        group_server_socket.connect("tcp://localhost:5570")
        group_server_socket.send_json({"type": "RegisterGroup", "group_id": self.group_id, "ip_address": f"tcp://localhost:{self.port_number}"})
        response = group_server_socket.recv_string()
        print(f"Server response: {response}")
        # close the socket
        group_server_socket.close()            

    def handle_user_request(self, request):
        if request.get("type") == "joinGroup":
            user_id = request.get("user_id")
            self.users.add(user_id)
            return "SUCCESS"
        elif request.get("type") == "leaveGroup":
            user_id = request.get("user_id")
            if user_id in self.users:
                self.users.remove(user_id)
                return "SUCCESS"
            else:
                return "FAILURE - User not in group"
            
        # Handle other user requests like GetMessage, SendMessage, etc.

    def run(self):
        while True:
            # Listen for incoming messages from users
            user_msg = self.user_socket.recv()
            print(f"Received message from user: {user_msg}")
            # Handle user messages


# take group_name and port_number as command line arguments
group_id = sys.argv[1]
port_number = sys.argv[2]

group = Group(group_id, port_number)
group.register_with_server()