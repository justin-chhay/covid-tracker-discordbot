'''
Justin Chhay
Created 05.16.2021
Covid-19 Tracker Discord Bot
'''

import os
import discord
import requests  #allows us to make http requests to access APIs
import json  #data we get from zenquotes API
from datetime import datetime

client = discord.Client()
discordToken = os.environ["discordAPI_token"]


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


#Retrieves random inspirational quote from ZenQuotesAPI
def get_quote():
    #get json data from api (the quote)
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]["q"] + " -" + json_data[0]["a"]  #key is q(quote) and a (author), places data in a string
    return quote


#Retrieves data regarding total cases from Diseases.sh API
def get_worldCases():
    response = requests.get("https://disease.sh/v3/covid-19/all")
    json_data = json.loads(response.text)
    data = json_data["cases"]
    return data

#Lets CovidTracker Bot read messages and act
@client.event
async def on_message(message):
    #local variables
    now = datetime.now()  # datetime object var, local so that it constantly updates date/time
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    msg = message.content
    msg_parameters = msg.split(" ")
    parameter = ""
    second_parameter = ""

    # Check if additional parameters added to command
    if len(msg_parameters) == 2:
        parameter = msg_parameters[1]
    elif len(msg_parameters) == 3:
        second_parameter = msg_parameters[2]

    #Make sure it returns smth if message is from the bot
    if message.author == client.user:
        return

    #Help Command - lists ALL current bot cmds
    if msg.startswith("!h" or "!help"):
        await message.channel.send("Current commands are:")
        await message.channel.send("!inspire")
        await message.channel.send("!cases")
        await message.channel.send("!cases <country>")

    #Random Quote command
    if msg.startswith("!inspire"):
        quote = get_quote()
        await message.channel.send(quote)

    #Total Cases in Specified Country or Worldwide
    if msg.startswith("!cases"):
        #if parameter exists, give data for specified country. Otherwise give worldwide data!
        if parameter == "specifiedCountry":
            data = str(get_worldCases())
            await message.channel.send("There are " + data + " coronavirus cases in {} as of {}".format("specified country", dt_string)+" (EST).")
        else:
            data = str(get_worldCases())
            await message.channel.send("There are " + data + " coronavirus cases worldwide as of {}".format(dt_string)+" (EST).")


#run the program in the bot (parameter is the bot token)
client.run(discordToken)