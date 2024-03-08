import zmq
import time

class User:
    def __init__(self, user_id):
        self.context = zmq.Context()

        self.user_REQsocket = self.context.server_socket(zmq.REQ)
        self.user_REQsocket.connect("tcp://localhost:5550")

        self.user_SUBsocket = self.context.socket(zmq.SUB)
        self.user_SUBsocket.bind("tcp://*:5551")

        self.group_ids = set()
        self.user_id = user_id

    def join_group(self):
        self.server_socket.send_json({"type": "joinGroup", "group_id": self.group_id, "user_id": self.user_id})
        response = self.server_socket.recv_string()
        print(f"Server response: {response}")

    def leave_group(self):
        self.server_socket.send_json({"type": "leaveGroup", "group_id": self.group_id, "user_id": self.user_id})
        response = self.server_socket.recv_string()
        print(f"Server response: {response}")

    def send_message(self, group_id, message):
        message_data = {"type": "sendMessage", "group_id": group_id, "user_id": self.user_id, "message": message}
        self.server_socket.send_json(message_data)
        response = self.server_socket.recv_string()
        print(f"Server response: {response}")

    def get_messages(self, group_id, timestamp=None):
        message_request = {"type": "getMessage", "group_id": group_id, "user_id": self.user_id, "timestamp": timestamp}
        self.server_socket.send_json(message_request)
        messages = self.server_socket.recv_json()
        print(f"Messages: {messages}")

if __name__ == "__main__":
    group_id = "Group1"  # Replace with group ID
    user_id = "User1"  # Replace with user ID

    user = User(user_id)
    user.join_group(group_id)
    
    user.send_message(group_id, "Hello, group!")  
    user.get_messages(group_id)