
from flask import Flask, request, render_template, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, send, emit, disconnect
from datetime import datetime
import uuid
import json
import csv
import random
import string
import logging

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"
logging.basicConfig(filename='flask.log', level=logging.INFO)
socketio = SocketIO(app, cors_allowed_origins="*")

rooms = {
    "1": [None, None],
    "2": [None, None],
    "3": [None, None]
}

class server:
    def __init__(self):
        self.data = json.load(open("server-info.json"))
        self.host_ip = self.data["host_ip"]
        self.host_port = self.data["host_port"]
        self.debug = self.data["debug"]
        self.server_link = self.data["server_link"]
        self.save_clients = self.data["save_clients"]
        self.data_file = self.data["data_file"]

        if not self.server_link:
            self.server_link = f"http://{self.host_ip}:{self.host_port}"

        print(f"[+] host ip: {self.host_ip}")
        print(f"[+] host port: {self.host_port}")
        print(f"[+] debug: {self.debug}")
        print(f"[+] host server link: {self.server_link}")
        print(f"[+] data file: {self.data_file}")

# fetch server info
def get_server_info():
    user_count = 0
    room_count = 0
    for room, clients in rooms.items():
        room_count += 1
        user_count += len(clients)
    return (user_count, room_count)

# generate random id
def generate_id():
    existing_ids = []
    for clients in rooms.values():
        for client in clients:
            existing_ids.append(client)
    while True:
        new_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if new_string not in existing_ids:
            return "polly_" + new_string

# update the info in all client
def update_html():
    server_info = get_server_info()
    emit("update_info", {
         "users_count": server_info[0],
         "rooms_count": server_info[1]
    }, broadcast=True)

# save each's client data
def write_csv(data):
    if server.save_clients:
        csv_file = server.data_file
        current_file = list(csv.reader(open(csv_file)))
        current_time = datetime.now().strftime("%B %d, %Y %I:%M:%S %p")
        data.insert(2, current_time)
        current_file.append(data)

        with open(csv_file, "w") as file:
            writer = csv.writer(file)
            writer.writerows(current_file)

@socketio.on("connect")
def handle_connect():
    client_ip = request.remote_addr
    client_unique_id = generate_id()
    server_info = get_server_info()

    data = [client_ip, client_unique_id, "connect"]
    write_csv(data)

    emit("unique_id", {"unique_id": client_unique_id})
    update_html()

@socketio.on("join")
def handle_join(data):
    client_unique_id = data.get("unique_id")
    client_ip = request.remote_addr
    available_room = None
    client_room = None
    status = None

    # search for available room
    for room, clients in rooms.items():
        if len(clients) <= 1:
            available_room = room

    # join into available room
    if available_room:
        if len(rooms[available_room]) == 1:
            status = "paired"
        else:
            status = "waiting"

        join_room(available_room)
        rooms[available_room].append(client_unique_id)
        client_room = available_room
        print(f"client {client_unique_id} joined to room {available_room}")

    # create a new room if there is no available one
    else:
        status = "waiting"
        new_room = str(len(rooms) + 1)
        join_room(new_room)
        rooms[new_room] = [client_unique_id]
        client_room = new_room
        print(f"room {new_room} created for client {client_unique_id}")

    # send the room
    emit("room", {
         "unique_id": client_unique_id,
         "room": client_room,
         "status": status,
         "clients": [client for client in rooms[client_room]]
    }, room=client_room)

    data = [client_ip, client_unique_id, "join_room"]
    write_csv(data)
    update_html()

@socketio.on("leave_room")
def leave_room_handler(data):
    if type(data).__name__ == "dict":
        client_ip = request.remote_addr
        client_unique_id = data.get("unique_id")
        client_room = data.get("room")

        leave_room(client_room)

        # disconnect all client in the server if a pair leaves
        for room, clients in rooms.items():
            if client_unique_id in clients:
                clients.clear()

        emit("disconnect", "Stranger was disconnected.", room=client_room)
        print(f"client {client_unique_id} left the room {room}")

        data = [client_ip, client_unique_id, "leave_room"]
        write_csv(data)
        update_html()

@socketio.on("message")
def handle_message(data):
    if type(data).__name__ == "dict":
        client_ip = request.remote_addr
        client_unique_id = data.get("unique_id")
        message = data.get("message")
        room = data.get("room")

        emit("message", {
             "unique_id": client_unique_id,
             "message": message,
             "room": room
        }, room=room)

@app.route("/")
def home():
    return render_template("index.html",
                           link=server.server_link)

if __name__ == "__main__":
    server = server()
    socketio.run(app,
                 host=server.host_ip,
                 port=server.host_port,
                 debug=server.debug)

