import os
import sys
import json
import time
import requests
import websocket
import threading
import random
from typing import List

# pip install websocket-client

GUILD_ID = "823785341201940500"
CHANNEL_ID = "1142048374758056016"
SELF_MUTE_OPTIONS = [True, False]
STATUS_OPTIONS = ["online", "dnd", "idle"]


def keep_online(token: str, status: str, self_mute: bool, self_deaf: bool) -> None:
    headers = {"Authorization": token, "Content-Type": "application/json"}
    validate = requests.get("https://discordapp.com/api/v9/users/@me", headers=headers)

    if validate.status_code != 200:
        print("[ERROR] Your token might be invalid. Please check it again.")
        sys.exit()

    userinfo = validate.json() 
    username = userinfo.get("username", "Unknown")
    userid = userinfo.get("id", "Unknown")

    print(f"Logged in as {username} ({userid})")

    ws = websocket.WebSocket()
    ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")

    start = json.loads(ws.recv())
    heartbeat_interval = start["d"]["heartbeat_interval"]

    auth_payload = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {
                "$os": "Windows 11",
                "$browser": "Google Chrome",
                "$device": "Windows",
            },
            "presence": {"status": status, "afk": False},
        },
        "s": None,
        "t": None,
    }

    voice_payload = {
        "op": 4,
        "d": {
            "guild_id": GUILD_ID,
            "channel_id": CHANNEL_ID,
            "self_mute": self_mute,
            "self_deaf": self_deaf,
        },
    }

    ws.send(json.dumps(auth_payload))
    ws.send(json.dumps(voice_payload))

    online = {"op": 1, "d": None}
    time.sleep(heartbeat_interval / 1000)
    ws.send(json.dumps(online))


def run_keep_online(token: str, status: str, self_mute: bool, self_deaf: bool) -> None:
    while True:
        keep_online(token, status, self_mute, self_deaf)
        time.sleep(30)
        os.system("cls" if os.name == "nt" else "clear")


def main():
    tokens: List[str] = [
        "XXXXXXXXXXXXXXXXXXXXXXX.YYYYYYYYY.ZZZZZZZZZZZZZZZZZZ",
        "XXXXXXXXXXXXXXXXXXXXXXX.YYYYYYYYY.ZZZZZZZZZZZZZZZZZZ",
    ]

    for token in tokens:
        thread = threading.Thread(
            target=run_keep_online,
            args=(
                token,
                random.choice(STATUS_OPTIONS),
                random.choice(SELF_MUTE_OPTIONS),
                False,  # Set SELF_DEAF as needed
            ),
        )
        thread.start()


if __name__ == "__main__":
    main()
