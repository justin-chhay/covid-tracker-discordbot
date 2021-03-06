'''
Justin Chhay
Created 05.16.2021
Covid-19 Tracker Discord Bot
'''

import os
import discord # import discord.py commands so that we can manipulate the bot's Discord ,essages
import requests  # allows us to make http requests to access APIs
import json  # data we get from zenquotes API
from datetime import datetime  # we can access local pc date and time


client = discord.Client()
discordToken = os.environ["discordAPI_token"]


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


# Retrieves random inspirational quote from ZenQuotesAPI
def get_quote():
    # get json data from api (the quote)
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]["q"] + " - " + json_data[0]["a"]
    return quote


# Retrieves worldwide coronavirus data from Diseases.sh API
def get_worldData():
    response = requests.get("https://disease.sh/v3/covid-19/all")
    json_data = json.loads(response.text)
    return json_data


# Retrieves data regarding specified country from Diseases.sh API
def get_country(country):
    response = requests.get("https://disease.sh/v3/covid-19/countries")
    json_data = json.loads(response.text)
    for item in json_data:
        data = item["country"]
        if data.lower() == country.lower():
            return item
    return -1  # if specified country does not exist


# Retrieves data regarding specified country (IF HAS TWO WORDS IN NAME) from Diseases.sh API
def get_country2(country_fname, country_lname):
    response = requests.get("https://disease.sh/v3/covid-19/countries")
    json_data = json.loads(response.text)
    for item in json_data:
        data = item["country"]
        if data.lower() == (country_fname.lower() + " " + country_lname.lower()):
            return item
    return -1  # if specified country does not exist


# Returns color for embed msg based on severity of covid in specified country (determined by deaths)
def get_covid_color(num):
    x = num["deaths"]
    if x <= 1000:
        return 0x4AF106
    elif x <= 50000:
        return 0x45731E
    elif x <= 100000:
        return 0x675E24
    elif x <= 500000:
        return 0x8D472B
    else:
        return 0xC82538


# Returns embedded message for country (related stats)
def makeEmbed(data, time):
    bedmsg = discord.Embed(title=str(data["country"] + ", " + data["continent"]), color=get_covid_color(data))
    bedmsg.add_field(name="Total Cases:", value=str("{:,}".format(data["cases"])), inline=False)
    bedmsg.add_field(name="Active:", value=str("{:,}".format(data["active"])), inline=False)
    bedmsg.add_field(name="Recovered:", value=str("{:,}".format(data["recovered"])), inline=False)
    bedmsg.add_field(name="Deaths:", value=str("{:,}".format(data["deaths"])), inline=False)
    bedmsg.set_footer(text="Updated at " + time + " EST.")
    bedmsg.set_thumbnail(url=str(data["countryInfo"]["flag"]))
    return bedmsg


# Lets CovidTracker Bot read messages and act, when client sends msg
@client.event
async def on_message(message):
    # local variables
    now = datetime.now()  # datetime object var, local so that it constantly updates date/time
    dt_string = now.strftime("%d/%m/%Y ??? %H:%M:%S") #format the datetime object into a string
    msg = message.content #command sent from user
    msg_parameters = msg.split(" ") #split up command into an array (to discern from command indentifier and value)
    parameter = ""
    second_parameter = ""

    # Check if additional parameters added to command
    if len(msg_parameters) == 2:
        parameter = msg_parameters[1]
    elif len(msg_parameters) == 3: #special case, if country name has two words
        parameter = msg_parameters[1]
        second_parameter = msg_parameters[2]

    # Make sure it returns smth if message is from the bot
    if message.author == client.user:
        return

    # Help Command - lists ALL current bot cmds
    if msg.lower().startswith("!h" or "!help"):
        bedmsg = discord.Embed(title="Help - CovidTracker3000 Bot Commands", color=0x009BFF)
        bedmsg.add_field(name="!inspire", value="Receive a random inspirational quote.", inline=False)
        bedmsg.add_field(name="!cases", value="Gives real-time worldwide stats.", inline=False)
        bedmsg.add_field(name="!cases <country>", value="Gives real-time stats for specified country parameter.",
                         inline=False)
        bedmsg.set_footer(text="Created by @justin-chhay on GitHub", icon_url="https://i.imgur.com/ORXlNqT.png")
        await message.channel.send(embed=bedmsg)

    # Random Quote command
    if msg.lower().startswith("!i" or "!inspire"):
        quote = get_quote()
        bedmsg = discord.Embed(title="Inspirational Quote", description=quote, color=0x009BFF)
        bedmsg.set_footer(text="Created by @justin-chhay on GitHub", icon_url="https://i.imgur.com/ORXlNqT.png")
        await message.channel.send(embed=bedmsg)

    # Total Cases in Specified Country or Worldwide
    if msg.lower().startswith("!c" or "!cases"):
        # if parameter exists, give data for specified country. Otherwise give worldwide data!
        if parameter != "" and second_parameter == "":  # one word in country name
            data = get_country(parameter)
            # Sends out embed message including stats for specified country
            if data != -1:
                await message.channel.send(embed=makeEmbed(data, dt_string))
            else:
                await message.channel.send("Input for country is invalid.")
        elif parameter != "" and second_parameter != "":  # two words in country name
            data = get_country2(parameter, second_parameter)
            # Sends out embed message including stats for specified country
            if data != -1:
                await message.channel.send(embed=makeEmbed(data, dt_string))
            else:
                await message.channel.send("Input for country is invalid.")
        else:  # no parameter, worldwide stats
            data = get_worldData()
            bedmsg = discord.Embed(title="Worldwide", color=0xD85337)
            bedmsg.add_field(name="Total Cases:", value=str("{:,}".format(data["cases"])), inline=False)
            bedmsg.add_field(name="Active:", value=str("{:,}".format(data["active"])), inline=False)
            bedmsg.add_field(name="Recovered:", value=str("{:,}".format(data["recovered"])), inline=False)
            bedmsg.add_field(name="Deaths:", value=str("{:,}".format(data["deaths"])), inline=False)
            bedmsg.set_footer(text="Updated at " + dt_string + " EST.")
            bedmsg.set_thumbnail(url="https://i.imgur.com/yLPDm9H.png")
            await message.channel.send(embed=bedmsg)


# run the program in the bot (parameter is the bot token)
client.run(discordToken)