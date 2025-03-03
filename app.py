import os
import discord
import hmac
import hashlib
import random
from flask import Flask, jsonify, request
from discord_interactions import verify_key_decorator


app = Flask(__name__)

app.config["DISCORD_CLIENT_ID"] = os.environ["DISCORD_CLIENT_ID"]
DISCORD_PUBLIC_KEY = os.environ["DISCORD_PUBLIC_KEY"]
app.config["DISCORD_CLIENT_SECRET"] = os.environ["DISCORD_CLIENT_SECRET"]
app.config["DISCORD_BOT_TOKEN"] = os.environ["DISCORD_BOT_TOKEN"]

# Create a list of writing prompts
writing_prompts = [
    "You wake up in a world where everyone has superpowers except you.",
    "A detective is on the trail of a thief who can teleport.",
    "You find a diary that predicts the future.",
    "A spaceship lands in your backyard.",
    "You discover a hidden door in your house that leads to another dimension.",
    "A time traveler from the future needs your help.",
    "You inherit a mysterious, ancient artifact with magical powers.",
    "A friendly ghost haunts your new apartment.",
    "You have the ability to speak with animals, and they need your help.",
    "A secret society is trying to recruit you for their cause.",
    "You wake up one day with the ability to read minds.",
    "A scientist offers you a chance to live on Mars.",
    "You find a portal to a parallel universe in your basement.",
    "A stranger hands you a suitcase full of money and a cryptic note.",
    "You discover your best friend is a superhero in disguise.",
    "An ancient prophecy predicts you will save the world.",
    "You meet a future version of yourself who warns you of impending danger.",
    "A machine that grants wishes appears in your living room.",
    "You are the last human on Earth after an alien invasion.",
    "You find a map leading to a hidden treasure beneath your city.",
    "You develop the ability to control the weather.",
    "A genie grants you three wishes, but there are unexpected consequences.",
    "You wake up with no memories and a mysterious tattoo on your arm.",
    "A magical book transports you into its story.",
    "You receive a letter from a long-lost relative inviting you to a hidden island.",
    "You discover you can travel through time using an old pocket watch.",
    "A mysterious illness spreads through your town, and you are immune.",
    "You are chosen to represent humanity in an intergalactic council.",
    "You find a camera that shows you glimpses of the future.",
    "A dragon appears in your backyard and claims you are its rider.",
    "You discover a hidden underground city beneath your town.",
    "You are given a chance to relive one day of your life, but with a twist.",
    "A robot becomes your best friend and protector.",
    "You inherit a haunted mansion and must uncover its secrets.",
    "You find a pair of glasses that allow you to see people's true intentions.",
    "You are transported into your favorite video game and must complete a quest to return home.",
    "A mysterious voice in your head guides you through dangerous situations.",
    "You discover a hidden talent that makes you famous overnight.",
    "You are kidnapped by pirates and must find a way to escape.",
    "You find an ancient tree that grants you wisdom and knowledge.",
    "A famous celebrity asks for your help to solve a mystery.",
    "Digging in your garden you find a mysterious portal.",
    "Everyone in the world has forgotten the colour red apart from one person.",
    "There is a mysterious creature living the local canal.",
    "An attack drone becomes self-aware and chooses a new philosophy of pacifism.",
    "Following the strange smell you uncover the spaceship under the floorboards.",
    "A knight falls from his horse.",
    "You meet a god in the pub."
]

@app.route("/", methods=["GET"])
def home():
    return 'Discord Bot is running!'

@app.route("/interactions", methods=["POST"])
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
        elif command_name == "prompt":
            message_content = random.choice(writing_prompts)
        else:
            message_content = "Unknown"

        response_data = {
            "type": 4,
            "data": {"content": message_content},
        }

    return jsonify(response_data)

if __name__ == "__main__":
    app.run(debug=True)