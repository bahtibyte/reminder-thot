from quart import Quart
import asyncio
import logging
import os
import asyncio
from hypercorn.asyncio import serve
from hypercorn.config import Config

loop = asyncio.get_event_loop()
app = Quart(__name__)

log = logging.getLogger(__name__)

@app.route("/")
def index():
    return "Hello World! From BootcampV2"

# loop.create_task(discord.connect())

if os.getenv('ENV') == 'PROD':
    port = os.getenv('PORT')
    hypercorn_config = Config()
    hypercorn_config.bind = ["0.0.0.0:" + port]

    log.info(f"\n\nRunning on: {hypercorn_config.bind}\n\n")
    loop.run_until_complete(serve(app, hypercorn_config))
else:
    loop.run_until_complete(serve(app, Config()))



