#********************************************************************************#
#       Author : Sanjay Sengupta - Enterprise Cloud & Big Data Analytics Architect
# Last Updated : Jan 8, 2024
#********************************************************************************#

from yahoo_fin import stock_info as si
import asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData

### ticker quote producer function ###
def get_ticker_quote(ticker):
    ticker_quote = '{"Ticker":"' + ticker.upper() + '","Price":"' + str(round(si.get_live_price(ticker), 2)) + '"}'
    print(ticker_quote)
    return ticker_quote

### test code block ###
# get_ticker_quote(ticker)

### ticker quote event producer function ###
connection_str = 'Endpoint=sb://idev-event-hubs-namespace.servicebus.windows.net/;SharedAccessKeyName=iDEV-Event-Hub-Authorization-Rule;SharedAccessKey=zv2U3JveHkej2d+9oTbBY2HYYjXkuHUku+AEhFBa6YM=;EntityPath=idev-event-hub'
event_hub_path = 'idev-event-hub'
async def stream_ticker_quote():
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
    # the event hub name.
    producer = EventHubProducerClient.from_connection_string(conn_str=connection_str, eventhub_name=event_hub_path)
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        event_data_batch.add(EventData(get_ticker_quote(ticker = 'tsla')))
        event_data_batch.add(EventData(get_ticker_quote(ticker = 'meta')))
        event_data_batch.add(EventData(get_ticker_quote(ticker = 'googl')))
 
        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)

### ticker quote streaming event producer code ###
while True:
    asyncio.run(stream_ticker_quote())
