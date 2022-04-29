from pymongo import MongoClient
from discord.ext import commands
from discord import Embed
from quart import Quart
from datetime import datetime
from hypercorn.asyncio import serve
from hypercorn.config import Config
import os

mongo = MongoClient(os.getenv('MONGO_HOST'))
alerts = mongo['reminder-thot']['alerts']
archives = mongo['reminder-thot']['archives']

bot = commands.Bot(command_prefix='-')

app = Quart(__name__)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

async def refresh():
    for doc in alerts.find():
        if 'title' not in doc:
            continue
        
        if datetime.now() > datetime.strptime(doc['date'] + ' 9', '%m-%d-%Y %H'):
            embed = Embed(title=doc['title'] + ' Reminder', description=doc['body'], color=0xff0000)
            channel = await bot.fetch_channel(969683673639157790)
            await channel.send(embed=embed)

            alerts.find_one_and_delete({"_id": doc['_id']})

        print('Completed refresh')

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
        archives.insert_one(data)

        await message.channel.send('Alert created for ' + data['date'])

@app.route("/")
async def hello():
    mongo['reminder-thot']['visits'].insert_one({'visit-time': datetime.now()})
    await refresh()
    return 'Welcome to reminder-thot'

hypercorn_config = Config()
hypercorn_config.bind = ['0.0.0.0:' + os.getenv('PORT')]

print(f'\n\nRunning on: {hypercorn_config.bind}\n\n')
bot.loop.create_task(serve(app, hypercorn_config))
bot.run(os.getenv('DISCORD_TOKEN'))
