<h1 align="center">Pollify</h1>
<div align="center">
  <p>Connect to strangers anonymously</p>
  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Pollify-1.0.0-red?style=for-the-badge">
  <img src="https://img.shields.io/badge/Python-3.11.6-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/Flask-3.0.0-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Werkzeug-3.0.1-blue?style=for-the-badge">
</div>


## Description
Chat and meet strangers anonymously. Powered with Flask and SocketIO.

## Features
- Chat anonymously
- Lightweight and Interactive

## Installation
**Clone the repo**
```
git clone https://github.com/im-strange/pollify
```

**Customize** <br>
`server-info.json` contains server details that you may want to configure first before running
```json
{
    "host_ip": "127.0.0.1",
    "host_port": 8000,
    "debug": true,
    "server_link": null,
    "data_file": "clients.csv"
}
```
You can paste your ngrok link in `server_link` for effective sharing.

**Run** <br>
You can now run `main.py`

> Licensed with MIT
