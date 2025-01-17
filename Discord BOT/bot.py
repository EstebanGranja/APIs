import discord
from discord.ext import commands
from discord import app_commands
import os
import requests


with open('riot_key', 'r') as file:
    RIOT_API_KEY = file.read().strip()

with open('ds_key', 'r') as file:
    DS_API_KEY = file.read().strip()

def get_summoner_data(summoner_name):
    url = f'https://las.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}'
    headers = {'X-Riot-Token': RIOT_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()


def get_ranked_data(summoner_id):
    url = f'https://las.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}'
    headers = {'X-Riot-Token': RIOT_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()


def get_mastery_data(summoner_id):
    url = f'https://las.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}'
    headers = {'X-Riot-Token': RIOT_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()



intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(f'Failed to sync commands: {e}')


@bot.tree.command(name="whoisbetter")
async def whoisbetter(interaction: discord.Interaction, invocador1: str, invocador2: str):
    summoner1 = get_summoner_data(invocador1)
    summoner2 = get_summoner_data(invocador2)

    ranked1 = get_ranked_data(summoner1['id'])
    ranked2 = get_ranked_data(summoner2['id'])

    mastery1 = get_mastery_data(summoner1['id'])
    mastery2 = get_mastery_data(summoner2['id'])

    # Calculo temporal de mejor jugador
    if summoner1['summonerLevel'] > summoner2['summonerLevel']:
        better = invocador1
    else:
        better = invocador2

    await interaction.response.send_message(f'El mejor jugador es {better}!')


bot.run(DS_API_KEY)
