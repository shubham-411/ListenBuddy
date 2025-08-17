# Anonymous Chat with Matchmaking

A real-time chat application built with **Flask** and **Socket.IO**, where two users are matched based on opposite roles (🎧 Listener & 🎤 Speaker) and can chat anonymously using randomly generated animal nicknames.


# Features

*  Real-time chat powered by Flask-SocketIO
*  Anonymous usernames (random animal names)
*  Matchmaking based on roles: Listener ↔ Speaker
*  Instant notifications when partner joins/leaves
*  Clean and interactive UI with role-based chat view
* Responsive design for desktop & mobile

# Tech Stack

* **Backend:** Flask, Flask-SocketIO (Python)
* **Frontend:** HTML, CSS, JavaScript
* **Realtime Communication:** WebSockets

# How It Works

1. User selects a **role**: Listener or Speaker.
2. The system looks for a waiting user with the **opposite role**.
3. If found → both are matched and placed in a private room.
4. If not found → the user waits until a partner arrives.
5. Users chat in real-time until one disconnects.
6. If a partner leaves, the other is notified instantly.


# Matchmaking Algorithm-

We use a *Queue-based Opposite Role Matching* algorithm:

* New user joins → check waiting queue.
* If a user with the opposite role exists → instantly match them.
* Else → add user to waiting queue.

# Benefits of This Algorithm-

* **Simple & Fast (O(1))** – no heavy computation.
* **Low Latency** – instant matches when possible.
* **Lightweight** – works efficiently with Socket.IO events.

# Future Enhancements-

* 🎥 Voice & Video calling with WebRTC
* 🧑‍🤝‍🧑 Group chat rooms
