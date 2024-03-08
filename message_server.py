import zmq

class MessageServer:
    def __init__(self):
        self.context = zmq.Context()

        # Adding message_server's socket details
        self.message_server_REPsocket = self.context.socket(zmq.REP)
        self.message_server_REPsocket.bind("tcp://*:5510")
        
        self.groups = {}  # Dictionary to store group details

    def handle_group_registration(self, group_id, ip_address):
        if group_id not in self.groups:
            self.groups[group_id] = ip_address
            print(f"Group '{group_id}' registered with IP Address: {ip_address}")
            self.message_server_REPsocket.send_string("SUCCESS")
            return "SUCCESS"
        else: 
            return "FAILURE - Group already exists"

    def handle_user_request(self, request):
        if request.get("type") == "GetGroupList":
            group_list = "\n".join([f"{group} - {ip}" for group, ip in self.groups.items()])
            return group_list
        # Handle other user requests like joinGroup, LeaveGroup, GetMessage, SendMessage, etc.

    def run(self):
        print("server strats listening\n")
        while True:
        
            # Listen for incoming messages from groups and users
            message = self.message_server_REPsocket.recv_json()
            print(f"Received message: {message}")
            
            if message.get("type") == "RegisterGroup":
                # handle group registration
                group_id= message.get("group_id")
                ip_address= message.get("ip_address")
                response = self.handle_group_registration(group_id, ip_address)

server = MessageServer()
server.run()


# if group_msg_parts[0] == 'JOIN':
            #     group_name = group_msg_parts[1]
            #     ip_address = group_msg_parts[2]
            #     response = self.handle_group_registration(group_name, ip_address)
            #     self.group_socket.send_string(f"{response} {group_name}")