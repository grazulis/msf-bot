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
    "A mysterious creature speaks to you in your dreams and tells you that when you awake, you will have the ability to see into another realm.",
    "Your pet dragon transforms into a person.",
    "You are gifted with the strongest, most elusive sword in the kingdom, but if you use it you will never be able to speak again.",
    "A magical world exists underground. To get there, you’ll need to start digging.",
    "You wake up and find out that you’re the only living person left on the planet.",
    "On her deathbed, your grandmother tells you that there’s a hidden treasure buried in her backyard. The family has been trying to locate it for decades. It’s up to you to finally find it.",
    "The ocean becomes the sky.",
    "You must save your kingdom from ruin by learning how to breathe fire.",
    "You have the power to read the lost language, making you the only person to decipher the scroll.",
    "Fairies are tired of being used for free labor.",
    "Your favorite fairy tale is now set in 2019.",
    "You are kidnapped by a knight who demands your assistance in sleighing the city’s most dangerous dragon.",
    "A man and his wife own the largest potion store in town. Little do the townspeople know, but they’re all being slowly poisoned by the potions.",
    "A magical toad begins talking to you, but you’re the only person who can hear him.",
    "You come into possession of a ring that can change the weather to whatever you decide.",
    "You’re selected to take part in a secretive, underground magic university… but you have to kill someone to go.",
    "You wake up to find yourself a member of King Arthur’s Round Table.",
    "An underwater society decides to overtake the world.",
    "Regular person by day, a shape shifter by night.",
    "Satan puts you in charge of Hell.",
    "Your whole family has fought in the space military, but you’ve decided to no longer take part in it.",
    "In an alternate universe where global warming has ruined the planet, you’ve spent your entire life living in an airplane on autopilot.",
    "You’re a 15-year-old in the middle of a zombie apocalypse. However, a cure has been found that not only rids the infected person of the virus before they turn but prevents it altogether. Only one problem… Your parents are anti-vaxxers.",
    "NASA engineers monitor the curiosity rover’s actions. All seems normal until the robot suddenly changes its course. The scientists attempt to correct it over and over until they suddenly receive a transmission from the rover: 'Will Save Oppy'.",
    "What if a nuclear submarine was ordered to launch their nuclear arsenal onto the world?",
    "What if the world we live in is actually a computer simulation?",
    "What if the past and present timelines began to merge?",
    "What if your stepfather or stepmother is actually your future self?",
    "What if the sun began to die?",
    "What if the universe as we know it is actually someone’s imagination?",
    "Everyone on earth begins to experience universal amnesia.",
    "The year is 2200. What does the world look like to you?",
    "In the future, we no longer require water, air, or food. We are a super efficient team of robots.",
    "What do you think happens when the grid goes down?",
    "Describe your perfect utopian world.",
    "Your penpal lives on the opposite side of the universe.",
    "Aliens who only communicate with sign language invade. To avoid war, our governments must engage a vastly marginalized portion of the human population: the hearing-impaired.",
    "A rogue planet with strange properties collides with our sun, and after it’s all over, worldwide temperature falls forty degrees. Write from the perspective of a someone trying to keep his tropical fruit trees alive.",
    "Ever read about the world’s loneliest whale? Write a story in which he’s actually the survivor of an aquatic alien species which crashed here eons ago, and he’s trying very hard to learn the 'local' whale language so he can fit in. Write from his perspective the first time he makes contact.",
    "An alien planet starts receiving bizarre audio transmissions from another world (spoiler: they’re from Earth). What does it mean? Are they under attack? Some think so…until classic rock ‘n’ roll hits the airwaves, and these aliens discover dancing. Write from the perspective of the teenaged alien who first figures it out.",
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