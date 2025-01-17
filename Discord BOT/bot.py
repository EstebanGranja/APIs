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
    ranks = ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "EMERALD", "DIAMOND", "MASTER", "GRANDMASTER", "CHALLENGER"]

    def get_highest_ranked_entry(entries):
        solo_duo_entries = [entry for entry in entries if entry['queueType'] == 'RANKED_SOLO_5x5']
        if not solo_duo_entries:
            return None
        return max(solo_duo_entries, key=lambda entry: ranks.index(entry['tier']))

    summoner1_data = get_summoner_data(invocador1)
    summoner2_data = get_summoner_data(invocador2)

    summoner1_ranked_data = get_ranked_data(summoner1_data['id'])
    summoner2_ranked_data = get_ranked_data(summoner2_data['id'])

    summoner1_highest_rank = get_highest_ranked_entry(summoner1_ranked_data)
    summoner2_highest_rank = get_highest_ranked_entry(summoner2_ranked_data)

    if not summoner1_highest_rank and not summoner2_highest_rank:
        await interaction.response.send_message("Neither summoner has a rank in solo/duo queue.")
        return

    if not summoner1_highest_rank:
        await interaction.response.send_message(f"{invocador2} is better with rank {summoner2_highest_rank['tier']} {summoner2_highest_rank['rank']}.")
        return

    if not summoner2_highest_rank:
        await interaction.response.send_message(f"{invocador1} is better with rank {summoner1_highest_rank['tier']} {summoner1_highest_rank['rank']}.")
        return

    if ranks.index(summoner1_highest_rank['tier']) > ranks.index(summoner2_highest_rank['tier']):
        better_summoner = invocador1
        better_rank = summoner1_highest_rank
    elif ranks.index(summoner1_highest_rank['tier']) < ranks.index(summoner2_highest_rank['tier']):
        better_summoner = invocador2
        better_rank = summoner2_highest_rank
    else:
        if summoner1_highest_rank['rank'] > summoner2_highest_rank['rank']:
            better_summoner = invocador1
            better_rank = summoner1_highest_rank
        else:
            better_summoner = invocador2
            better_rank = summoner2_highest_rank

    await interaction.response.send_message(f"{better_summoner} is better with rank {better_rank['tier']} {better_rank['rank']}.")


bot.run(DS_API_KEY)
