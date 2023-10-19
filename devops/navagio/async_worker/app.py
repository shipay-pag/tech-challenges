import os
import faust

BROKER_URL = os.getenv('BROKER_URL', 'kafka://localhost')

app = faust.App(
    'channel',
    broker='kafka://localhost',
    store='memory://',
)

class MyModel(faust.Record):
    x: int

channel = app.channel(value_type=MyModel)

@app.agent(channel)
async def process(stream):
    async for event in stream:
        print(f'Received: {event!r}')

@app.timer(1.0)
async def populate():
    await channel.send(MyModel(303))