#!/usr/bin/env python

from typing_extensions import Required
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord import Client, Intents, Embed
import requests
from dotenv import load_dotenv
import os
from web3 import Web3


load_dotenv(".env")

client = commands.Bot(command_prefix="!")
slash = SlashCommand(client, sync_commands=True)
token = os.getenv("PRICE_CHECKER_TOKEN")


@slash.slash(
    name="pricebot",
    description="Shows token prices",
    guild_ids=[  #    # Dangywing Test Server
        849034764190875669,
        # ,
        #    # club-nfts
        # 812365773372129311,
        #    # manzcoin-nftz
        #    826820629260533790,
        # club-ngmi
        762763149728153601,
        # club-defi
        907968023854460958,
    ],
    options=[
        create_option(
            name="coinage",
            description="coins to choose from",
            required=True,
            option_type=3,
            choices=[create_choice(name="JEWEL", value="defi-kingdoms")],
        )
    ],
)
async def price_finder(ctx: SlashContext, **kwargs):

    # COIN_NAME = "defi-kingdoms"

    for COIN_NAME in kwargs.values():
        await ctx.defer(hidden=False)

        data_url = (
            "https://api.coingecko.com/api/v3/simple/price?ids="
            + str(COIN_NAME)
            + "&vs_currencies=usd&include_market_cap=true"
        )
        response = requests.get(data_url)
        json_data = response.json()
        current_price = json_data[COIN_NAME]["usd"]
        embed = Embed(title="$" + str(current_price * 6666), type="rich")
        embed.set_author(name=COIN_NAME + " price")
        await ctx.send(embed=embed)


client.run(token)
