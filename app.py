import os
import discord
import hmac
import hashlib
from flask import Flask, jsonify, request
from discord_interactions import verify_key_decorator


app = Flask(__name__)

app.config["DISCORD_CLIENT_ID"] = os.environ["DISCORD_CLIENT_ID"]
DISCORD_PUBLIC_KEY = os.environ["DISCORD_PUBLIC_KEY"]
app.config["DISCORD_CLIENT_SECRET"] = os.environ["DISCORD_CLIENT_SECRET"]
app.config["DISCORD_BOT_TOKEN"] = os.environ["DISCORD_BOT_TOKEN"]

@app.route("/", methods=["GET"])
def home():
    return 'Discord Bot is running!'

@app.route("/interactions", methods=["POST"])
#@app.route("/interactions", methods=["GET"])
async def interactions():
    print(f"👉 Request: {request.json}")
    raw_request = request.json
    return interact(raw_request)

@verify_key_decorator(DISCORD_PUBLIC_KEY)
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

def verify_discord_request(req):
    signature = req.headers.get('X-Signature-Ed25519')
    timestamp = req.headers.get('X-Signature-Timestamp')
    body = req.data.decode('utf-8')

    if not signature or not timestamp:
        return False

    try:
        # Combine timestamp and body to create the message
        message = timestamp + body
        message_bytes = message.encode('utf-8')

        # Decode the public key and signature
        public_key_bytes = bytes.fromhex(DISCORD_PUBLIC_KEY)
        signature_bytes = bytes.fromhex(signature)

        # Verify the signature
        verify_key = nacl.signing.VerifyKey(public_key_bytes)
        verify_key.verify(message_bytes, signature_bytes)
        return True
    except Exception as e:
        print(f"Verification failed: {e}")
        return False

@app.route('/webhook', methods=['POST'])
def webhook():
    if not verify_discord_request(request):
        return jsonify({"error": "Invalid request signature"}), 401

    # Handle the request as it is verified
    data = request.json
    return jsonify({"message": "Request verified", "data": data}), 200

if __name__ == "__main__":
    app.run(debug=True)