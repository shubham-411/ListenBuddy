from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, emit
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

adjectives = ["Swift", "Silent", "Curious", "Brave", "Mighty", "Clever", "Gentle", "Wild", "Happy", "Calm"]
animals = ["Lion", "Tiger", "Fox", "Panda", "Wolf", "Eagle", "Dolphin", "Bear", "Hawk", "Rabbit"]
waiting_users = []   
active_rooms = {}    
user_rooms = {}     
def generate_anonymous_name():
    return f"{random.choice(adjectives)} {random.choice(animals)}"

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('join')
def handle_join(data):
    role = data['role']
    sid = request.sid
    username = generate_anonymous_name()   

    new_user = {'sid': sid, 'username': username, 'role': role}
    print(f"[JOIN] {username} ({role}) joined with sid={sid}")

  
    partner = None
    for user in waiting_users:
        if user['role'] != role: 
            partner = user
            break

    if partner:  
        room = f"room_{partner['sid']}_{sid}"
        join_room(room, sid=partner['sid'])
        join_room(room, sid=sid)
        active_rooms[room] = [partner['sid'], sid]
        user_rooms[partner['sid']] = room
        user_rooms[sid] = room
        print(f"[MATCHED] {username} ({role}) <--> {partner['username']} ({partner['role']}) in {room}")

        emit('matched', {'room': room, 'partner': username, 'your_username': partner['username']}, room=partner['sid'])
        emit('matched', {'room': room, 'partner': partner['username'], 'your_username': username}, room=sid)
        waiting_users.remove(partner)

    else: 
        waiting_users.append(new_user)
        emit('waiting', {'message': f'Hello {username}, waiting for a partner...'}, room=sid)

@socketio.on('send_message')
def handle_send_message(data):
    room = data['room']
    msg = {'username': data['username'], 'message': data['message']}
    emit('message', msg, room=room, include_self=False)


@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid

    for user in list(waiting_users):  
        if user['sid'] == sid:
            waiting_users.remove(user)
            print(f"[DISCONNECT] {user['username']} removed from waiting")
            return

    if sid in user_rooms:
        room = user_rooms[sid]
        if room in active_rooms:
            users = active_rooms[room]
            partner_sid = [u for u in users if u != sid][0]

            emit('partner_left', {}, room=partner_sid)
            print(f"[DISCONNECT] {sid} left {room}, partner {partner_sid} notified")

            del active_rooms[room]

        del user_rooms[sid]


if __name__ == '__main__':
    socketio.run(app, debug=True)
