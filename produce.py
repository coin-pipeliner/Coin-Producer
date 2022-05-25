import websockets
import asyncio
import json
from kafka import KafkaProducer
import os


async def produce(env, code):

    producer = KafkaProducer(
        acks=0,
        compression_type="gzip",
        bootstrap_servers=["kafka1:19091", "kafka2:19092", "kafka3:19093"],
        value_serializer=lambda x: json.dumps(x).encode("utf-8"),
    )
    code = code.upper()
    uri = "wss://api.upbit.com/websocket/v1"
    topic = f"{env}.coin-pipeliner.{code}"
    print(code, env)
    while True:
        async with websockets.connect(uri, ping_interval=60) as websocket:

            subscribe_data = [
                {"ticket": "test"},
                {"type": "ticker", "codes": [code]},
            ]
            subscribe_data = json.dumps(subscribe_data)

            print("Send subscribe data :", subscribe_data)
            await websocket.send(subscribe_data)

            while True:
                data = await websocket.recv()
                data = json.loads(data)
                print(data)
                producer.send(topic, value=data)
                producer.flush()


if __name__ == "__main__":
    asyncio.run(
        produce(
            os.environ["ENV"],
            os.environ["CODE"]
        )
    )
