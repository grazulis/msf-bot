import os
import discord
from flask import Flask, jsonify, request
# from flask_discord_interactions import DiscordInteractions

app = Flask(__name__)

app.config["DISCORD_CLIENT_ID"] = os.environ["DISCORD_CLIENT_ID"]
DISCORD_PUBLIC_KEY = os.environ["DISCORD_PUBLIC_KEY"]
app.config["DISCORD_CLIENT_SECRET"] = os.environ["DISCORD_CLIENT_SECRET"]
app.config["DISCORD_BOT_TOKEN"] = os.environ["DISCORD_BOT_TOKEN"]

@app.route("/", methods=["GET"])
def home():
    return 'Discord Bot is running!'

#@app.route("/interactions", methods=["POST"])
@app.route("/interactions", methods=["GET"])
async def interactions():
    print(f"👉 Request: {request.json}")
    raw_request = request.json
    return interact(raw_request)

# @verify_key_decorator(DISCORD_PUBLIC_KEY)
def interact(raw_request):
    if raw_request["type"] == 1:  # PING
        response_data = {"type": 1}  # PONG
    else:
        data = raw_request["data"]
        command_name = data["name"]

        if command_name == "hello":
            message_content = "Hello there!"
        elif command_name == "echo":
            original_message = data["options"][0]["value"]
            message_content = f"Echoing: {original_message}"

        response_data = {
            "type": 4,
            "data": {"content": message_content},
        }

    return jsonify(response_data)

if __name__ == "__main__":
    app.run(debug=True)