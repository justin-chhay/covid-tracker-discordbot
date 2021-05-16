'''
Justin Chhay
Created 05.16.2021
Covid-19 Tracker Discord Bot
'''

import os
import discord
import requests  #allows us to make http requests to
import json  #data we get from zenquotes API

client = discord.Client()
discordToken = os.environ["discordAPI_token"]

#variables
covid_keyTerms = ["covid", "covid19"]


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


#pulls random quote from ZenQuotesAPI
def get_quote():
    #get json data from api (the quote)
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]["q"] + " -" + json_data[0][
        "a"]  #key is q(quote) and a (author), places data in a string
    return quote


#lets Bot read Commands
@client.event
async def on_message(message):
    #make sure it returns smth if message is from the bot
    if message.author == client.user:
        return

    msg = message.content

    #Random Quote command
    if msg.startswith("!inspire"):
        quote = get_quote()
        await message.channel.send(quote)

    #auto-detects if covid terms are mentioned in any message
    if any(word in msg for word in covid_keyTerms):
        await message.channel.send("Did I hear something about Covid-19?")

#run the program in the bot (parameter is the bot token)
client.run(discordToken)