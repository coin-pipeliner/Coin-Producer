import websockets
import asyncio
import json
from kafka import KafkaProducer
from json import dumps
import sys


async def produce(data_num):
    
    producer = KafkaProducer(
        acks = 0,
        compression_type = 'gzip',
        bootstrap_servers = ['kafka1:19091', 'kafka2:19092', 'kafka3:19093'],
        value_serializer = lambda x: dumps(x).encode('utf-8')
    )
    uri = 'wss://pubwss.bithumb.com/pub/ws'
    
    async with websockets.connect(uri) as websocket:
        greeting = await websocket.recv()
        print(greeting)

        subscribe_fmt = {
                "type":"ticker", 
                "symbols": ["BTC_KRW"], 
                "tickTypes": ["1H"]
        }
        subscribe_data = json.dumps(subscribe_fmt)
        await websocket.send(subscribe_data)

        for i in range(data_num):
            data = await websocket.recv()
            data = json.loads(data)
            producer.send('BTC_KRW', value=data)
            producer.flush()
            print(data)

if __name__ == '__main__':
    data_num = int(sys.argv[1])
    asyncio.run(produce(data_num))
