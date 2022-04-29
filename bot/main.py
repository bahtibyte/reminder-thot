from pymongo import MongoClient
from discord.ext import commands
from quart import Quart
from datetime import datetime
import os

mongo = MongoClient(os.getenv('MONGO_HOST'))
alerts = mongo['reminder-thot']['alerts']

bot = commands.Bot(command_prefix='-')

app = Quart(__name__)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name="hi")
async def hi_command(ctx):
    await ctx.channel.send("hello")

@bot.event
async def on_message(message):
    if message.content.startswith('-alert'):

        msg = message.content.split('|')
        
        data = {
            'title': msg[1].strip(),
            'body': msg[2].strip(),
            'date': msg[3].strip()
        }
        
        alerts.insert_one(data)

        await message.channel.send('d')

@app.route("/")
async def hello():
    alerts.insert_one({'info': 'user visited', 'time': datetime.now()})
    return "hello world by bahti"

bot.loop.create_task(app.run_task())
bot.run(os.getenv('DISCORD_TOKEN'))
